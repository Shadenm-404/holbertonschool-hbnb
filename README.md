# Holbertonschool-Hbnb Project

HBnB Evolution is a technical documentation project focused on designing the architecture of a simplified Airbnb-like application.  
The objective of this project is to define a clear system structure using a layered architecture approach before moving into the implementation phase.  
This documentation serves as a foundational blueprint that explains how different components of the system are organized and how they interact with each other.  
Emphasis is placed on UML modeling, clean architectural design, and separation of concerns.

---
# Part 1 – System Architecture and Design

## Package Diagram

This section presents the High-Level Package Diagram for the HBnB Evolution application.  
The diagram illustrates the overall system architecture based on a three-layer structure: Presentation Layer, Business Logic Layer, and Persistence Layer.  
It highlights how the layers interact with each other through the Facade Pattern, providing a clear separation of concerns and simplifying communication between components.  
This diagram offers a conceptual overview of the system without including implementation or database-specific details.

<img src="part1/hbnb_package_diagram.png" width="200">

---

## Class Diagram

This section documents the class diagram for the Business Logic layer of the HBnB application.  
The diagram describes the core domain entities, their attributes, methods, and the relationships that govern their interactions.  
It focuses on modeling the fundamental business rules and behaviors independently of presentation or persistence concerns, ensuring a clean and maintainable design.

<img src="part1/Hbnb_Class_Diagram.png" width="1000">

---

## Sequence Diagrams

This section presents the sequence diagrams for the HBnB Evolution application.  
These diagrams illustrate how the Presentation Layer, Business Logic Layer, and Persistence Layer interact to handle key user operations.  
Each sequence diagram represents a specific API use case and demonstrates the flow of requests and responses across the system layers, highlighting how business logic is processed and how data is stored or retrieved.


<p align="left">
<img src="part1/Sequence Diagrams User Registration.png" width="450">
<img src="part1/Sequence Diagrams Place Creation.png" width="450">
<img src="part1/Sequence Diagrams Review Submission.png" width="450">
<img src="part1/Sequence Diagrams Fetching a List of Place.png" width="450">
</p>

--- 

# Part 2 – Business Logic and API Implementation

This part of the **HBnB** project focuses on implementing the **Business Logic Layer (BL)** and exposing application functionality through **RESTful API endpoints**.  
The implementation follows the architecture previously defined and applies the **Facade Design Pattern** to centralize business operations and enforce a clean separation between layers.

An **in-memory persistence mechanism** is used to manage entities and apply business rules such as data validation and entity relationships.  
This stage delivers a functional and maintainable backend foundation.

---

## Business Logic Overview

The Business Logic Layer is responsible for validating input data, enforcing business rules, coordinating interactions between the API and repository layers, and preventing invalid operations such as creating entities with non-existent relationships.

All business behavior is centralized to ensure consistent and reliable application behavior regardless of how the API is accessed.

---

## Architecture and Design

The application follows a layered architecture consisting of:
- An API Layer for handling HTTP requests and responses
- A Business Logic Layer for validation and rule enforcement
- A Repository Layer for abstracting data storage

All communication between layers is coordinated through the **Facade**, improving maintainability, scalability, and testability.

---

## Persistence Strategy

Data persistence in this phase is simulated using in-memory Python data structures.  
This approach allows the application to focus on enforcing business logic, validation rules, and entity relationships without introducing database complexity.

All stored data is reset when the server restarts, which is an intentional design choice aligned with the scope of this project stage.  
This strategy supports rapid development, easier debugging, and clear validation of application behavior before integrating permanent storage solutions in future phases.

---

## API Implementation

RESTful API endpoints are implemented using **Flask** and **Flask-RESTX**, providing a clean and structured interface for interacting with the application.  
The API enables operations on core entities such as Users, Places, Amenities, and Reviews using standard HTTP methods and JSON payloads.

Flask-RESTX is also used to automatically generate **Swagger documentation**, offering an interactive view of available endpoints, request formats, and response structures.  
This improves usability, consistency, and clarity for both development and testing.

---

## Testing and Validation

API functionality is validated using automated shell scripts that simulate real client requests through the `curl` command-line tool.  
These scripts are designed to test both successful and invalid scenarios to ensure correct behavior under different conditions.

- `test_users.sh` validates **Tasks 1–3**, covering user creation, retrieval, and update operations.
- `test_amenities_places.sh` validates **Tasks 4–6**, covering amenity operations and place creation with owner validation.

Testing verifies:
- Correct enforcement of business rules
- Proper handling of invalid input and non-existent resources
- Accurate HTTP status codes
- Consistent and structured JSON responses

---

## Summary

Part 2 delivers a functional backend implementation that transforms architectural design into executable code.  
By centralizing business logic through the Facade Pattern, enforcing validation rules, exposing RESTful APIs, and validating behavior through structured testing, this stage provides a solid and maintainable foundation for future enhancements such as persistent storage and authentication.

---

# Part 3 – Database Integration and Persistence

In Part 3, HBnB moves from temporary in-memory storage to a **relational database-backed system**, introducing persistent storage, enforced relationships, and scalable backend architecture. SQLAlchemy ORM maps Python models to tables, manages transactions, and enforces entity relationships, while preserving the existing API and layered design.

---

## Technologies

| Technology          | Purpose                                                                                                   |
|--------------------|-----------------------------------------------------------------------------------------------------------|
| Python 3            | The main programming language used to implement the HBnB backend logic, handling API requests, data processing, and integration with the database. |
| Flask / Flask-RESTX | Provides the framework for building RESTful API endpoints, request/response handling, and automatic Swagger documentation for interactive testing. |
| SQLAlchemy ORM      | Maps Python models to database tables, manages sessions and transactions, enforces relationships between entities, and ensures data consistency. |
| SQLite              | Lightweight relational database used to store persistent data for Users, Places, Reviews, and Amenities, supporting queries, constraints, and relationships. |
| JWT Authentication  | Secures user access by issuing JSON Web Tokens, allowing authenticated interactions with protected endpoints while keeping credentials safe. |

---

## Key Updates from Part 2
| Aspect                | Part 2 (In-memory)                                                                                     | Part 3 (Database)                                                                                                      |
|----------------------|-------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| Data Storage          | Data was stored temporarily in Python objects and dictionaries, disappearing when the server restarted. | Data is now stored permanently in a relational database, ensuring that all entities persist across server restarts.  |
| Persistence           | No long-term storage; any restart cleared all Users, Places, Reviews, and Amenities.                  | Full persistence using SQLAlchemy ORM ensures durable storage and long-term availability of all data.                  |
| Relationships         | Relationships between entities (like Place belonging to User) were enforced only in code logic, which could be bypassed. | Relationships are now enforced at the database level with foreign keys, ensuring referential integrity and automatic consistency. |
| Transactions          | No transaction management; changes were applied immediately without rollback capability.              | Transactions are managed via SQLAlchemy sessions, allowing commit/rollback to maintain data integrity in case of errors. |
| Authentication        | User credentials were validated locally, without persistent storage.                                  | User validation now queries the database directly, with JWT tokens issued for secure authentication and protected access. |
| Scalability / Reliability | Limited scalability; data loss on server restart, prone to inconsistency.                             | Highly scalable and reliable; persistent storage, enforced relationships, and proper transaction management support production-level usage. |

---


## Database Design – ER Diagram

The ER Diagram below illustrates how **Users, Places, Reviews, and Amenities** are related, including primary keys, foreign keys, and association tables.

<img src="part3/ER_diagram.png" width="800">

---
## Summary

Part 3 completes the transition to a **persistent and scalable backend**, ensuring data integrity, secure authentication, and durable storage.  
HBnB is now ready for future features, advanced extensions, and production-level deployment.

---
## Authors

### Shaden Majed Alalwani  
Riyadh, Saudi Arabia  
Student at Holberton Schools  
GitHub: https://github.com/Shadenm-404  

### Nada Ghannam Al-Mutairi  
Riyadh, Saudi Arabia  
Student at Holberton Schools  
GitHub: https://github.com/NadaGhannam25  

### Sondos Saleh Alrubaish  
Riyadh, Saudi Arabia  
Student at Holberton Schools  
GitHub: https://github.com/sondos04  



