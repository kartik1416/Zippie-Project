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

### Expose the server publicly (optional)

If you want to make the local dev server reachable from other machines or the internet, there are two common approaches:

- Bind to 0.0.0.0 and open/forward the port on your router/firewall (less secure):

```powershell
# start server on all interfaces
$env:HOST='0.0.0.0'; $env:PORT='5000'; python run.py
```

Then ensure your OS firewall allows incoming connections on port 5000 and set up port forwarding on your router to forward external traffic to your machine.

- Use a secure tunneling service like ngrok or localtunnel (recommended for development):

```powershell
# using ngrok (install from https://ngrok.com)
ngrok http 5000

# using localtunnel (install via npm)
lt --port 5000
```

Both will provide a public URL (HTTPS) that tunnels to your local server without opening ports on your machine.

### 6. Run tests
```
pytest
```

---

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

