# Zippee Task Manager API

## Features
- User registration and JWT authentication
- CRUD operations for tasks
- Pagination and filtering
- Role-based permissions (admin, regular)
- Swagger API documentation

## Setup Instructions

### 1. Create and activate a virtual environment
```
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Set environment variables (optional for development)
```
set FLASK_APP=run.py
set FLASK_ENV=development
set SECRET_KEY=your-secret-key
```

### 4. Initialize the database
```
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

### 5. Run the application
```
flask run
```

The API will be available at http://localhost:5000
Swagger docs: http://localhost:5000/apidocs

### 6. Run tests
```
pytest
```

## Project Structure
```
app/
    __init__.py
    models.py
    routes.py
    auth.py
    schemas.py
tests/
config.py
run.py
requirements.txt
README.md
```

