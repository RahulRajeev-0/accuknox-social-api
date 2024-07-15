# AccuKnox Social Networking Application 

This project is a RESTful API for a social networking application built with Django Rest Framework. It provides core functionalities such as user authentication, user search, and a friend request system. The API is containerized using Docker for easy deployment and uses JWT (JSON Web Tokens) for secure authentication.

### Key Features
- User authentication with JWT (login and signup)
- User search by email and name
- Friend request management (send, accept, reject)
- Friend list and pending request views
- Rate limiting on friend requests

### Tech Stack
- Django
- Django Rest Framework
- Docker
- JWT Authentication

## Prerequisites

Make sure you have the following installed before setting up the project:
- Docker
- Git

## Important: Authentication Requirements

This project uses JWT (JSON Web Token) authentication. Please note:

1. Registration and login endpoints are publicly accessible.
2. All other endpoints require authentication.
3. To authenticate:
   - Log in to receive an access token in the response.
   - For all subsequent requests, include this access token in the Authorization header as a Bearer token.
4. Access tokens are valid for 60 minutes from the time of issuance.

Example:
Authorization: Bearer <your_access_token_here>

Important:
- Failure to include a valid access token will result in authentication errors.
- If your token expires, you'll need to log in again to obtain a new one.
- Ensure you're properly authenticated when testing or using the API.
- Plan your testing or usage sessions with the 60-minute token validity in mind.
## Getting Started

### Clone the Repository

```bash
git clone https://github.com/RahulRajeev-0/accuknox-social-api.git
cd accuknox-social-api/
```
```
cd backend
```
#### Build and start the Docker containers
```
docker-compose up --build

```
#### Apply Migrations
Open a new terminal window/tab and apply database migrations to set up the database schema:
```
docker-compose exec web python manage.py makemigrations

docker-compose exec web python manage.py migrate

```
#### Accessing the Application
Create super user
```
docker-compose exec web python manage.py createsuperuser

```
Django Admin Interface
To access the Django admin interface:
1. Open your web browser and go to http://localhost:8000/admin.
2. Log in with the superuser credentials.

## API Collection 
To help you get started with testing the API endpoints, I've prepared a Postman collection. 
https://documenter.getpostman.com/view/31743247/2sA3kPqQPy




