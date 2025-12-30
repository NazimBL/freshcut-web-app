# Fresh Cuts Barbershop App

A premium, Flask-based booking system for barbershops.

## Features
- **Public**: Browse services, check availability, and book appointments.
- **Admin**: Secure dashboard to view bookings and manage working hours.
- **Automated Validation**: Prevents bookings outside of business hours.

## Local Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Initialize Database**:
    ```bash
    python seed_db.py
    ```
    *This creates `fresh_cuts.db` and seeds it with default services and an admin user.*

3.  **Run the App**:
    ```bash
    python run.py
    ```
    Access the app at `http://127.0.0.1:5000`.

## Admin Access
- **Login URL**: `http://127.0.0.1:5000/admin/dashboard`
- **Default Credentials**:
    - Username: `admin`
    - Password: `password123`

## Deployment
To deploy this application to a production server (e.g., Render, Heroku, DigitalOcean):

1.  **Database**:
    - **SQLite** (Current): Works fine for simple, single-instance deployments (e.g., a VPS or Railway volume).
    - **PostgreSQL**: Recommended for scalable platforms like Heroku. You would update `config.py` to read `DATABASE_URL` from the environment.

2.  **Security**:
    - Change the `SECRET_KEY` in `config.py` to a secure random string.
    - **Change the Admin Password**: Open the python shell in production (`flask shell`) and update the admin user's password.

3.  **Web Server**:
    - Use a production WSGI server like `gunicorn` instead of `python run.py`.
    - Command: `gunicorn -w 4 run:app`
