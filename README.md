# holbertonschool-hbnb Project

HBnB Evolution is a technical documentation project focused on designing the architecture of a simplified Airbnb-like application.  
The objective of this project is to define a clear system structure using a layered architecture approach before moving into the implementation phase.  
This documentation serves as a foundational blueprint that explains how different components of the system are organized and how they interact with each other.  
Emphasis is placed on UML modeling, clean architectural design, and separation of concerns.

---

## High-Level Package Diagram

The diagram below presents the **High-Level Package Diagram** for the HBnB Evolution application.  
It illustrates the three main layers of the system: **Presentation Layer**, **Business Logic Layer**, and **Persistence Layer**, and demonstrates how these layers communicate through the **Facade Pattern**.  
This diagram provides a high-level architectural overview without including implementation or database-specific details.

![HBnB High-Level Package Diagram](part1/hbnb_package_diagram.png)

 ## Business Logic Layer – Class Diagram

This section documents the Business Logic class diagram for the HBnB application. It describes the core domain entities, their attributes, operations, and the relationships that govern their interactions.  
The diagram focuses on modeling fundamental business rules and behaviors independently of presentation or persistence concerns.

### 1. Overview of the Business Logic Class Diagram

This class diagram represents the Business Logic layer of the HBnB application. It provides a structured view of the core domain entities, their attributes, operations, and the relationships that govern their interactions. The diagram focuses on modeling the fundamental business rules and behaviors independent of presentation or persistence concerns.

The Business Logic layer is designed following object-oriented principles, ensuring separation of concerns, reusability, and maintainability. All domain entities inherit from a common base class to enforce consistency across the model.

### 2. BaseEntity Class
The BaseEntity class serves as an abstract foundational class for all business entities within the system. It centralizes common attributes and behaviors shared across entities, promoting code reuse and consistency.

**Attributes**
- `id (UUID)`: A unique identifier for each entity instance.
- `created_at (DateTime)`: Timestamp indicating when the entity was created.
- `updated_at (DateTime)`: Timestamp indicating the last update to the entity.

**Methods**
- `save()`: Persists the entity state.
- `update()`: Updates the entity’s attributes.
- `delete()`: Removes the entity from the system.

All core entities (`User`, `Place`, `Review`, and `Amenity`) inherit from `BaseEntity`, ensuring uniform lifecycle management across the Business Logic layer.

### 3. User Entity
The User class represents registered users of the HBnB platform. Users act as the primary actors within the system and are responsible for managing places and submitting reviews.

**Attributes**
- `first_name (String)`
- `last_name (String)`
- `email (String)`
- `password (String)`
- `is_admin (Boolean)`: Indicates administrative privileges.

**Methods**
- `register()`: Handles user registration logic.
- `update_profile()`: Updates user-related information.
- `delete_account()`: Removes the user account from the system.

**Relationships**
- **User – Place (One-to-Many):**  
  A single user can own zero or more places, while each place is owned by exactly one user.
- **User – Review (One-to-Many):**  
  A user can submit multiple reviews, but each review is authored by one user.

### 4. Place Entity
The Place class represents accommodations or listings offered within the HBnB platform. It encapsulates location, pricing, and descriptive information.

**Attributes**
- `title (String)`
- `description (String)`
- `price (Float)`
- `latitude (Float)`
- `longitude (Float)`

**Methods**
- `create()`: Creates a new place listing.
- `update()`: Updates place details.
- `delete()`: Removes a place listing.
- `list_amenities()`: Retrieves associated amenities.

**Relationships**
- **Place – User (Many-to-One):**  
  Each place is owned by one user.
- **Place – Review (One-to-Many):**  
  A place can have multiple reviews, while each review belongs to one place.
- **Place – Amenity (Many-to-Many):**  
  A place may offer multiple amenities, and an amenity can be associated with multiple places.

### 5. Review Entity
The Review class models user feedback and ratings associated with a specific place. Reviews contribute to the quality assessment and user trust within the platform.

**Attributes**
- `rating (Integer)`
- `comment (String)`

**Methods**
- `create()`: Submits a new review.
- `update()`: Modifies an existing review.
- `delete()`: Removes a review.

**Relationships**
- Each review is associated with one user and one place.  
- Users and places may each have multiple reviews, enforcing clear ownership and context for feedback.

### 6. Amenity Entity
The Amenity class represents optional features or services that can be associated with places, such as Wi-Fi, parking, or air conditioning.

**Attributes**
- `name (String)`
- `description (String)`

**Methods**
- `create()`: Adds a new amenity.
- `update()`: Updates amenity details.
- `delete()`: Removes an amenity.

**Relationships**
- **Amenity – Place (Many-to-Many):**  
  Amenities can be shared across multiple places, allowing flexible and scalable feature assignment.
![HBnB Business Logic Class Diagram](part1/HBnB_Class%20Diagram_diagram.png)
### 8. Summary
The detailed class diagram provides a comprehensive and precise representation of the HBnB Business Logic layer. It serves as a reliable blueprint for implementation, ensuring that developers can translate business requirements into a robust, maintainable, and scalable system architecture.
