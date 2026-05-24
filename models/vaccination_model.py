from db import get_connection


def get_vaccination_filter_options():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT country_id, country_name
        FROM Countries
        ORDER BY country_name
    """)
    countries = cursor.fetchall()

    cursor.execute("""
        SELECT DISTINCT region
        FROM Countries
        WHERE region IS NOT NULL
        ORDER BY region
    """)
    regions = cursor.fetchall()

    cursor.execute("""
        SELECT antigen_id, antigen_name
        FROM Antigens
        ORDER BY antigen_name
    """)
    antigens = cursor.fetchall()

    cursor.execute("""
        SELECT DISTINCT year
        FROM VaccinationData
        ORDER BY year DESC
    """)
    years = cursor.fetchall()

    conn.close()
    return countries, regions, antigens, years


def get_countries_meeting_target(country_id=None, region=None, antigen_id=None, year=None, sort="desc"):
    conn = get_connection()
    cursor = conn.cursor()

    order_direction = "ASC" if sort == "asc" else "DESC"

    query = f"""
        SELECT
            a.antigen_name,
            v.year,
            c.country_name,
            c.region,
            CAST(v.vaccinated_count * 100.0 / c.population AS DECIMAL(10,2)) AS vaccination_rate
        FROM VaccinationData v
        JOIN Countries c ON v.country_id = c.country_id
        JOIN Antigens a ON v.antigen_id = a.antigen_id
        WHERE
            (? IS NULL OR v.country_id = ?)
            AND (? IS NULL OR c.region = ?)
            AND (? IS NULL OR v.antigen_id = ?)
            AND (? IS NULL OR v.year = ?)
            AND (v.vaccinated_count * 100.0 / c.population) >= 90
        ORDER BY vaccination_rate {order_direction}
    """

    cursor.execute(
        query,
        country_id, country_id,
        region, region,
        antigen_id, antigen_id,
        year, year
    )

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_regional_summary(region=None, antigen_id=None, year=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            a.antigen_name,
            v.year,
            c.region,
            COUNT(DISTINCT c.country_id) AS countries_meeting_target
        FROM VaccinationData v
        JOIN Countries c ON v.country_id = c.country_id
        JOIN Antigens a ON v.antigen_id = a.antigen_id
        WHERE
            (? IS NULL OR c.region = ?)
            AND (? IS NULL OR v.antigen_id = ?)
            AND (? IS NULL OR v.year = ?)
            AND (v.vaccinated_count * 100.0 / c.population) >= 90
        GROUP BY
            a.antigen_name,
            v.year,
            c.region
        ORDER BY countries_meeting_target DESC
    """

    cursor.execute(
        query,
        region, region,
        antigen_id, antigen_id,
        year, year
    )

    rows = cursor.fetchall()
    conn.close()
    return rows