from database.db_init import db
from app import app

with app.app_context():
    try:
        db.session.execute("SELECT 1")  # Simple query to test connection
        print("✅ Database connection successful!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
