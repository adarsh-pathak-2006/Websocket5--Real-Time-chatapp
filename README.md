# Django Channels Chat App

A real-time chat application built with Django, Django Channels, and Django REST Framework.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Setup environment variables:
   Copy `.env.example` to `.env` and fill in the values.

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the server:
   ```bash
   daphne -p 8000 chat_app.asgi:application
   ```

## Deployment on Render

This project is configured for deployment on Render.

1. Ensure the `build.sh` script is executable.
2. In the Render dashboard, create a new Web Service.
3. Set the build command to `./build.sh`.
4. Set the start command to `daphne -b 0.0.0.0 -p $PORT chat_app.asgi:application`.
5. Add the necessary Environment Variables (e.g., `SECRET_KEY`, `DATABASE_URL`, `REDIS_URL`).
