from flask import jsonify, request
from . import dashboard_bp
from db.database import DatabaseSession
from models.designer import Designer, Sidemark
from models.inventory import Inventory
from models.orders import Workorder, WorkorderItem
from sqlalchemy.orm import joinedload


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

    inventory_data = [{"id": item.id, "item_name": item.item_name, "quantity": item.quantity} for item in
                      designer_inventory]

    return jsonify(inventory_data), 200


@dashboard_bp.route('/api/designer/<int:designer_id>/sidemarks', methods=['GET'])
def get_sidemarks_for_designer(designer_id):
    with DatabaseSession() as session:
        # Fetch the designer information
        designer = session.query(Designer).filter_by(id=designer_id).first()

        # If designer is not found, return an error response
        if designer is None:
            return jsonify({"error": "Designer not found"}), 404

        # Fetch the sidemarks associated with the designer
        sidemarks = session.query(Sidemark).filter_by(designer_id=designer_id).all()

        # Prepare the sidemark data
        sidemark_data = [{"id": s.id, "name": s.name} for s in sidemarks]

    return jsonify(sidemark_data), 200


@dashboard_bp.route('/api/sidemark/<int:sidemark_id>/orders', methods=['GET'])
def get_orders_for_sidemark(sidemark_id):
    with DatabaseSession() as session:
        orders = session.query(Workorder).filter_by(sidemark_id=sidemark_id).all()
        order_data = [{"id": o.id, "workorder_id": o.workorder_id, "status": o.status} for o in orders]
    return jsonify(order_data), 200


@dashboard_bp.route('/api/designer/<int:designer_id>/sidemark/<int:sidemark_id>/orders', methods=['GET'])
def view_orders(designer_id, sidemark_id):
    """Return the orders for a specific designer and sidemark as JSON."""
    with DatabaseSession() as session:
        # Query the orders for the specified sidemark and designer
        orders = (
            session.query(Workorder)
            .options(joinedload(Workorder.sidemark), joinedload(Workorder.designer))
            .filter(Workorder.sidemark_id == sidemark_id, Workorder.designer_id == designer_id)
            .all()
        )

    order_data = [{"id": o.id, "workorder_id": o.workorder_id, "status": o.status} for o in orders]
    return jsonify(order_data), 200


@dashboard_bp.route('/api/workorder/<int:workorder_id>/inventory', methods=['GET'])
def view_workorder_inventory(workorder_id):
    """Return the details of a workorder and its related inventory in JSON format."""
    with DatabaseSession() as session:
        # Query the Workorder
        workorder = session.query(Workorder).filter_by(id=workorder_id).first()

        # Query the WorkorderItems and associated Inventory for this Workorder
        workorder_items = (
            session.query(WorkorderItem, Inventory)
            .join(Inventory, WorkorderItem.inventory_id == Inventory.id)
            .filter(WorkorderItem.workorder_id == workorder_id)
            .all()
        )

        # Prepare the response data
        inventory_data = [
            {
                "id": item.Inventory.id,
                "item_name": item.Inventory.item_name,
                "sku": item.Inventory.sku,
                "manufacture": item.Inventory.manufacture,
                "quantity": item.Inventory.quantity,
                # Note: This seems odd as it might be same as WorkorderItem.quantity.
                "length": item.Inventory.length,
                "width": item.Inventory.width,
                "height": item.Inventory.height,
                "weight": item.Inventory.weight,
                "description": item.Inventory.description  # Include any other fields needed
            }
            for item in workorder_items
        ]

    return jsonify(inventory_data), 200


@dashboard_bp.route('/api/add-sidemark', methods=['POST'])
def add_sidemark():
    data = request.get_json()
    sidemark_name = data.get('sidemarkName')
    company_name = data.get('company')

    if sidemark_name and company_name:
        with DatabaseSession() as session:
            # Find the designer by company name
            designer = session.query(Designer).filter(Designer.company == company_name).first()

            if designer:
                new_sidemark = Sidemark(name=sidemark_name, designer_id=designer.id)
                session.add(new_sidemark)
                session.commit()

                response = {
                    'status': 'success',
                    'message': f'New sidemark added: {sidemark_name}',
                    'sidemark_name': sidemark_name
                }
                return jsonify(response), 200
            else:
                return jsonify({'status': 'fail', 'message': 'Designer not found.'}), 400
    else:
        return jsonify({'status': 'fail', 'message': 'Sidemark name or company name is missing.'}), 400


@dashboard_bp.route('/api/workorder/<int:workorder_id>/inventory', methods=['GET'])
def view_workorder(workorder_id):
    """Return workorder details and associated inventory as JSON."""
    with DatabaseSession() as session:
        # Query the requested Workorder
        workorder = session.query(Workorder).filter_by(id=workorder_id).first()

        if not workorder:
            return jsonify({"status": "fail", "message": "Workorder not found."}), 404

        # Fetch the WorkorderItems and associated Inventory
        workorder_items = (
            session.query(WorkorderItem, Inventory)
            .join(Inventory, WorkorderItem.inventory_id == Inventory.id)
            .filter(WorkorderItem.workorder_id == workorder_id)
            .all()
        )

        # Convert the data to JSON-friendly format
        inventory_data = [
            {"id": item.Inventory.id, "item_name": item.Inventory.item_name, "quantity": item.WorkorderItem.quantity}
            for item in workorder_items]

        return jsonify({
            "status": "success",
            "workorder_id": workorder_id,
            "inventory": inventory_data
        }), 200
