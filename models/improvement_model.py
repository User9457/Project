from db import get_connection


def get_improvement_filter_options():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT year
        FROM VaccinationData
        ORDER BY year DESC
    """)
    years = cursor.fetchall()

    cursor.execute("""
        SELECT antigen_id, antigen_name
        FROM Antigens
        ORDER BY antigen_name
    """)
    antigens = cursor.fetchall()

    conn.close()
    return years, antigens


def get_biggest_improvements(start_year, end_year, antigen_id, top_n):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT TOP (?)
            c.country_name,
            a.antigen_name,
            start_v.year AS start_year,
            end_v.year AS end_year,
            CAST(start_v.vaccinated_count * 100.0 / c.population AS DECIMAL(10,2)) AS start_rate,
            CAST(end_v.vaccinated_count * 100.0 / c.population AS DECIMAL(10,2)) AS end_rate,
            CAST(
                (end_v.vaccinated_count * 100.0 / c.population)
                -
                (start_v.vaccinated_count * 100.0 / c.population)
            AS DECIMAL(10,2)) AS rate_increase
        FROM VaccinationData start_v
        JOIN VaccinationData end_v
            ON start_v.country_id = end_v.country_id
            AND start_v.antigen_id = end_v.antigen_id
        JOIN Countries c
            ON start_v.country_id = c.country_id
        JOIN Antigens a
            ON start_v.antigen_id = a.antigen_id
        WHERE
            start_v.year = ?
            AND end_v.year = ?
            AND start_v.antigen_id = ?
            AND (
                (end_v.vaccinated_count * 100.0 / c.population)
                -
                (start_v.vaccinated_count * 100.0 / c.population)
            ) > 0
        ORDER BY rate_increase DESC
    """

    cursor.execute(query, top_n, start_year, end_year, antigen_id)
    rows = cursor.fetchall()

    conn.close()
    return rows