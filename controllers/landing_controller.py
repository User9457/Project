from flask import Blueprint, render_template
from models.landing_model import get_landing_kpis

landing_bp = Blueprint("landing", __name__)


@landing_bp.route("/landing")
def landing():
    kpis = get_landing_kpis()
    return render_template("landing.html", kpis=kpis, active_page="landing")