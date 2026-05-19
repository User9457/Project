"""
controllers/mission_controller.py
Level 1 – Sub-Task B
"""
from flask import Blueprint, render_template
from models.mission_model import get_personas, get_team_members

mission_bp = Blueprint('mission', __name__)


@mission_bp.route('/')
def index():
    personas     = get_personas()
    team_members = get_team_members()
    return render_template('mission.html', personas=personas, team_members=team_members)
