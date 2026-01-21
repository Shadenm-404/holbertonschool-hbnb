# HBnB – part3 : Database Integration and Persistence

This project represents **Part 3** of the HBnB (Holberton Bed & Breakfast) application.  
In this phase, the system transitions from **in-memory data storage** to a **database-backed persistence layer** using a relational database.

The primary goal of this part is to introduce permanent data storage while preserving the existing API behavior and maintaining a clean, scalable architecture.

---

## Objectives

The objectives of this phase are to:

- Replace in-memory persistence with database storage
- Integrate SQLAlchemy as the Object Relational Mapper (ORM)
- Implement proper session and transaction management
- Maintain clear separation between application layers
- Ensure data consistency and long-term persistence

---

## Architecture 

The application follows a layered architecture with clear responsibility boundaries:

```
Client
↓
API Layer (Flask / Flask-RESTX)
↓
Business Logic Layer (Facade Pattern)
↓
Persistence Layer (SQLAlchemy + Relational Database)
```


This structure improves maintainability, scalability, and testability.

---

## Project Structure - Actual Implementation

The following directory structure reflects the **actual file layout used in Part 3**,
based strictly on the implemented project files.

```
part3/
└── hbnb/
│   ├── app/
│   │   ├── api/
│   │   │   └── init.py
│   │   │   └── v1/
│   │   │       ├── users.py
│   │   │       ├── places.py
│   │   │       ├── reviews.py
│   │   │       ├── amenities.py
│   │   │       ├── auth.py
│   │   │       └── init.py
│   │   ├── models/
│   │   │   ├── init.py
│   │   │   ├── base_model.py
│   │   │   ├── user.py
│   │   │   ├── place.py
│   │   │   ├── amenity.py
│   │   │   └── review.py
│   │   ├── db/
│   │   │   ├── database.py
│   │   │   └── session.py
│   │   ├── repositories/
│   │   │   ├── amenity_repository.py 
│   │   │   ├── place_repository.py
│   │   │   ├── review_repository.py
│   │   │   ├── sqlalchemy_repository.py
│   │   │   ├── user_repository.py
│   │   │   └── init.py
│   │   ├── services/
│   │   │   ├── init.py
│   │   │   └── facade.py
│   │   └── init.py
│   ├── sql/
│   │   ├── create_tables.sql
│   │   ├── insert_admin.sql
│   │   └── insert_amenities.sql
│   ├── run.py
│   ├── config.py
│   ├── requirements.txt
│   ├── test_amenities.sh
│   ├── test_places_reviews.sh
│   └── README.md
│
└── README.md
```
---
## SQL and Database Files

- `repositories/sqlalchemy_repository.py`

  Handles database operations using SQLAlchemy.
  It is responsible for saving, retrieving, and updating data in the database, replacing in-memory storage with persistent SQL-based storage.

- `api/v1/auth.py`

  Manages authentication-related API endpoints.
  It verifies user credentials using stored database data and prepares the application for secure access.

- `sql/create_tables.sql`

  Contains SQL statements used to create the database tables and define the schema structure.

- `sql/insert_admin.sql`

  Provides initial SQL data for the database, such as inserting a default or administrative user.

- `sql/insert_amenities.sql`

  Provides initial SQL data for the database, such as inserting predefined amenity records.

- `Database Integration (db)`

  The database layer is responsible for establishing the connection, managing sessions, and ensuring data is stored persistently.
  It acts as the foundation that links the application logic with the SQL database.

---

## Table 1: API Layer (v1) – Changes & Responsibilities
| File | Entity | Endpoints | Part 3 Updates | Responsibility |
|------|--------|-----------|----------------|----------------|
| api/v1/places.py | Place | POST /places | Connected place creation to database via Facade | Handle place creation requests |
|  |  | GET /places | Retrieve places from database instead of memory | List all places |
|  |  | GET /places/<id> | Fetch a specific place from database | Retrieve a single place |
| api/v1/reviews.py | Review | POST /reviews | Added duplicate review prevention logic | Create reviews with validation |
|  |  | GET /reviews | Read reviews from database | List all reviews |
|  |  | GET /reviews/<id> | Retrieve a review by ID | Fetch a single review |
| api/v1/users.py | User | POST /users | Persist users in database | Create user accounts |
|  |  | GET /users | Retrieve users from database | List users |
| api/v1/auth.py | Auth | POST /auth/login | Authenticate users using database data | Issue JWT access tokens |
| api/v1/amenities.py | Amenity | POST /amenities | Store amenities in database instead of memory | Create amenities (admin-level) |
|  |  | GET /amenities | Retrieve amenities from database | List all amenities |
|  |  | GET /amenities/<id> | Fetch a specific amenity by ID | Retrieve a single amenity |

---
## Table 2: Models Layer – SQLAlchemy ORM Updates
| File | Model | Table | Core Fields | Relationships | Part 3 Enhancements |
|------|-------|-------|-------------|---------------|---------------------|
| models/base_model.py | BaseModel | — | id, created_at, updated_at | — | Integrated with SQLAlchemy declarative base |
| models/user.py | User | users | email, password, is_admin | places, reviews | Added ORM relationships and persistent storage |
| models/place.py | Place | places | title, owner_id, price_per_night | owner, reviews | Added foreign key to User and ORM relationships |
| models/review.py | Review | reviews | text, rating, user_id, place_id | user, place | Added foreign keys and unique constraint to prevent duplicates |
| models/amenity.py | Amenity | amenities | name | places | Persisted amenities using SQLAlchemy ORM |

---
## Notes
- The API layer is responsible only for request handling and response formatting.
- Business rules and validation logic are centralized in the Facade layer.
- All entity relationships are defined exclusively in the Models layer.
- Duplicate review prevention is enforced at both:
- Application level (Facade validation)
- Database level (unique constraint).
---

## Testing
*The project can be tested using:*

- Manual API testing with `curl`
- Automated test scripts located in the `tests/` directory

**Example request:**
```
curl -X POST http://127.0.0.1:5000/api/v1/users \
-H "Content-Type: application/json" \
-d '{"email":"test@mail.com","password":"1234"}'
```

## How to Run the Project

1- **Install dependencies:**
```
pip install -r requirements.txt
```
2- **Start the application:**
```
python3 run.py
```

3- **Access the API:**
```
http://127.0.0.1:5000/api/v1/
```
---
## Test Results

This section presents the results of the executed tests for the main system entities.  
All tests were performed after completing the database integration in Part 3 to ensure correct persistence, validation, and API behavior.

---
### 1. User Tests

<img src="https://github.com/user-attachments/assets/590dbbef-0db9-4d0b-8b96-3e8cc10e0fb8" alt="User Test 1" width="450">

<img src="https://github.com/user-attachments/assets/531e4c22-571e-4ed9-95a4-986e029aa9ac" alt="User Test 2" width="450">

---

### 2. Place & Review Tests

<img src="https://github.com/user-attachments/assets/16eaa084-f50d-4793-9409-5aea3a640782" alt="Place Test" width="450">

<img src="https://github.com/user-attachments/assets/a51d2c2f-7fad-4a54-81ca-d280ec194493" alt="Review Test" width="450">

---

### 3. Amenity Tests

<img src="https://github.com/user-attachments/assets/cc2dfa3e-6a3a-4daf-8196-cacf69ed7ba2" alt="Amenity Test 1" width="450">

<img src="https://github.com/user-attachments/assets/e8c6128f-0dba-4e39-9f38-3483b2f26cf2" alt="Amenity Test 2" width="450">

---

### Key Improvements from Part 2

- Introduction of database-backed persistence
- SQLAlchemy ORM integration
- Improved separation of concerns
- Enhanced scalability and maintainability
---

## Conclusion

Part 3 of the HBnB project successfully transitions the application from in-memory storage to a fully persistent, database-backed architecture.
By integrating SQLAlchemy, implementing a clean repository and facade pattern, and enforcing proper relationships and business rules, the system achieves improved scalability, reliability, and maintainability.
This phase establishes a solid foundation for future extensions, advanced features, and production-ready deployment.

