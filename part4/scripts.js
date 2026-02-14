// ============================================
// HBnB - Final Clean JavaScript
// ============================================

const API_URL = 'http://127.0.0.1:5000/api/v1';

// ========== Cookie Helpers ==========
function getCookie(name) {
    const value = ; ${document.cookie};
    const parts = value.split(; ${name}=);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function setCookie(name, value, days = 7) {
    const d = new Date();
    d.setTime(d.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = ${name}=${value}; path=/; expires=${d.toUTCString()};
}

function deleteCookie(name) {
    document.cookie = ${name}=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;
}

// ========== Auth Functions ==========
function isAuthenticated() {
    return getCookie('token') !== null;
}

function updateAuthUI() {
    const loginBtn = document.getElementById('login-btn');
    const userMenu = document.getElementById('user-menu');
    const userInitial = document.getElementById('user-initial');
    const email = localStorage.getItem('userEmail');

    if (isAuthenticated() && email) {
        if (loginBtn) loginBtn.style.display = 'none';
        if (userMenu) {
            userMenu.classList.remove('hidden');
            userMenu.classList.add('flex');
        }
        if (userInitial) {
            userInitial.textContent = email.charAt(0).toUpperCase();
        }
    } else {
        if (loginBtn) loginBtn.style.display = 'inline-block';
        if (userMenu) {
            userMenu.classList.add('hidden');
            userMenu.classList.remove('flex');
        }
    }
}

function setupLogout() {
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            deleteCookie('token');
            localStorage.removeItem('userEmail');
            window.location.href = 'index.html';
        });
    }
}

// ========== Login ==========
async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const errorMsg = document.getElementById('error-msg');

    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok && data.access_token) {
            setCookie('token', data.access_token, 7);
            localStorage.setItem('userEmail', email);
            window.location.href = 'index.html';
        } else {
            if (errorMsg) errorMsg.textContent = data.message || 'Invalid credentials';
        }
    } catch (error) {
        if (errorMsg) errorMsg.textContent = 'Connection error';
    }
}

function setupLoginForm() {
    const form = document.getElementById('login-form');
    if (form) {
        form.addEventListener('submit', handleLogin);
    }
}

// ========== Places ==========
async function fetchPlaces() {
    try {
        const response = await fetch(`${API_URL}/places/`);
        if (!response.ok) throw new Error('Failed');
        return await response.json();
    } catch (error) {
        return [];
    }
}

function getPlaceImage(placeId) {
    const images = [
        'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600',
        'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=600',
        'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=600',
        'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=600',
        'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=600'
    ];
    const hash = placeId.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
    return images[hash % images.length];
}

function getAmenitiesIcons(amenities) {
    if (!amenities || amenities.length === 0) return '';
    
    const iconMap = {
        'WiFi': 'fa-wifi',
        'Pool': 'fa-swimming-pool',
        'Parking': 'fa-car',
        'Breakfast': 'fa-coffee',
        'Gym': 'fa-dumbbell',
        'AC': 'fa-snowflake'
    };

    return amenities.slice(0, 4).map(a => {
        const icon = iconMap[a.name] || 'fa-check';
        return `<div class="flex items-center gap-2 text-sm text-gray-600">
            <i class="fas ${icon} text-purple-600"></i>
            <span>${a.name}</span>
        </div>`;
    }).join('');
}

function createPlaceCard(place) {
    const isFavorite = localStorage.getItem(`fav_${place.id}`) === 'true';
    const heartClass = isFavorite ? 'fas' : 'far';

    return `
        <div class="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition relative">
            <button class="absolute top-3 right-3 z-10 w-10 h-10 bg-white rounded-full flex items-center justify-center shadow-md hover:scale-110 transition favorite-btn" data-id="${place.id}">
                <i class="${heartClass} fa-heart text-red-500 text-xl"></i>
            </button>
            
            <img src="${getPlaceImage(place.id)}" class="w-full h-48 object-cover" alt="${place.title}">
            
            <div class="p-4">
                <h3 class="text-xl font-bold mb-2">${place.title}</h3>
                <p class="text-gray-600 text-sm mb-3">${(place.description || '').substring(0, 100)}...</p>
                
                <div class="flex flex-wrap gap-3 mb-4">
                    ${getAmenitiesIcons(place.amenities)}
                </div>
                
                <div class="flex items-center justify-between">
                    <div>
                        <span class="text-2xl font-bold text-purple-600">${place.price_per_night}</span>
                        <span class="text-gray-600 text-sm"> SAR/night</span>
                    </div>
                    <a href="place.html?id=${place.id}" class="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition font-semibold">View</a>
                </div>
            </div>
        </div>
    `;
}
async function displayPlaces() {
    const container = document.getElementById('places-list');
    if (!container) return;
    await displayPlacesInContainer(container, 'price-filter');
}

async function displayPlacesInContainer(container, filterElementId) {
    if (!container) return;

    try {
        const places = await fetchPlaces();

        if (!places || places.length === 0) {
            container.innerHTML = '<div class="col-span-full text-center py-12 text-gray-600">No places available</div>';
            return;
        }

        function renderPlaces(list) {
            container.innerHTML = list.map(p => createPlaceCard(p)).join('');
            setupFavorites();
        }

        renderPlaces(places);

        const filter = document.getElementById(filterElementId);
        if (filter) {
            filter.addEventListener('change', (e) => {
                const val = e.target.value;
                if (val === 'all') {
                    renderPlaces(places);
                } else {
                    const filtered = places.filter(p => p.price_per_night <= Number(val));
                    renderPlaces(filtered);
                }
            });
        }
    } catch (error) {
        container.innerHTML = '<div class="col-span-full text-center py-12 text-red-600">Error loading places</div>';
    }
}
function setupFavorites() {
    document.querySelectorAll('.favorite-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();

            const id = btn.dataset.id;
            const icon = btn.querySelector('i');
            const isFav = localStorage.getItem(fav_${id}) === 'true';

            if (isFav) {
                localStorage.removeItem(fav_${id});
                icon.classList.remove('fas');
                icon.classList.add('far');
            } else {
                localStorage.setItem(fav_${id}, 'true');
                icon.classList.remove('far');
                icon.classList.add('fas');
            }
        });
    });
}

// ========== Place Details ==========
async function fetchPlaceDetails(id) {
    try {
        const response = await fetch(${API_URL}/places/${id});
        if (!response.ok) throw new Error('Failed');
        return await response.json();
    } catch (error) {
        return null;
    }
}
Nada Al-Mutairi
nada_almutairi
In voice

Sondos Alrubaish — 2:41 AM
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HBnB - Luxury Stays in Riyadh</title>

    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">

    <!-- Custom CSS -->
    <link rel="stylesheet" href="css/styles.css">
    <link rel="stylesheet" href="css/index.css">
</head>
Shaden — 2:44 AM
---
fetch("http://127.0.0.1:5000/api/v1/places/").then(r => r.json()).then(console.log)
Sondos Alrubaish — 2:47 AM
Image
Shaden — 2:51 AM
️ افتحي الصفحة
️ اضغطي الثلاث نقاط فوق يمين
️ More Tools → Extensions
 فعّلي Incognito Mode للمتصفح
افتحي الصفحة في نافذة Incognito
chrome://extensions/
 اختبري هذا معي:
افتحي الصفحة
ثم افتحي Inspect
وبعدها اسحبي DevTools للأسفل بدل اليمين
(في أعلى DevTools فيه ثلاث نقاط → Dock side → اختاري bottom)
لو رجع تصميم البطاقات طبيعي؟
إذا نعم → المشكلة Responsive breakpoints فقط.
Shaden — 2:58 AM
<link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
<link rel="stylesheet" href="{{ url_for('static', filename='css/index.css') }}">
---
<script src="{{ url_for('static', filename='js/scripts.js') }}"></script>
from flask import render_template

@app.route("/")
def home():
    return render_template("index.html")
Sondos Alrubaish — 3:02 AM
from flask import Flask
from flask_restx import Api
from flask import render_template
from config import DevelopmentConfig
from app.extensions import db, bcrypt, jwt, cors

from app.api.v1.users import api as users_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns


def create_app(config_class=DevelopmentConfig):
    app = Flask(name)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/": {"origins": ""}})

    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API",
        doc="/api/v1/"
    )

    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(auth_ns, path="/api/v1/auth")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")

    return app
Shaden — 3:05 AM
from flask import Flask, render_template
from flask_restx import Api
from config import DevelopmentConfig
from app.extensions import db, bcrypt, jwt, cors

from app.api.v1.users import api as users_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns


def create_app(config_class=DevelopmentConfig):
    app = Flask(name)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/": {"origins": ""}})

    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API",
        doc="/api/v1/"
    )

    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(auth_ns, path="/api/v1/auth")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")

    # 👇 هذا هو الجزء الجديد
    @app.route("/")
    def home():
        return render_template("index.html")

    return app
Sondos Alrubaish — 3:07 AM
Image
Shaden — 3:12 AM
روحي للـ Console مرة ثانية
لكن هذه المرة:
لا تكتبي fetch يدويًا
بس حدّثي الصفحة (F5)
وقولي لي:
هل يظهر أي Error أحمر بعد تحميل الصفحة؟
أنا متأكد فيه error مخفي الآن.
async function renderPlacesList() {
    const container = document.getElementById('places-list');
    if (!container) return;

    container.innerHTML = "Loading...";

    try {
        const places = await fetchPlaces();
        console.log("PLACES:", places);   

        container.innerHTML = "";  

        places.forEach(place => {
            const div = document.createElement("div");
            div.innerHTML = 
                <div style="border:1px solid #ccc; padding:10px; margin:10px;">
                    <h3>${place.title || place.name || "No Title"}</h3>
                    <p>${place.price || place.price_per_night || 0} SAR</p>
                </div>
            ;
            container.appendChild(div);
        });

    } catch (error) {
        console.error("ERROR:", error);
        container.innerHTML = "Error loading places";
    }
}
-------------
في scripts.js عندك:
const page = document.body.dataset.page;

if (page === 'index') {
    renderPlacesList();
}
لو ما عندك هذا داخل HTML:
<body data-page="index">
الدالة ما تشتغل أبدًا.
Shaden — 3:28 AM
renderPlacesList()
Sondos Alrubaish — 3:29 AM
Image
Nada Al-Mutairi — 4:38 AM
9B7BB8
Sondos Alrubaish — 5:24 AM
from flask import Flask
from flask_restx import Api
from flask_cors import CORS

from app.extensions import db, bcrypt, jwt

def create_app(config_class):
    app = Flask(name)
    app.config.from_object(config_class)

    CORS(app, 
         resources={r"/api/": {"origins": ""}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API",
        doc="/api/v1/"
    )

    from app.api.v1.users import api as users_ns
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns

    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(auth_ns, path="/api/v1/auth")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")

    return app
Shaden — 9:42 PM
Science in Financial Economics
investment
Financial Analysis

FinTech
Sondos Alrubaish — 10:12 PM
from app.extensions import db

class SQLAlchemyRepository:
    def init(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()
        return obj

    def get_by_id(self, obj_id):

        return db.session.get(self.model, obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self):
        db.session.commit()

    def delete(self, obj):
        db.session.delete(obj)
        db.session.commit()
----
from app.extensions import db
from app.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.models.review import Review


class ReviewRepository(SQLAlchemyRepository):
    def init(self):
        super().init(Review)

    def get_by_user_and_place(self, user_id, place_id):
        return (
            self.model.query
            .filter_by(user_id=user_id, place_id=place_id)
            .first()
        )
    def get_by_place_id(self, place_id):
        return Review.query.filter_by(place_id=place_id).order_by(Review.created_at.desc()).all()
---
from app.extensions import db
from app.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.models.place import Place


class PlaceRepository(SQLAlchemyRepository):
    def init(self):
        super().init(Place)

    def get_by_owner(self, user_id):
        return self.model.query.filter_by(owner_id=user_id).all()
----
from app.extensions import db
from app.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.models.amenity import Amenity


class AmenityRepository(SQLAlchemyRepository):
    def init(self):
        super().init(Amenity)

    def get_by_name(self, name):
        return self.model.query.filter_by(name=name).first()
---
from app.extensions import db, bcrypt
from app.models.base_model import BaseModel


class User(BaseModel):
    tablename = "users"

    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(128), nullable=True)
    last_name = db.Column(db.String(128), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship("Place", back_populates="owner", cascade="all, delete-orphan")
    reviews = db.relationship("Review", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password: str):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
----
from app.extensions import db
from app.models.base_model import BaseModel


class Review(BaseModel):
    tablename = "reviews"

    text = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey("places.id"), nullable=False)

    table_args = (
        db.UniqueConstraint("user_id", "place_id", name="uq_review_user_place"),
        db.CheckConstraint("rating >= 1 AND rating <= 5", name="ck_review_rating_1_5"),
    )

    user = db.relationship("User", back_populates="reviews")
    place = db.relationship("Place", back_populates="reviews")

    def to_dict(self):
        return {
            "id": str(self.id),
            "text": self.text,
            "rating": self.rating,
            "user_id": str(self.user_id),
            "place_id": str(self.place_id),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "user": {
                "id": str(self.user.id),
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "email": self.user.email
            }
    }
----
from app.extensions import db
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    tablename = "amenities"

    name = db.Column(db.String(50), nullable=False, unique=True)

    places = db.relationship(
        "Place",
        secondary="place_amenity",
        back_populates="amenities"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
Sondos Alrubaish — 10:20 PM
----
from sqlalchemy import create_engine
from config import config


def get_engine(env="development"):
    return create_engine(
        config[env].SQLALCHEMY_DATABASE_URI,
        echo=False,
        future=True
    )
----
from sqlalchemy.orm import sessionmaker
from app.db.database import get_engine

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=get_engine()
)
Nada Al-Mutairi — 10:23 PM
>
Sondos Alrubaish — 10:23 PM
=========
# app/api/v1/users.py

from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import facade
from app.extensions import db

message.txt
5 KB
Nada Al-Mutairi — 10:25 PM
>
Sondos Alrubaish — 10:25 PM
======
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.facade import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'place_id': fields.String(required=True, description='Place ID')
})

@api.route('/')
class ReviewList(Resource):
    def get(self):
        try:
            place_id = request.args.get('place_id')

            if place_id:
                reviews = facade.get_reviews_by_place(place_id)
            else:
                reviews = facade.get_all_reviews()

            return [r.to_dict() for r in reviews], 200

        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"Error: {str(e)}")

    @api.expect(review_model)
    @jwt_required()
    def post(self):
        try:
            current_user_id = get_jwt_identity()
            review_data = api.payload or {}

            rating = review_data.get('rating')
            try:
                rating_int = int(rating)
            except (TypeError, ValueError):
                api.abort(400, 'Rating must be between 1 and 5')

            if rating_int < 1 or rating_int > 5:
                api.abort(400, 'Rating must be between 1 and 5')

            review_data["user_id"] = current_user_id

            new_review = facade.create_review(review_data)
            return new_review.to_dict(), 201

        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"Error: {str(e)}")
Nada Al-Mutairi — 10:25 PM
>
Sondos Alrubaish — 10:27 PM
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import create_access_token
from app.services.facade import facade

api = Namespace("auth", description="Authentication operations")

login_model = api.model("Login", {
    "email": fields.String(required=True, description="User email"),
    "password": fields.String(required=True, description="User password"),
})

token_model = api.model("Token", {
    "access_token": fields.String,
})


@api.route("/login")
class Login(Resource):

    @api.expect(login_model, validate=True)
    @api.marshal_with(token_model)
    def post(self):
        data = api.payload or {}

        email = (data.get("email") or "").strip()
        password = data.get("password")

        if not email or not password:
            api.abort(400, "Missing email or password")

        user = facade.user_repo.get_by_email(email)
        if not user or not user.check_password(password):
            api.abort(401, "Invalid email or password")

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin}
        )

        return {"access_token": access_token}, 200
Nada Al-Mutairi — 10:27 PM
>
Sondos Alrubaish — 10:30 PM
scripts.js
Nada Al-Mutairi — 10:31 PM
>
Sondos Alrubaish — 10:31 PM
// ============================================
// HBnB - Final Clean JavaScript
// ============================================

const API_URL = 'http://127.0.0.1:5000/api/v1';

// ========== Cookie Helpers ==========
function getCookie(name) {
    const value = ; ${document.cookie};
    const parts = value.split(; ${name}=);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function setCookie(name, value, days = 7) {
    const d = new Date();
    d.setTime(d.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = ${name}=${value}; path=/; expires=${d.toUTCString()};
}

function deleteCookie(name) {
    document.cookie = ${name}=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;
}

// ========== Auth Functions ==========
function isAuthenticated() {
    return getCookie('token') !== null;
}

function updateAuthUI() {
    const loginBtn = document.getElementById('login-btn');
    const userMenu = document.getElementById('user-menu');
    const userInitial = document.getElementById('user-initial');
    const email = localStorage.getItem('userEmail');

    if (isAuthenticated() && email) {
        if (loginBtn) loginBtn.style.display = 'none';
        if (userMenu) {
            userMenu.classList.remove('hidden');
            userMenu.classList.add('flex');
        }
        if (userInitial) {
            userInitial.textContent = email.charAt(0).toUpperCase();
        }
    } else {
        if (loginBtn) loginBtn.style.display = 'inline-block';
        if (userMenu) {
            userMenu.classList.add('hidden');
            userMenu.classList.remove('flex');
        }
    }
}

function setupLogout() {
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            deleteCookie('token');

message.txt
5 KB
Nada Al-Mutairi — 10:33 PM
>
Sondos Alrubaish — 10:35 PM
async function displayPlaces() {
    const container = document.getElementById('places-list');
    if (!container) return;
    await displayPlacesInContainer(container, 'price-filter');
}

async function displayPlacesInContainer(container, filterElementId) {
    if (!container) return;

    try {
        const places = await fetchPlaces();

        if (!places || places.length === 0) {
            container.innerHTML = '<div class="col-span-full text-center py-12 text-gray-600">No places available</div>';
            return;
        }

        function renderPlaces(list) {
            container.innerHTML = list.map(p => createPlaceCard(p)).join('');
            setupFavorites();
        }

        renderPlaces(places);

        const filter = document.getElementById(filterElementId);
        if (filter) {
            filter.addEventListener('change', (e) => {
                const val = e.target.value;
                if (val === 'all') {
                    renderPlaces(places);
                } else {
                    const filtered = places.filter(p => p.price_per_night <= Number(val));
                    renderPlaces(filtered);
                }
            });
        }
    } catch (error) {
        container.innerHTML = '<div class="col-span-full text-center py-12 text-red-600">Error loading places</div>';
    }
}
Nada Al-Mutairi — 10:36 PM
>
Sondos Alrubaish — 10:36 PM
function setupFavorites() {
    document.querySelectorAll('.favorite-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();

            const id = btn.dataset.id;
            const icon = btn.querySelector('i');
            const isFav = localStorage.getItem(fav_${id}) === 'true';

            if (isFav) {
                localStorage.removeItem(fav_${id});
                icon.classList.remove('fas');
                icon.classList.add('far');
            } else {
                localStorage.setItem(fav_${id}, 'true');
                icon.classList.remove('far');
                icon.classList.add('fas');
            }
        });
    });
}

// ========== Place Details ==========
async function fetchPlaceDetails(id) {
    try {
        const response = await fetch(${API_URL}/places/${id});
        if (!response.ok) throw new Error('Failed');
        return await response.json();
    } catch (error) {
        return null;
    }
}
Nada Al-Mutairi — 10:37 PM
>
Sondos Alrubaish — 10:37 PM

async function fetchReviews(placeId) {
    console.log(' Fetching reviews for place:', placeId);
    try {
        const url = `${API_URL}/reviews/?place_id=${placeId}`;
        console.log(' Full URL:', url);

message.txt
8 KB
﻿

async function fetchReviews(placeId) {
    console.log(' Fetching reviews for place:', placeId);
    try {
        const url = `${API_URL}/reviews/?place_id=${placeId}`;
        console.log('📡 Full URL:', url);
        
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        console.log('Response status:', response.status);
        console.log('Response headers:', response.headers);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Response error:', errorText);
            return [];
        }
        
        const data = await response.json();
        console.log('Reviews data:', data);
        console.log('Number of reviews:', Array.isArray(data) ? data.length : 'Not an array');
        
        return Array.isArray(data) ? data : [];
    } catch (error) {
        console.error(' Fetch error:', error);
        console.error(' Error type:', error.name);
        console.error(' Error message:', error.message);
        return [];
    }
}

async function displayPlaceDetails() {
    const container = document.getElementById('place-details');
    const reviewsContainer = document.getElementById('reviews-list');
    const addReviewSection = document.getElementById('add-review-section');
    const allPlacesSection = document.getElementById('all-places-section');
    const detailsSection = document.getElementById('place-details-section');
    
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');
    
    // Show all places if no ID
    if (!id && allPlacesSection) {
        allPlacesSection.classList.remove('hidden');
        if (detailsSection) detailsSection.classList.add('hidden');
        
        const allPlacesList = document.getElementById('all-places-list');
        if (allPlacesList) {
            displayPlacesInContainer(allPlacesList, 'price-filter-places');
        }
        return;
    }
    
    // Show place details if ID exists
    if (!container) return;
    
    if (allPlacesSection) allPlacesSection.classList.add('hidden');
    if (detailsSection) detailsSection.classList.remove('hidden');

    try {
        const place = await fetchPlaceDetails(id);
        
        if (!place) {
            container.innerHTML = '<div class="text-center py-12 text-red-600">Place not found</div>';
            return;
        }

        // Display place details
        container.innerHTML = `
            <div class="bg-white rounded-xl shadow-md overflow-hidden">
                <img src="${getPlaceImage(place.id)}" class="w-full h-96 object-cover" alt="${place.title}">
                <div class="p-6">
                    <h1 class="text-3xl font-bold mb-4">${place.title}</h1>
                    <p class="text-gray-700 mb-4">${place.description || 'No description available'}</p>
                    
                    <div class="flex flex-wrap gap-4 mb-6">
                        ${getAmenitiesIcons(place.amenities)}
                    </div>
                    
                    <div class="text-3xl font-bold text-purple-600">
                        ${place.price_per_night} SAR <span class="text-lg text-gray-600 font-normal">/ night</span>
                    </div>
                </div>
            </div>
        `;

        // Fetch and display reviews
        const reviews = await fetchReviews(id);

        if (reviewsContainer) {
            const reviewsSection = reviewsContainer.closest('#reviews-section');
            if (reviewsSection) {
                const reviewsTitle = reviewsSection.querySelector('h2');
                if (reviewsTitle) {
                    reviewsTitle.textContent = `Reviews (${reviews.length})`;
                }
            }

            if (reviews && reviews.length > 0) {
                reviewsContainer.innerHTML = reviews.map(r => {
                    const userName = r.user?.first_name || 'Anonymous';
                    const userInitial = userName.charAt(0).toUpperCase();
                    const rating = r.rating || 0;
                    const reviewText = r.text || 'No comment';
                    
                    return `
                        <div class="bg-white p-6 rounded-xl shadow-md mb-4 border border-gray-200">
                            <div class="flex items-center justify-between mb-3">
                                <div class="flex items-center gap-3">
                                    <div class="w-12 h-12 bg-gradient-to-br from-purple-600 to-purple-800 rounded-full flex items-center justify-center text-white font-bold text-lg">
                                        ${userInitial}
                                    </div>
                                    <div>
                                        <div class="font-semibold text-gray-900">${userName}</div>
                                        <div class="text-sm text-gray-500">${new Date(r.created_at || Date.now()).toLocaleDateString()}</div>
                                    </div>
                                </div>
                                <div class="flex items-center gap-1 text-yellow-500 text-xl">
                                    ${'⭐'.repeat(rating)}
                                </div>
                            </div>
                            <p class="text-gray-700 leading-relaxed">${reviewText}</p>
                        </div>
                    `;
                }).join('');
            } else {
                reviewsContainer.innerHTML = `
                    <div class="bg-gray-50 border-2 border-dashed border-gray-300 rounded-xl p-8 text-center">
                        <div class="text-4xl mb-3">💬</div>
                        <p class="text-gray-600 font-semibold mb-2">No reviews yet</p>
                        <p class="text-gray-500 text-sm">Be the first to share your experience!</p>
                    </div>
                `;
            }
        }

        // Setup review form for authenticated users
        if (addReviewSection) {
            if (isAuthenticated()) {
                addReviewSection.classList.remove('hidden');
                
                // Setup star rating and form (order is important!)
                setTimeout(() => {
                    setupReviewForm(id);
                    setupStarRating();
                }, 100);
            } else {
                addReviewSection.innerHTML = `
                    <div class="bg-blue-50 border border-blue-200 rounded-xl p-6 text-center">
                        <p class="text-blue-800 font-semibold mb-3">Want to leave a review?</p>
                        <a href="login.html" class="inline-block px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition font-semibold">
                            Sign in to review
                        </a>
                    </div>
                `;
                addReviewSection.classList.remove('hidden');
            }
        }
    } catch (error) {
        console.error(' Error:', error);
        container.innerHTML = '<div class="text-center py-12 text-red-600">Error loading details</div>';
    }
}
