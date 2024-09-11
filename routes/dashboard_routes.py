from flask import jsonify
from . import dashboard_bp


@dashboard_bp.route('/dashboard/')
def index():
    return jsonify({'message': 'success!'})
