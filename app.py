import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash

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
    # Use DictCursor to return results as dictionaries
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return conn, cursor

# Routes

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Hash the password before storing it in the database
        password_hash = generate_password_hash(password)
        
        conn, cursor = get_db_connection()
        
        # Insert the user into the database
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                       (username, email, password_hash))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn, cursor = get_db_connection()
        
        # Fetch the user from the database
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):  # Access by column name
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

        conn, cursor = get_db_connection()
        
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

@app.route('/asset-management', methods=['GET', 'POST'])
def asset_management():
    conn, cursor = get_db_connection()
    
    if request.method == 'POST':
        try:
            asset_name = request.form['asset_name']
            asset_type = request.form['asset_type']
            description = request.form['description']
            criticality_level = request.form['criticality_level']
            owner = request.form['owner']

            cursor.execute(
                "INSERT INTO assets (asset_name, asset_type, description, criticality_level, owner) "
                "VALUES (%s, %s, %s, %s, %s)",
                (asset_name, asset_type, description, criticality_level, owner)
            )
            conn.commit()
            flash('Asset saved successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error saving asset: {str(e)}', 'error')
    
    # Get all assets for display
    cursor.execute("SELECT * FROM assets ORDER BY created_at DESC")
    assets = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('AssetManagement.html', assets=assets)

@app.route('/mitigation-planning')
def mitigation_planning():
    return render_template('MitigationPlanning.html')

@app.route('/reports')
def reports():
    return render_template('Reports.html')

@app.route('/risk-assessment')
def risk_assessment():
    return render_template('RiskAssessment.html')

@app.route('/risk-monitoring', methods=['GET', 'POST'])
def risk_monitoring():
    conn, cursor = get_db_connection()
    
    if request.method == 'POST':
        try:
            # Extract form data
            file_id = request.form['file_id']
            affected_asset = request.form['affected_asset']
            threat_name = request.form['threat_name']
            file_size = request.form['file_size']
            risk_type = request.form['risk_type']

            cursor.execute(
                "INSERT INTO risks (file_id, affected_asset, threat_name, file_size, risk_type) "
                "VALUES (%s, %s, %s, %s, %s)",
                (file_id, affected_asset, threat_name, file_size, risk_type)
            )
            conn.commit()
            flash('Risk entry added successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error saving risk entry: {str(e)}', 'error')
    
    # Get all risks
    cursor.execute("""
        SELECT id, file_id, affected_asset, threat_name, 
               to_char(detected_time, 'HH12:MI AM') as time,
               file_size, risk_type 
        FROM risks 
        ORDER BY detected_time DESC
    """)
    risks = cursor.fetchall()
    
    # Get risk statistics for widgets
    cursor.execute("""
        SELECT 
            COUNT(*) FILTER (WHERE risk_type = 'High Risk') as high_risk,
            COUNT(*) FILTER (WHERE risk_type = 'Medium Risk') as medium_risk,
            COUNT(*) FILTER (WHERE risk_type = 'Low Risk') as low_risk
        FROM risks
    """)
    risk_stats = cursor.fetchone()
    
    cursor.close()
    conn.close()

    return render_template('RiskMonitoring.html', 
                         risks=risks, 
                         risk_stats=risk_stats)

@app.route('/settings')
def settings():
    return render_template('Settings.html')

@app.route('/threat-management', methods=['GET', 'POST'])
def threat_management():
    conn, cursor = get_db_connection()  # Use the updated connection function
    
    # Handle form submission
    if request.method == 'POST':
        threat_name = request.form.get('threat-name')
        threat_source = request.form.get('threat-source')
        description = request.form.get('threat-description')
        severity = request.form.get('threat-severity')
        
        try:
            cursor.execute(
                "INSERT INTO threats (threat_name, threat_source, description, severity) "
                "VALUES (%s, %s, %s, %s)",
                (threat_name, threat_source, description, severity)
            )
            conn.commit()
            flash('Threat added successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error saving threat: {str(e)}', 'error')
    
    # Get threats for real-time feed
    cursor.execute("SELECT * FROM threats ORDER BY created_at DESC")
    threats = cursor.fetchall()  # This will now return dictionaries
    cursor.close()
    conn.close()
    
    return render_template('ThreatManagement.html', threats=threats)

if __name__ == '__main__':
    app.run(debug=True)