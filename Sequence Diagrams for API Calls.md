This section describes the interaction flow between system components for the primary API operations in the HBnB application. The sequence diagrams illustrate how requests move through the Presentation, Business Logic, and Persistence layers.

1. Registration
Purpose
Illustrates the user registration workflow.
Explanation
The user submits registration data to the API. The Business Logic layer creates and saves the user in the database. A successful operation returns an HTTP 201 Created response.
Design Note
User-creation logic is isolated in the Business Logic layer to ensure security and consistency.

2. Place Creation
   
Purpose
Shows how a new place is created and linked to existing amenities.
Explanation
The API forwards the place creation request to the Business Logic layer. Amenity IDs are validated against the database before saving the place. The created place is then returned to the user with an HTTP 201 Created response.
Design Note
Validating related entities preserves referential integrity.
