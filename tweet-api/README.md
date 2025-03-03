# # Tweet API

In this project, I will extend the Tweet API by adding new functionality and modifying the database schema.

**Task 1**: Add 4 New Endpoints to the Tweet API


1. Create a Tweet Item:
  - Adds a new Tweet item to the database.
  - The userId must be included in the request body when creating a tweet.
  -	Returns the created item.
2. Delete a Tweet Item by ID:
  -	Deletes an existing Tweet item by its ID.
	-	Returns the deleted item.
3. Get a Tweet Item by ID:
  -	Retrieves a Tweet item by its ID.
  -	Returns the requested item.
4. Update a Tweet Item by ID:
  -	Updates an existing Tweet item by its ID.
  -	Returns the updated item.


**Task 2**: Add a New Column to the Users Table and Create an Endpoint

1. Add `preferredName` Column:
  -	Add a new column, `preferredName`, to the existing User model in your Prisma schema.
2. Create an Endpoint:
  -	Implement a new API endpoint that returns a list of users sorted by `preferredName` in ascending order.

