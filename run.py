import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Allow configuring host and port via environment variables.
    # Binding to 0.0.0.0 makes the server reachable on the host's network interfaces.
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', '').lower() == 'development'
    app.run(host=host, port=port, debug=debug)

