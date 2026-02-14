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
