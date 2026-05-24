from flask import Blueprint, render_template, request
from models.vaccination_model import (
    get_vaccination_filter_options,
    get_countries_meeting_target,
    get_regional_summary
)

vaccination_bp = Blueprint("vaccination", __name__)


@vaccination_bp.route("/vaccination")
def vaccination():
    country_id = request.args.get("country_id") or None
    region = request.args.get("region") or None
    antigen_id = request.args.get("antigen_id") or None
    year = request.args.get("year") or None
    sort = request.args.get("sort", "desc")

    if country_id:
        country_id = int(country_id)

    if antigen_id:
        antigen_id = int(antigen_id)

    if year:
        year = int(year)

    countries, regions, antigens, years = get_vaccination_filter_options()

    table1 = get_countries_meeting_target(
        country_id=country_id,
        region=region,
        antigen_id=antigen_id,
        year=year,
        sort=sort
    )

    table2 = get_regional_summary(
        region=region,
        antigen_id=antigen_id,
        year=year
    )

    return render_template(
        "vaccination.html",
        countries=countries,
        regions=regions,
        antigens=antigens,
        years=years,
        table1=table1,
        table2=table2,
        selected_country=country_id,
        selected_region=region,
        selected_antigen=antigen_id,
        selected_year=year,
        sort=sort,
        active_page="vaccination"
    )