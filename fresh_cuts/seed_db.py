from app import create_app, db
from app.models import Service, User, Availability

app = create_app()

def seed():
    with app.app_context():
        db.create_all()

        if Service.query.first():
            print("Database already seeded.")
            return

        # Services
        services = [
            Service(
                name="Professional Package", 
                description="Haircut, hot towel shave, eyebrow trim, and styling.", 
                duration_minutes=60, 
                price=55, 
                image_url="https://images.unsplash.com/photo-1503951914875-befea7470dac?auto=format&fit=crop&w=800&q=80"
            ),
            Service(
                name="Regular Haircut", 
                description="Precision haircut and style.", 
                duration_minutes=30, 
                price=30, 
                image_url="https://images.unsplash.com/photo-1599351431202-1e0f0137d9c8?auto=format&fit=crop&w=800&q=80"
            ),
            Service(
                name="Hot Towel Shave", 
                description="Relaxing hot towel treatment and straight razor shave.", 
                duration_minutes=30, 
                price=35, 
                image_url="https://images.unsplash.com/photo-1621605815971-fbc98d665033?auto=format&fit=crop&w=800&q=80"
            ),
            Service(
                name="Beard Trim", 
                description="Shape and style your beard.", 
                duration_minutes=20, 
                price=20, 
                image_url="https://images.unsplash.com/photo-1585747860715-2ba372244959?auto=format&fit=crop&w=800&q=80"
            )
        ]

        db.session.add_all(services)

        # Default Admin
        admin = User(username="admin")
        admin.set_password("password123")
        db.session.add(admin)
        
        db.session.commit()
        print("Database seeded successfully.")

if __name__ == "__main__":
    seed()
