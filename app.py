from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db
from routes.threat_routes import threat_bp
from routes.asset_routes import asset_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Database
db.init_app(app)

# Register API Routes
app.register_blueprint(threat_bp)
app.register_blueprint(asset_bp)

if __name__ == "__main__":
    app.run(debug=True)
