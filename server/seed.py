from app import app
from models import db, Plant

with app.app_context():
    db.drop_all()
    db.create_all()

    plants = [
        Plant(name="Aloe", image="./images/aloe.jpg", price=11.50, is_in_stock=True),
        Plant(name="ZZ Plant", image="./images/zz-plant.jpg", price=25.98, is_in_stock=False),
        Plant(name="Peace Lily", image="./images/peace-lily.jpg", price=15.00, is_in_stock=True)
    ]

    db.session.add_all(plants)
    db.session.commit()

    print("🌿 Database seeded successfully!")
