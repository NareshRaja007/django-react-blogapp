# Common README for Simple Blog (Backend + Frontend)

## Project Overview
Simple Blog is a full-stack web application built with Django REST Framework for the backend and React for the frontend. It allows users to register, log in, and manage their blog posts with authentication.

---

## 1️⃣ Backend (Django REST Framework)

### Features:
- User registration and login with JWT authentication
- CRUD operations for blog posts
- Pagination support for blog post listing
- Structured API responses using `Common.create_payload`
- Logging and error handling

### Installation
#### Prerequisites:
- Python 3.8+
- PostgreSQL (or your preferred database)

#### Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd simple_blog/backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Set up the database
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

### API Endpoints
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/backend/v1/blog_app/register` | Register a new user |
| POST | `/backend/v1/blog_app/login` | Authenticate a user and obtain JWT tokens |
| GET | `/backend/v1/blog_app/all_posts` | Get all blog posts (paginated) |
| POST | `/backend/v1/blog_app/post_create` | Create a new blog post |
| PUT | `/backend/v1/blog_app/post_edit` | Edit a user's blog post |
| DELETE | `/backend/v1/blog_app/post_delete?post_id=` | Delete a blog post |

For more details, check the [Backend README](backend/README.md).

---

## 2️⃣ Frontend (React + Vite)

### Features:
- React app integrated with Django REST API
- User authentication using JWT
- Fetching and displaying blog posts
- CRUD operations for blog posts

### Installation
#### Prerequisites:
- Node.js 16+
- npm or yarn

#### Setup
```bash
# Navigate to the frontend directory
cd simple_blog/frontend

# Install dependencies
npm install  # or `yarn install`

# Run the development server
npm run dev  # or `yarn dev`
```

### Frontend Pages
| Page | Description |
|------|-------------|
| Home | Displays a list of blog posts |
| Login | Allows users to log in |
| Register | Allows new users to sign up |
| Create Post | Form to create a new blog post |
| Edit Post | Edit an existing blog post |

For more details, check the [Frontend README](frontend/README.md).

---

## Running the Full Application
1. Start the **backend server**:
   ```bash
   cd backend
   python manage.py runserver
   ```
2. Start the **frontend server**:
   ```bash
   cd frontend
   npm run dev
   ```
3. Open the frontend at `http://localhost:5173`
   Change your backend running sercer IP in .env in frontend
---

## Testing
### Backend Tests
```bash
cd backend
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm run test
```

---

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m 'Added new feature'`)
4. Push to the branch (`git push origin feature-name`)
5. Create a pull request

---

## License
This project is open-source under the MIT License.

---

## Contact
For any queries, reach out to me via GitHub Issues or email.

---

Now you're all set! 🚀 Happy coding!

