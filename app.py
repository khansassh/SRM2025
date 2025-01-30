from flask import Flask
from database.db_init import init_db, db
from routes.asset_routes import asset_bp
from routes.threat_routes import threat_bp

app = Flask(__name__)

# Initialize database
init_db(app)

# Register blueprints (routes)
app.register_blueprint(asset_bp)
app.register_blueprint(threat_bp)

if __name__ == "__main__":
    app.run(debug=True)
