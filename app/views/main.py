from flask import Blueprint, redirect, url_for

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET'])
def index():
    """Redirect home page to login page."""
    return redirect(url_for('login.index'))
