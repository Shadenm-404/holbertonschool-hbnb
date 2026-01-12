# HBnB – Part 2: Business Logic Layer

This part of the **HBnB** project focuses on implementing the **Business Logic Layer (BL)** and exposing it through **RESTful API endpoints**, following the architecture defined in **Part 1**.
The project applies the **Facade Design Pattern** to centralize all business operations and enforce a clear separation between the Presentation Layer, Business Logic Layer, and Data Access Layer.  
An **in-memory persistence mechanism** is used to manage entities and enforce business rules such as data validation and entity relationships.
This stage establishes a clean, scalable, and maintainable backend foundation.

---

## Business Logic Responsibilities

The Business Logic Layer is responsible for:

- Validating input data before object creation or update  
- Enforcing business rules and application constraints  
- Coordinating interactions between the API layer and the repository layer  
- Preventing invalid operations (e.g. creating a Place with a non-existing owner)

By centralizing these responsibilities, the BL ensures consistent and reliable application behavior regardless of how the API is accessed.

---

## Architecture Overview

The application follows a layered architecture with clear separation of concerns:

- The **API Layer** handles HTTP requests and responses.
- The **Business Logic Layer** enforces validation, business rules, and entity relationships.
- The **Repository Layer** abstracts data storage and access.
- All communication between layers is coordinated through the **Facade**.

This design improves maintainability, scalability, and testability.

---

## Facade Pattern

All business operations in the application are routed through a single access point known as the **Facade**.

The API layer never interacts directly with models or repositories.  
Instead, validation, entity creation, and data coordination are centralized within the Facade, reducing coupling between layers and resulting in a cleaner and more maintainable codebase.

---

## Repository Layer

The Repository Layer acts as an abstraction over data storage.

In this implementation, persistence is simulated using in-memory Python data structures.  
Data is reset when the server restarts, which aligns with the scope of this project phase and supports rapid development and testing.

---

## Project Objectives

By the end of this project, the following objectives are achieved:

### 1. Project Structure Setup
- Organize the project using a modular architecture following Python and Flask best practices.
- Separate Presentation, Business Logic, and Data Access layers.

### 2. Business Logic Implementation
- Implement core domain entities: User, Place, Review, and Amenity.
- Define relationships and constraints between entities.
- Apply the Facade Pattern to simplify communication between layers.

### 3. RESTful API Development
- Implement CRUD operations for Users, Places, Reviews, and Amenities.
- Use **Flask-RESTX** to define and document the API.
- Serialize related entity data when required (e.g. including owner information when retrieving a Place).

### 4. API Testing and Validation
- Verify correct behavior for valid and invalid requests.
- Test edge cases such as missing fields and non-existent IDs.
- Ensure consistent JSON responses and correct HTTP status codes.

---

## Project Structure

```
part2/
└── hbnb/
    ├── app/
    │   ├── api/
    │   │   └── __init__.py
    │   │   └── v1/
    │   │       ├── users.py
    │   │       ├── places.py
    │   │       ├── review.py
    │   │       ├── amenities.py
    │   │       └── __init__.py
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── BaseModel.py
    │   │   ├── user.py
    │   │   ├── place.py
    │   │   ├── amenity.py
    │   │   ├── review.py
    │   │   └── validation.py
    │   ├── repositories/
    │   │   └── in_memory_repository.py
    │   │   └── __init__.py
    │   ├── services/
    │   │   └── facade.py
    │   └── persistence
    │   │   └── __init__.py
    │   │   └── repository.py
    │   └── __init__.py
    ├── run.py
    ├── README.md
    ├── config.py
    ├── requirements.txt
    ├── simple_test_report.md
    ├── test_models.py
    ├── test_users.sh
    └── test_amenities_places.sh
```
---
## Files Description

| Layer | File | Description |
|------|------|-------------|
| API | `users.py` | User creation, retrieval, and update REST endpoints |
| API | `places.py` | Place creation and retrieval REST endpoints |
| API | `amenities.py` | Amenity creation, retrieval, and update REST endpoints |
| Models | `BaseModel.py` | Base entity providing `id`, `created_at`, and `updated_at` |
| Models | `user.py` | User entity definition |
| Models | `place.py` | Place entity with owner validation |
| Models | `amenity.py` | Amenity entity definition |
| Models | `review.py` | Review entity definition linked to users and places |
| Models | `validation.py` | Centralized validation and input checking logic |
| Services | `facade.py` | Central Business Logic Layer implementing the Facade Pattern |
| Repository | `in_memory_repository.py` | In-memory data storage abstraction |
| Testing | `test_users.sh` | Shell script testing user-related endpoints (Tasks 1–3) |
| Testing | `test_amenities_places.sh` | Shell script testing amenity and place endpoints (Tasks 4–6) |

---
## Supported API Endpoints

The application exposes RESTful endpoints that allow interaction with core entities such as Users, Places, and Amenities.  
All endpoints follow REST conventions and return structured JSON responses.  
Swagger documentation is provided using Flask-RESTX for interactive API exploration.

---
## HTTP Status Codes

| Status Code | Description |
|------------|-------------|
| 200 | Successful retrieval or update operation |
| 201 | Resource created successfully |
| 400 | Invalid or missing input data |
| 404 | Requested resource not found |

---

## Requirements File (requirements.txt)

The ```requirements.txt``` file contains all Python dependencies required to run the application correctly, including Flask and Flask-RESTX.
Install dependencies using:

```
pip install -r requirements.txt
```

### Running the Application
Start the Flask server locally:

``` 
python3 run.py
```

The project includes two shell scripts for automated API testing:

- `test_users.sh` tests functionality implemented in Tasks 1, 2, and 3 (User operations).
- `test_amenities_places.sh` tests functionality implemented in Tasks 4, 5, and 6 (Amenity and Place operations).

--- 
### Execute the scripts as follows:
```
./test_users.sh
./test_amenities_places.sh
```

### Test Script Behavior

Each test script sends a sequence of HTTP requests that:

1. Create resources using POST requests
2. Retrieve resources using GET requests
3. Update resources using PUT requests
4. Trigger invalid operations to verify error handling

**All requests include the required header:**

``Content-Type: application/json``

--- 
## Expected Output
**When the test scripts are executed, the terminal displays:**

○ HTTP response headers

○ HTTP status codes (e.g. 200, 201, 400, 404)

○ JSON response bodies returned by the API

**A successful test execution is indicated by:**

○ Correct HTTP status codes

○ Valid JSON responses

○ Error messages appearing only for intentionally invalid requests

○ No crashes or unhandled exceptions

---

## Summary
This project implements the Business Logic Layer of the HBnB application using a clean, layered architecture.
Business rules are centralized through the Facade Pattern, with in-memory persistence and structured testing to ensure correctness, reliability, and maintainability.

