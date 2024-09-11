from flask import Blueprint

models = Blueprint('models', __name__)

from .designer import *
