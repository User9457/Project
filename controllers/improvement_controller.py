from flask import Blueprint, render_template, request
from models.improvement_model import (
    get_improvement_filter_options,
    get_biggest_improvements
)

improvement_bp = Blueprint("improvement", __name__)


@improvement_bp.route("/improvement")
def improvement():
    years, antigens = get_improvement_filter_options()

    start_year = request.args.get("start_year")
    end_year = request.args.get("end_year")
    antigen_id = request.args.get("antigen_id")
    top_n = request.args.get("top_n", 10)

    results = []

    if start_year and end_year and antigen_id:
        start_year = int(start_year)
        end_year = int(end_year)
        antigen_id = int(antigen_id)
        top_n = int(top_n)

        results = get_biggest_improvements(
            start_year=start_year,
            end_year=end_year,
            antigen_id=antigen_id,
            top_n=top_n
        )

    return render_template(
        "improvement.html",
        years=years,
        antigens=antigens,
        results=results,
        selected_start_year=start_year,
        selected_end_year=end_year,
        selected_antigen=antigen_id,
        selected_top_n=top_n,
        active_page="improvement"
    )