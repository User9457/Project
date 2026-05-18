"""
models/economic_model.py
Level 2 – Sub-Task B: Focused view of infection data by economic status
"""
from db import get_connection


def get_economic_statuses():
    """Lấy danh sách các tình trạng kinh tế khác biệt từ database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT economic_status
        FROM Countries
        WHERE economic_status IS NOT NULL
        ORDER BY economic_status
    """)
    result = [row[0] for row in cursor.fetchall()]
    conn.close()
    return result


def get_infection_types():
    """Lấy danh sách các loại bệnh (cột) từ bảng InfectionData."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT disease_name
        FROM Diseases
        ORDER BY disease_name
    """)
    result = [row[0] for row in cursor.fetchall()]
    conn.close()
    return result


def get_available_years():
    """Lấy danh sách các năm có dữ liệu."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT year
        FROM InfectionData
        ORDER BY year DESC
    """)
    result = [row[0] for row in cursor.fetchall()]
    conn.close()
    return result


def get_country_infections(economic_status, disease_name, year, sort_col='cases_per_100k', sort_dir='DESC'):
    """
    Bảng 1: Dữ liệu ca nhiễm theo từng quốc gia, lọc theo economic_status + disease + năm.
    Hỗ trợ sort theo bất kỳ cột nào.
    """
    allowed_cols = {'country_name', 'economic_status', 'cases_per_100k', 'year'}
    allowed_dirs = {'ASC', 'DESC'}
    sort_col = sort_col if sort_col in allowed_cols else 'cases_per_100k'
    sort_dir = sort_dir.upper() if sort_dir.upper() in allowed_dirs else 'DESC'

    conn = get_connection()
    cursor = conn.cursor()

    params = [year, disease_name]
    where_econ = ""
    if economic_status and economic_status != 'all':
        where_econ = "AND c.economic_status = ?"
        params.append(economic_status)

    sql = f"""
        SELECT
            c.country_name,
            c.economic_status,
            d.disease_name  AS infection_type,
            i.year,
            -- ISNULL: nếu total_cases hoặc population là NULL → trả về 0 thay vì NULL
            ROUND(
                CAST(ISNULL(i.total_cases, 0) AS FLOAT) / NULLIF(c.population, 0) * 100000
            , 2) AS cases_per_100k
        FROM InfectionData  i
        JOIN Countries       c ON i.country_id  = c.country_id
        JOIN Diseases        d ON i.disease_id  = d.disease_id
        WHERE i.year = ?
          AND d.disease_name = ?
          {where_econ}
        ORDER BY {sort_col} {sort_dir}
    """
    cursor.execute(sql, params)
    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_summary_by_economic_phase(disease_name, year):
    """
    Bảng 2: Tổng hợp – tổng ca nhiễm theo từng nhóm kinh tế cho một bệnh & năm cụ thể.
    Dùng JOIN + GROUP BY + SUM (aggregation).
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            c.economic_status                AS economic_phase,
            d.disease_name                   AS preventable_disease,
            i.year,
            COUNT(DISTINCT c.country_id)     AS total_countries,
            -- ISNULL: xử lý dữ liệu thiếu (NULL total_cases) bằng cách coi = 0
            SUM(ISNULL(i.total_cases, 0))    AS total_cases
        FROM InfectionData  i
        JOIN Countries       c ON i.country_id = c.country_id
        JOIN Diseases        d ON i.disease_id = d.disease_id
        WHERE d.disease_name = ?
          AND i.year         = ?
          AND c.economic_status IS NOT NULL
        GROUP BY c.economic_status, d.disease_name, i.year
        ORDER BY total_cases DESC
    """, [disease_name, year])
    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return rows
