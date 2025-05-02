from flask import Blueprint
from ..utils import success_response

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    return success_response({"message": "root"})
