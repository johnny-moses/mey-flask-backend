from flask import jsonify
from . import dashboard_bp
from db.database import DatabaseSession
from models.designer import Designer


@dashboard_bp.route('/dashboard/')
def index():
    return jsonify({'message': 'success!'})


@dashboard_bp.route('/api/designer/', methods=['GET'])  # I changed the route to be plural to align with convention
def get_designer_names():
    with DatabaseSession() as session:
        designers = session.query(Designer.id, Designer.designer_name).filter(Designer.designer_name.isnot(None)).all()
        # Create a list of dictionaries with 'id' and 'designer_name'
        designer_data = [{"id": designer.id, "name": designer.designer_name} for designer in designers]
        return jsonify(designer_data), 200

