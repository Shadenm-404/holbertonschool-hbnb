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

3. Fetching a List of Places
   
Purpose
Illustrates how the system retrieves a list of places based on user-defined filters.
Explanation
The user sends a request to the API to retrieve places. The API forwards filtering parameters to the Business Logic layer, which queries the database for matching places. The results are returned through the same layers back to the user.
Design Note
Filtering logic is handled in the Business Logic layer to maintain separation of concerns.

4. Review Submission
Purpose
Describes the process of submitting and validating a review.
Explanation
The user submits a review via the API. The Business Logic layer validates the review data and saves it in the database. Upon successful creation, the API returns an HTTP 201 Created response.
Design Note
Centralised validation ensures data consistency and enforces business rules.


