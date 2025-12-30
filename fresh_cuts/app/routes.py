from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models import Service, Booking, User, Availability
from app.forms import AvailabilityForm
from flask_login import login_user, logout_user, login_required
from datetime import datetime
import os

main = Blueprint('main', __name__)
admin = Blueprint('admin', __name__, url_prefix='/admin')

# Public Routes
@main.route('/')
def index():
    services = Service.query.all()
    # Limit to 3 for the home page display if needed, or show all
    return render_template('public/index.html', services=services)

@main.route('/services')
def services():
    services = Service.query.all()
    return render_template('public/services.html', services=services)

@main.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        # Simple booking logic
        service_id = request.form.get('service_id')
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        
        # Combine date and time
        booking_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        
        # Validation: Check Availability
        day_of_week = booking_time.weekday() # 0=Monday, 6=Sunday
        availability = Availability.query.filter_by(day_of_week=day_of_week).first()

        if availability:
            if availability.is_closed:
                flash(f"Sorry, we are closed on {booking_time.strftime('%A')}s.")
                return redirect(url_for('main.book'))
            
            booking_time_time = booking_time.time()
            if booking_time_time < availability.start_time or booking_time_time > availability.end_time:
                flash(f"Please select a time between {availability.start_time.strftime('%I:%M %p')} and {availability.end_time.strftime('%I:%M %p')}.")
                return redirect(url_for('main.book'))

        booking = Booking(
            customer_name=name,
            customer_email=email,
            customer_phone=phone,
            service_id=service_id,
            booking_time=booking_time,
            status='Confirmed'
        )
        db.session.add(booking)
        db.session.commit()
        return redirect(url_for('main.confirmation', booking_id=booking.id))
        
    services = Service.query.all()
    return render_template('public/book.html', services=services)

@main.route('/confirmation/<int:booking_id>')
def confirmation(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return render_template('public/confirmation.html', booking=booking)

# Admin Routes
@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        
        flash('Invalid username or password')
    return render_template('admin/login.html')

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@admin.route('/dashboard')
@login_required
def dashboard():
    bookings = Booking.query.order_by(Booking.booking_time.desc()).all()
    return render_template('admin/dashboard.html', bookings=bookings)

@admin.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    # Ensure all days exist
    if Availability.query.count() < 7:
        for i in range(7):
            if not Availability.query.filter_by(day_of_week=i).first():
                db.session.add(Availability(day_of_week=i, start_time=datetime.strptime("09:00", "%H:%M").time(), end_time=datetime.strptime("20:00", "%H:%M").time()))
        db.session.commit()

    availabilities = Availability.query.order_by(Availability.day_of_week).all()
    
    if request.method == 'POST':
        for av in availabilities:
            av.start_time = datetime.strptime(request.form.get(f'start_time_{av.id}'), "%H:%M").time()
            av.end_time = datetime.strptime(request.form.get(f'end_time_{av.id}'), "%H:%M").time()
            av.is_closed = request.form.get(f'is_closed_{av.id}') == 'on'
        db.session.commit()
        flash('Hours updated successfully.')
        return redirect(url_for('admin.settings'))

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return render_template('admin/settings.html', availabilities=zip(availabilities, days))
