"""
controllers/economic_controller.py
Level 2 – Sub-Task B
"""
from flask import Blueprint, render_template, request
from models.economic_model import (
    get_economic_statuses,
    get_infection_types,
    get_available_years,
    get_country_infections,
    get_summary_by_economic_phase,
)

economic_bp = Blueprint('economic', __name__)


@economic_bp.route('/level2', methods=['GET'])
def level2():
    # Dropdown options
    economic_statuses = get_economic_statuses()
    infection_types   = get_infection_types()
    years             = get_available_years()

    # Filter params từ query string
    selected_econ    = request.args.get('economic_status', 'all')
    default_disease  = 'Measles' if 'Measles' in infection_types else (infection_types[0] if infection_types else '')
    selected_disease = request.args.get('disease', default_disease)
    selected_year    = request.args.get('year',    years[0] if years else 2022)
    sort_col         = request.args.get('sort_col', 'cases_per_100k')
    sort_dir         = request.args.get('sort_dir', 'DESC')

    try:
        selected_year = int(selected_year)
    except (ValueError, TypeError):
        selected_year = years[0] if years else 2022

    # Truy vấn dữ liệu
    country_data = get_country_infections(selected_econ, selected_disease, selected_year, sort_col, sort_dir)
    summary_data = get_summary_by_economic_phase(selected_disease, selected_year)

    return render_template(
        'level2.html',
        economic_statuses = economic_statuses,
        infection_types   = infection_types,
        years             = years,
        selected_econ     = selected_econ,
        selected_disease  = selected_disease,
        selected_year     = selected_year,
        sort_col          = sort_col,
        sort_dir          = sort_dir,
        country_data      = country_data,
        summary_data      = summary_data,
    )
