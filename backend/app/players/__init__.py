from flask import Blueprint

players_bp = Blueprint('players', __name__)

# Import routes at the bottom to avoid circular imports
from . import routes