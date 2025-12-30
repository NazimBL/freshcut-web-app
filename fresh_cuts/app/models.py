from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    duration_minutes = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False) # Storing as integer (cents) or just float for simplicity
    image_url = db.Column(db.String(255))
    
    bookings = db.relationship('Booking', backref='service', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    booking_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='Confirmed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_of_week = db.Column(db.Integer, unique=True, nullable=False) # 0=Monday, 6=Sunday
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_closed = db.Column(db.Boolean, default=False)
