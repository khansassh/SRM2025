import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2.extras

<<<<<<< Updated upstream

app = Flask(_name_)
=======
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for flash messages
>>>>>>> Stashed changes

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
@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if the user exists
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if user:
            return redirect(url_for('dashboard'))  # Redirect to dashboard on successful login
        else:
            flash('Invalid credentials. Please try again.', 'error')
    
    return render_template('login.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if the user already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            flash('Email already registered. Please log in.', 'warning')
            return redirect(url_for('login'))
        
        # Insert new user into the database
        cursor.execute("INSERT INTO users (fullname, email, password) VALUES (%s, %s, %s)", 
                       (fullname, email, password))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        flash('Account created successfully. Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signin.html')

<<<<<<< Updated upstream
@app.route('/AssetManagement.html')
def asset_management():
    return render_template('AssetManagement.html')

=======
>>>>>>> Stashed changes
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

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

<<<<<<< Updated upstream
DB_HOST = "localhost"
DB_NAME = "khalza"
DB_USER = "postgres"
DB_PASS = "ilovemoon19"

# Function to get a database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

@app.route('/')
def home():
    # Example of how to use the database connection
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Example query
    cursor.execute("SELECT * FROM some_table")
    result = cursor.fetchall()
    
    cursor.close()
    conn.close()  # Ensure the connection is closed after use
    
    return render_template('dashboard.html', data=result)

if _name_ == '_main_':
    app.run(debug=True)
=======
if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> Stashed changes
