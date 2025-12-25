# Holbertonschool-Hbnb Project – Part 1

HBnB Evolution is a technical documentation project focused on designing the architecture of a simplified Airbnb-like application.
The objective of this project is to define a clear system structure using a layered architecture approach prior to implementation.
This documentation serves as a foundational blueprint that explains how different system components are organized and how they interact.
The project emphasizes UML modeling, clean architectural design, and separation of concerns.

---

## High-Level Package Diagram

This section presents the high-level package diagram for the HBnB Evolution application.
The diagram illustrates the overall system architecture using a three-layer structure: Presentation Layer, Business Logic Layer, and Persistence Layer.
It demonstrates how these layers communicate through the Facade Pattern, ensuring a clear separation of responsibilities.
The diagram provides a conceptual overview and does not include implementation or database-specific details.

![HBnB High-Level Package Diagram](hbnb_package_diagram.png)

---

## Business Logic Layer – Class Diagram

This section documents the class diagram of the Business Logic layer for the HBnB application.
The diagram describes the core domain entities, their attributes, operations, and the relationships governing their interactions.
It focuses on modeling fundamental business rules and behaviors independently of presentation and persistence concerns.

![HBnB Business Logic Class Diagram](Hbnb_Class_Diagram.png)

---

### 1. Overview of the Business Logic Class Diagram

The Business Logic class diagram provides a structured view of the core domain entities, their attributes, methods, and relationships.
The design follows object-oriented principles to ensure separation of concerns, reusability, and maintainability.
All domain entities inherit from a common base class to enforce consistency across the model.

---

### 2. BaseEntity Class

The BaseEntity class serves as an abstract foundational class for all business entities within the system.
It centralizes common attributes and shared behaviors, promoting code reuse and consistency.

**Attributes**
- `id (UUID)`: Unique identifier for each entity instance
- `created_at (DateTime)`: Timestamp of entity creation
- `updated_at (DateTime)`: Timestamp of the last update

**Methods**
- `save()`: Persists the entity state
- `update()`: Updates entity attributes
- `delete()`: Removes the entity from the system

All core entities (`User`, `Place`, `Review`, and `Amenity`) inherit from `BaseEntity`, ensuring uniform lifecycle management within the Business Logic layer.

---

### 3. User Entity

The User entity represents registered users of the HBnB platform and acts as a primary system actor.
Users can manage places and submit reviews.

**Attributes**
- `first_name (String)`
- `last_name (String)`
- `email (String)`
- `password (String)`
- `is_admin (Boolean)`: Indicates administrative privileges

**Methods**
- `register()`: Handles user registration logic
- `update_profile()`: Updates user information
- `delete_account()`: Removes the user account

**Relationships**
- **User – Place (One-to-Many):** One user may own multiple places
- **User – Review (One-to-Many):** One user may submit multiple reviews

---

### 4. Place Entity

The Place entity represents accommodations or listings available on the platform.
It encapsulates location, pricing, and descriptive details.

**Attributes**
- `title (String)`
- `description (String)`
- `price (Float)`
- `latitude (Float)`
- `longitude (Float)`

**Methods**
- `create()`: Creates a new place listing
- `update()`: Updates place details
- `delete()`: Removes a place listing
- `list_amenities()`: Retrieves associated amenities

**Relationships**
- **Place – User (Many-to-One):** Each place is owned by one user
- **Place – Review (One-to-Many):** A place may have multiple reviews
- **Place – Amenity (Many-to-Many):** Places may offer multiple amenities

---

### 5. Review Entity

The Review entity models user feedback and ratings associated with a specific place.
It contributes to quality assessment and user trust.

**Attributes**
- `rating (Integer)`
- `comment (String)`

**Methods**
- `create()`: Submits a new review
- `update()`: Modifies an existing review
- `delete()`: Removes a review

**Relationships**
- Each review is associated with one user and one place

---

### 6. Amenity Entity

The Amenity entity represents optional features or services associated with places, such as Wi-Fi or parking.

**Attributes**
- `name (String)`
- `description (String)`

**Methods**
- `create()`: Adds a new amenity
- `update()`: Updates amenity details
- `delete()`: Removes an amenity

**Relationships**
- **Amenity – Place (Many-to-Many):** Amenities may be associated with multiple places

---

## Sequence Diagrams

This section presents the sequence diagrams for the HBnB Evolution application.  
These diagrams illustrate how the Presentation Layer, Business Logic Layer, and Persistence Layer interact to handle key user operations.  
Each sequence diagram represents a specific API use case and demonstrates the flow of requests and responses across the system layers.

<p align="left">
  <img src="Sequence Diagrams User Registration.png" width="450">
  <img src="Sequence Diagrams Place Creation.png" width="450">
  <img src="Sequence Diagrams Review Submission.png" width="450">
  <img src="Sequence Diagrams Fetching a List of Place.png" width="450">
</p>


---

### Summary

The diagrams documented in this section provide a comprehensive and precise representation of the HBnB system architecture and Business Logic layer.
They serve as a reliable blueprint for future implementation, ensuring scalability, maintainability, and a clear translation of business requirements into system design.
