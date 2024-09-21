from flask import jsonify, request
from . import dashboard_bp
from db.database import DatabaseSession
from models.designer import Designer, Sidemark
from models.inventory import Inventory
from models.orders import Workorder, WorkorderItem
from sqlalchemy.orm import joinedload


@dashboard_bp.route('/api/designers/', methods=['GET'])
def get_designer_names():
    with DatabaseSession() as session:
        designers = session.query(
            Designer.id,
            Designer.designer_name,
            Designer.company,
            Designer.email,
            Designer.phone
        ).filter(Designer.designer_name.isnot(None)).all()

        designer_data = [
            {
                "id": designer.id,
                "designer_name": designer.designer_name,
                "company": designer.company,
                "email": designer.email,
                "phone": designer.phone
            }
            for designer in designers
        ]

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
        # get designer information
        designer = session.query(Designer).filter_by(id=designer_id).first()

        if designer is None:
            return jsonify({"error": "Designer not found"}), 404

        # get sidemarks associated with the designer
        sidemarks = session.query(Sidemark).filter_by(designer_id=designer_id).all()

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

        workorder = session.query(Workorder).filter_by(id=workorder_id).first()

        workorder_items = (
            session.query(WorkorderItem, Inventory)
            .join(Inventory, WorkorderItem.inventory_id == Inventory.id)
            .filter(WorkorderItem.workorder_id == workorder_id)
            .all()
        )

        inventory_data = [
            {
                "id": item.Inventory.id,
                "item_name": item.Inventory.item_name,
                "sku": item.Inventory.sku,
                "manufacture": item.Inventory.manufacture,
                "quantity": item.Inventory.quantity,
                "length": item.Inventory.length,
                "width": item.Inventory.width,
                "height": item.Inventory.height,
                "weight": item.Inventory.weight,
                "description": item.Inventory.description
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
            # find designer by company name
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
        # query the requested Workorder
        workorder = session.query(Workorder).filter_by(id=workorder_id).first()

        if not workorder:
            return jsonify({"status": "fail", "message": "Workorder not found."}), 404

        # get WorkorderItems and associated Inventory
        workorder_items = (
            session.query(WorkorderItem, Inventory)
            .join(Inventory, WorkorderItem.inventory_id == Inventory.id)
            .filter(WorkorderItem.workorder_id == workorder_id)
            .all()
        )

        inventory_data = [
            {"id": item.Inventory.id, "item_name": item.Inventory.item_name, "quantity": item.WorkorderItem.quantity}
            for item in workorder_items]

        return jsonify({
            "status": "success",
            "workorder_id": workorder_id,
            "inventory": inventory_data
        }), 200
