"""
controllers/above_average_controller.py
Level 3 – Sub-Task B
"""
from flask import Blueprint, render_template, request
from models.above_average_model import (
    get_infection_types,
    get_available_years,
    get_above_average_data,
    get_summary_stats,
)

above_average_bp = Blueprint('above_average', __name__)


@above_average_bp.route('/level3', methods=['GET'])
def level3():
    infection_types = get_infection_types()
    years           = get_available_years()

    default_disease = 'Measles' if 'Measles' in infection_types else (infection_types[0] if infection_types else '')
    selected_disease = request.args.get('disease', default_disease)
    selected_year    = request.args.get('year',    years[0] if years else 2022)
    sort_col         = request.args.get('sort_col', 'cases_per_100k')
    sort_dir         = request.args.get('sort_dir', 'DESC')

    try:
        selected_year = int(selected_year)
    except (ValueError, TypeError):
        selected_year = years[0] if years else 2022

    rows  = get_above_average_data(selected_year, selected_disease, sort_col, sort_dir)
    stats = get_summary_stats(selected_year, selected_disease)

    # Tách hàng Global ra khỏi danh sách (luôn là hàng đầu tiên)
    global_row     = rows[0] if rows else None
    country_rows   = rows[1:] if len(rows) > 1 else []

    return render_template(
        'level3.html',
        infection_types  = infection_types,
        years            = years,
        selected_disease = selected_disease,
        selected_year    = selected_year,
        sort_col         = sort_col,
        sort_dir         = sort_dir,
        global_row       = global_row,
        country_rows     = country_rows,
        stats            = stats,
    )
