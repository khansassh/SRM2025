from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/cyber_risk_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Database Models
class Threat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class RiskAssessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    risk_level = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Dashboard Route
@app.route('/')
def dashboard():
    threats = Threat.query.all()
    risks = RiskAssessment.query.all()
    return render_template('dashboard.html', threats=threats, risks=risks)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
