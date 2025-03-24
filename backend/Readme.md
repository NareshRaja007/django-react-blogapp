# Simple Blog - Django Backend

## Overview
Simple Blog is a Django-based backend for a blog application. It provides APIs for user authentication (signup, login) and blog post management (CRUD operations). The backend uses PostgreSQL as the database and follows a structured API response format.

## Features
- User authentication (JWT-based login & signup)
- Blog post management (create, update, delete, view posts)
- Pagination for blog post retrieval
- Structured API responses
- Logging integration
- Unit tests for models and APIs

## Installation
### 1. Clone the Repository
```sh
$ git clone <your-repository-url>
$ cd simple_blog
```

### 2. Set Up a Virtual Environment
```sh
$ python -m venv venv
$ source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```sh
$ pip install -r requirements.txt
```

### 4. Configure the Database
Update the `DATABASES` section in `settings.py` to use PostgreSQL. Then, run:
```sh
$ python manage.py migrate
```

### 6. Run the Server
```sh
$ python manage.py runserver 
```

## API Endpoints

### User Authentication
- **Register User**: `POST /backend/v1/auth/register/`
- **Login User**: `POST /backend/v1/auth/login/`

### Blog Post Management
- **Create a Post**: `POST /backend/v1/blog_app/post_create/`
- **Get All Posts**: `GET /backend/v1/blog_app/posts/`
- **Get User's Posts**: `GET /backend/v1/blog_app/my_posts/`
- **Edit a Post**: `PUT /backend/v1/blog_app/post_edit/`
- **Delete a Post**: `DELETE /backend/v1/blog_app/post_delete/?post_id=<id>`

## Running Tests
To run test cases for models and APIs:
```sh
$ python manage.py test
```

## Contributing
Feel free to open issues and submit pull requests for improvements!

## License
This project is open-source under the MIT License.

