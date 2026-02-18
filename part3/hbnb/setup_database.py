#!/usr/bin/env python3
"""
HBnB - Database Setup Script
Simple and guaranteed to work!
"""

import os
import sys

# Add backend to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from config import DevelopmentConfig
from app.extensions import db, bcrypt
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

def main():
    """Setup database with sample data"""
    
    print("\n" + "="*60)
    print("HBnB Database Setup")
    print("="*60)
    
    # Create app
    app = create_app(DevelopmentConfig)
    
    with app.app_context():
        try:
            # Step 1: Drop all tables
            print("\nDropping existing tables...")
            db.drop_all()
            print("Tables dropped")
            
            # Step 2: Create all tables
            print("\nCreating fresh tables...")
            db.create_all()
            print("Tables created")
            
            # Step 3: Create Users
            print("\Creating users...")
            
            admin = User(
                email='admin@hbnb.com',
                password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
                first_name='Admin',
                last_name='User',
                is_admin=True
            )
            db.session.add(admin)
            
            sondos = User(
                email='sondos@hbnb.com',
                password=bcrypt.generate_password_hash('sondos123').decode('utf-8'),
                first_name='Sondos',
                last_name='alrubaish',
                is_admin=False
            )
            db.session.add(sondos)
            
            shaden = User(
                email='shaden@hbnb.com',
                password=bcrypt.generate_password_hash('shaden123').decode('utf-8'),
                first_name='Shaden',
                last_name='Alalwani',
                is_admin=False
            )
            db.session.add(shaden)
                        
            nada  = User(
                email='nada@hbnb.com',
                password=bcrypt.generate_password_hash('nada123').decode('utf-8'),
                first_name='Nada',
                last_name='Almutairi',
                is_admin=False
            )
            db.session.add(nada)
            
            saleh  = User(
                email='saleh@hbnb.com',
                password=bcrypt.generate_password_hash('saleh123').decode('utf-8'),
                first_name='Saleh',
                last_name='Almutairi',
                is_admin=False
            )
            db.session.add(saleh)
            
            db.session.commit()
            print(f"Created {User.query.count()} users")
            
            # Step 4: Create Amenities
            print("\nCreating amenities...")
            
            amenities_list = ['WiFi', 'Pool', 'Parking', 'Breakfast', 'Gym', 'AC']
            amenities = []
            
            for name in amenities_list:
                amenity = Amenity(name=name)
                db.session.add(amenity)
                amenities.append(amenity)
            
            db.session.commit()
            print(f"Created {Amenity.query.count()} amenities")
            
            # Step 5: Create Places
            print("\nCreating places...")
            
            # Reload to get IDs
            wifi = Amenity.query.filter_by(name='WiFi').first()
            pool = Amenity.query.filter_by(name='Pool').first()
            parking = Amenity.query.filter_by(name='Parking').first()
            breakfast = Amenity.query.filter_by(name='Breakfast').first()
            gym = Amenity.query.filter_by(name='Gym').first()
            ac = Amenity.query.filter_by(name='AC').first()
            
            place1 = Place(
                title='Luxury Resort Riyadh',
                description='A luxury resort in the heart of Riyadh with all modern amenities',
                price_per_night=100.0,
                latitude=24.7136,
                longitude=46.6753,
                owner_id=admin.id
            )
            if wifi: place1.amenities.append(wifi)
            if pool: place1.amenities.append(pool)
            if parking: place1.amenities.append(parking)
            if breakfast: place1.amenities.append(breakfast)
            db.session.add(place1)
            
            place2 = Place(
                title='Modern City Hotel',
                description='A modern hotel in the city center with a great view',
                price_per_night=100.0,
                latitude=24.7242,
                longitude=46.6385,
                owner_id=admin.id
            )
            if wifi: place2.amenities.append(wifi)
            if parking: place2.amenities.append(parking)
            if gym: place2.amenities.append(gym)
            db.session.add(place2)
            
            place3 = Place(
                title='Cozy Downtown Apartment',
                description='Comfortable apartment in the city center, suitable for families',
                price_per_night=50.0,
                latitude=24.7353,
                longitude=46.5752,
                owner_id=admin.id
            )
            if wifi: place3.amenities.append(wifi)
            if ac: place3.amenities.append(ac)
            db.session.add(place3)
            
            place4 = Place(
                title='Family Villa with Garden',
                description='Luxury family villa with a spacious garden',
                price_per_night=10.0,
                latitude=24.6877,
                longitude=46.7219,
                owner_id=admin.id
            )
            if wifi: place4.amenities.append(wifi)
            if pool: place4.amenities.append(pool)
            if parking: place4.amenities.append(parking)
            db.session.add(place4)
            
            place5 = Place(
                title='Budget Room Near Metro',
                description='An economy room close to the meter.',
                price_per_night=90.0,
                latitude=24.7500,
                longitude=46.6900,
                owner_id=admin.id
            )
            if wifi: place5.amenities.append(wifi)
            db.session.add(place5)
            
            db.session.commit()
            print(f"Created {Place.query.count()} places")
            
            # Step 6: Create Reviews
            print("\nCreating reviews...")
            
            reviews_data = [
                (place1.id, saleh.id, 5, 'مكان رائع جداً! أنصح الجميع بزيارته'),
                (place1.id, nada.id, 4, 'تجربة ممتازة، المكان نظيف والخدمة رائعة'),
                (place2.id, saleh.id, 4, 'فندق جميل وموقع مميز'),
                (place3.id, nada.id, 5, 'شقة مريحة جداً وبسعر معقول'),
                (place4.id, saleh.id, 5, 'فيلا فخمة! استمتعنا كثيراً بالحديقة'),
            ]
            
            for place_id, user_id, rating, text in reviews_data:
                review = Review(
                    place_id=place_id,
                    user_id=user_id,
                    rating=rating,
                    text=text
                )
                db.session.add(review)
            
            db.session.commit()
            print(f"Created {Review.query.count()} reviews")
            
            # Success Summary
            print("\n" + "="*60)
            print("Database setup completed successfully!")
            print("="*60)
            
            print("\nLogin Credentials:")
            print("-" * 60)
            print("  admin@hbnb.com     | admin123     | (Admin)")
            print("  sondos@hbnb.com    | sondos123    | (User)")
            print("  shaden@hbnb.com    | shaden123    | (User)")
            print("  nada@hbnb.com      | nada123      | (User)")
            print("  saleh@hbnb.com     | saleh123     | (User)")
            print("-" * 60)
            
            print("\nDatabase Summary:")
            print(f"Users:      {User.query.count()}")
            print(f"Places:     {Place.query.count()}")
            print(f"Reviews:    {Review.query.count()}")
            print(f"Amenities: {Amenity.query.count()}")
            
            
            print("\n" + "="*60 + "\n")
            
            return 0
            
        except Exception as e:
            print(f"\nError occurred: {e}")
            import traceback
            traceback.print_exc()
            return 1

if __name__ == '__main__':
    exit(main())
