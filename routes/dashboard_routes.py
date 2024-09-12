from flask import jsonify
from . import dashboard_bp
from db.database import DatabaseSession
from models.designer import Designer, Sidemark
from models.inventory import Inventory
from models.orders import Workorder


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


@dashboard_bp.route('/api/designer/<int:designer_id>/inventory', methods=['GET'])
def view_designer_inventory(designer_id):
    """Fetch all inventory items for a specific designer in JSON format."""
    with DatabaseSession() as session:
        designer_inventory = session.query(Inventory).filter_by(designer_id=designer_id).all()

    inventory_data = [{"id": item.id, "item_name": item.item_name, "quantity": item.quantity} for item in designer_inventory]

    return jsonify(inventory_data), 200


@dashboard_bp.route('/api/designer/<int:designer_id>/sidemarks', methods=['GET'])
def get_sidemarks_for_designer(designer_id):
    with DatabaseSession() as session:
        sidemarks = session.query(Sidemark).filter_by(designer_id=designer_id).all()
        sidemark_data = [{"id": s.id, "name": s.name} for s in sidemarks]
    return jsonify(sidemark_data), 200


@dashboard_bp.route('/api/sidemark/<int:sidemark_id>/orders', methods=['GET'])
def get_orders_for_sidemark(sidemark_id):
    with DatabaseSession() as session:
        orders = session.query(Workorder).filter_by(sidemark_id=sidemark_id).all()
        order_data = [{"id": o.id, "workorder_id": o.workorder_id, "status": o.status} for o in orders]
    return jsonify(order_data), 200
