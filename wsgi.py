"""
wsgi.py — WSGI entry point for gunicorn / flask run.

    flask --app wsgi run           (development)
    gunicorn wsgi:app             (production)
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
