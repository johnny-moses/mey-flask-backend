from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__)

from . import dashboard_routes
