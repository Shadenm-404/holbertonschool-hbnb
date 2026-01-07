# HBnB – Part 2  
## API Implementation & Business Logic

---

## 🧠 Project Overview
This phase of the HBnB project focuses on implementing the backend foundation of the application by translating the designed architecture into working code. The work includes setting up the project structure, implementing core business logic classes, and exposing functionality through RESTful API endpoints.

The application enables the management of users, places, reviews, and amenities while following clean architecture principles to ensure scalability, modularity, and maintainability.

---

## 📂 Project Structure

<img width="500" height="332" alt="image" src="https://github.com/user-attachments/assets/781f7786-1c24-4980-96e8-507728492c16" />

---

## 📝 Tasks Breakdown

### **0. Project Setup and Package Initialization**
- Created the base project structure and Python packages.
- Initialized the Flask application.
- Configured application settings and entry points.
- Verified that the application runs successfully.

---

### **1. Core Business Logic Classes**
- Implemented core models:
  - User
  - Place
  - Review
  - Amenity
- Applied inheritance using a base model.
- Implemented UUID-based identifiers.
- Connected models to the repository and facade layers.

---

### **2. User Endpoints**
- Implemented RESTful endpoints:
  - `/users`
  - `/users/<user_id>`
- Supported full CRUD operations.
- Validated required fields such as email and password.
- Returned appropriate JSON responses and status codes.

---

### **3. Amenity Endpoints**
- Implemented endpoints:
  - `/amenities`
  - `/amenities/<amenity_id>`
- Supported POST, GET, PUT, and DELETE operations.
- Added input validation and error handling.

---

### **4. Place Endpoints**
- Implemented endpoints:
  - `/places`
  - `/places/<place_id>`
- Supported full CRUD functionality.
- Handled relationships with users and amenities.
- Ensured validation of related resource IDs.

---

### **5. Review Endpoints**
- Implemented endpoints:
  - `/reviews`
  - `/reviews/<review_id>`
- Supported CRUD operations.
- Linked reviews to users and places.
- Validated relationships and request payloads.

---

### **6. Testing and Validation**
- Before testing, all required dependencies must be installed:
  ```bash
  pip install -r requirements.txt

- Manually tested all endpoints using curl.

- Verified successful operations and error scenarios.

- Tested invalid input, missing fields, and non-existent IDs.

- Ensured consistent JSON responses and correct HTTP status codes.

---

## **✅Testing Guidelines**
- Install dependencies before running or testing the application.

- Always include Content-Type: application/json for POST and PUT requests.

- Use curl -i to inspect response headers and status codes.

- Test both success and failure cases.

- Ensure all endpoints return valid JSON.
