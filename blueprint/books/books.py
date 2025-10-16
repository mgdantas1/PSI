from flask import Blueprint
from database import *
from app import *


book_bp = Blueprint('users', __name__)

# @book_bp.route('')