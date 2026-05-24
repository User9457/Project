from db import get_connection


def get_landing_kpis():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            MIN(year) AS start_year,
            MAX(year) AS end_year
        FROM VaccinationData
    """)
    year_range = cursor.fetchone()

    cursor.execute("""
        SELECT COUNT(*) AS total_countries
        FROM Countries
    """)
    total_countries = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) AS total_vaccine_records
        FROM VaccinationData
    """)
    total_vaccine_records = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) AS antigen_count
        FROM Antigens
    """)
    antigen_count = cursor.fetchone()[0]

    conn.close()

    return {
        "start_year": year_range.start_year,
        "end_year": year_range.end_year,
        "total_countries": total_countries,
        "total_vaccine_records": total_vaccine_records,
        "antigen_count": antigen_count
    }