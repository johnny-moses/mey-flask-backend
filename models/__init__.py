from flask import Blueprint

models = Blueprint('models', __name__)

from .inventory import *
from .orders import *
from .designer import *
