# from flask import Blueprint, jsonify
# from misp_service import fetch_misp_threats

# threat_bp = Blueprint("threat_bp", __name__)

# @threat_bp.route('/api/threats', methods=['GET'])
# def get_threats():
#     """Fetch threats from MISP and return as JSON."""
#     threats = fetch_misp_threats()
#     return jsonify(threats)
