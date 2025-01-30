from flask import Flask, render_template

app = Flask(__name__)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/asset-management')
def asset_management():
    return render_template('AssetManagement.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

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
