import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2.extras
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for flash messages

# Database connection setup
DB_HOST = "localhost"
DB_NAME = "khalza"
DB_USER = "postgres"
DB_PASS = "ilovemoon19"

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

# Routes

from werkzeug.security import generate_password_hash

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Hash the password before storing it in the database
        password_hash = generate_password_hash(password)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert the user into the database
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                       (username, email, password_hash))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')


from werkzeug.security import check_password_hash

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Fetch the user from the database
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if user and check_password_hash(user[3], password):  # user[3] is the hashed password column
            return redirect(url_for('dashboard'))  # Redirect to dashboard on successful login
        else:
            flash('Invalid credentials. Please try again.', 'error')
    
    return render_template('login.html')



@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        try:
            username = request.form['username']  # Capture the username
            fullname = request.form['fullname']
            email = request.form['email']
            password = request.form['password']
        except KeyError as e:
            flash(f'Missing form field: {e}', 'error')
            return redirect(url_for('signin'))

        # Hash the password before saving it
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if the user already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            flash('Email already registered. Please log in.', 'warning')
            return redirect(url_for('login'))
        
        # Insert new user into the database, with hashed password
        cursor.execute("INSERT INTO users (username, fullname, email, password_hash) VALUES (%s, %s, %s, %s)", 
                       (username, fullname, email, hashed_password))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        flash('Account created successfully. Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signin.html')

@app.route('/asset-management')
def asset_management():
    return render_template('AssetManagement.html')

@app.route('/mitigation-planning')
def mitigation_planning():
    return render_template('MitigationPlanning.html')

@app.route('/reports')
def reports():
    return render_template('Reports.html')

@app.route('/risk-assessment')
def risk_assessment():
    return render_template('RiskAssessment.html')

@app.route('/risk-monitoring')
def risk_monitoring():
    return render_template('RiskMonitoring.html')

@app.route('/settings')
def settings():
    return render_template('Settings.html')

@app.route('/threat-management')
def threat_management():
    return render_template('ThreatManagement.html')

if __name__ == '__main__':
    app.run(debug=True)
