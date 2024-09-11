from flask import jsonify
from . import dashboard_bp
from db.database import DatabaseSession
from models.designer import Designer


@dashboard_bp.route('/dashboard/')
def index():
    return jsonify({'message': 'success!'})


@dashboard_bp.route('/api/designer_names', methods=['GET'])
def get_designer_names():
    with DatabaseSession() as session:
        designers = session.query(Designer.designer_name).filter(Designer.designer_name.isnot(None)).all()
        designer_names = [designer.designer_name for designer in designers]
        return jsonify(designer_names), 200
