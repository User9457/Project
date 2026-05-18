"""
models/above_average_model.py
Level 3 – Sub-Task B: Identify countries with above average infection rate

Yêu cầu kỹ thuật (rubric):
  - Một câu SQL duy nhất dùng CTE (GlobalAvg, CountryRates, Combined) + UNION ALL.
  - Outer SELECT wrapper để ORDER BY hoạt động đúng trên SQL Server với UNION ALL.
  - Không có post-processing Python – toàn bộ logic tính toán ở SQL.
  - Hàng 'Global' luôn đứng đầu bảng (row_order = 0).
  - Sắp xếp các quốc gia theo tiêu chí người dùng chọn (sort_col / sort_dir).
"""
from db import get_connection


# ── Helpers for dropdowns ────────────────────────────────────────────────────

def get_infection_types():
    """Lấy danh sách tên bệnh từ bảng Diseases (dùng cho select dropdown)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT disease_name FROM Diseases ORDER BY disease_name")
    result = [row[0] for row in cursor.fetchall()]
    conn.close()
    return result


def get_available_years():
    """Lấy danh sách các năm có dữ liệu từ bảng InfectionData."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT year FROM InfectionData ORDER BY year DESC")
    result = [row[0] for row in cursor.fetchall()]
    conn.close()
    return result


# ── Main Level 3 query ───────────────────────────────────────────────────────

def get_above_average_data(year: int, disease_name: str,
                           sort_col: str = 'cases_per_100k',
                           sort_dir: str = 'DESC'):
    """
    Trả về danh sách đã sắp xếp:
      [0]  hàng Global  – cases_per_100k = trung bình toàn cầu, pct_above_avg = NULL
      [1+] quốc gia có cases_per_100k > global average

    SQL gồm:
      - CTE GlobalAvg   : AVG(cases/100k) toàn cầu với JOIN 3 bảng
      - CTE CountryRates: tỷ lệ từng quốc gia với JOIN 3 bảng
      - CTE Combined    : UNION ALL (hàng Global ∪ các quốc gia vượt mức)
      - Outer SELECT    : ORDER BY hợp lệ trên SQL Server khi dùng UNION ALL
    Không dùng Python để tính toán hay post-process.
    """
    # Whitelist validation – chống SQL injection
    allowed_cols = {'cases_per_100k', 'country_name', 'pct_above_avg'}
    allowed_dirs = {'ASC', 'DESC'}
    sort_col = sort_col if sort_col in allowed_cols else 'cases_per_100k'
    sort_dir = sort_dir.upper() if sort_dir.upper() in allowed_dirs else 'DESC'

    # ORDER BY cho outer SELECT (SQL Server hỗ trợ alias khi bọc bằng outer query)
    # row_order = 0 (Global) luôn đứng trước; quốc gia sắp theo sort_col + sort_dir
    order_clause = f"row_order ASC, CASE WHEN row_order = 1 THEN {sort_col} END {sort_dir}"

    sql = f"""
    WITH GlobalAvg AS (
        -- Tính tỷ lệ nhiễm trung bình toàn cầu (cases / 100,000 dân)
        SELECT
            AVG(
                CAST(i.total_cases AS FLOAT) / NULLIF(c.population, 0) * 100000
            ) AS global_rate
        FROM InfectionData i
        JOIN Countries c ON i.country_id = c.country_id
        JOIN Diseases  d ON i.disease_id = d.disease_id
        WHERE d.disease_name = ?
          AND i.year         = ?
    ),
    CountryRates AS (
        -- Tỷ lệ nhiễm của từng quốc gia (cases / 100,000 dân)
        SELECT
            c.country_name,
            d.disease_name                AS infection_type,
            i.year,
            ROUND(
                CAST(i.total_cases AS FLOAT) / NULLIF(c.population, 0) * 100000
            , 2)                          AS cases_per_100k
        FROM InfectionData i
        JOIN Countries c ON i.country_id = c.country_id
        JOIN Diseases  d ON i.disease_id = d.disease_id
        WHERE d.disease_name = ?
          AND i.year         = ?
    ),
    Combined AS (
        -- Hàng Global (row_order = 0 → sẽ luôn đứng đầu sau ORDER BY)
        SELECT
            'Global'                AS country_name,
            ?                       AS infection_type,
            ?                       AS year,
            ROUND(g.global_rate, 2) AS cases_per_100k,
            CAST(NULL AS FLOAT)     AS pct_above_avg,
            0                       AS row_order
        FROM GlobalAvg g

        UNION ALL

        -- Các quốc gia có tỷ lệ vượt trung bình toàn cầu
        SELECT
            cr.country_name,
            cr.infection_type,
            cr.year,
            cr.cases_per_100k,
            ROUND(
                (cr.cases_per_100k - g.global_rate) / NULLIF(g.global_rate, 0) * 100
            , 1)                    AS pct_above_avg,
            1                       AS row_order
        FROM CountryRates cr
        CROSS JOIN GlobalAvg g
        WHERE cr.cases_per_100k > g.global_rate
    )
    -- Outer SELECT: SQL Server cho phép ORDER BY trên alias của CTE Combined
    SELECT
        country_name,
        infection_type,
        year,
        cases_per_100k,
        pct_above_avg,
        row_order
    FROM Combined
    ORDER BY {order_clause}
    """

    # 6 params: GlobalAvg(disease, year) | CountryRates(disease, year) | Combined literal (disease, year)
    params = [disease_name, year, disease_name, year, disease_name, year]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return rows


# ── KPI summary stats ────────────────────────────────────────────────────────

def get_summary_stats(year: int, disease_name: str):
    """
    Trả về dict thống kê cho KPI cards:
      global_avg      – tỷ lệ trung bình toàn cầu (float, 2 chữ số)
      countries_above – số quốc gia có rate > global_avg
      total_countries – tổng số quốc gia có dữ liệu
      highest_country – tên quốc gia có tỷ lệ cao nhất
      highest_rate    – tỷ lệ cao nhất

    Toàn bộ tính toán ở SQL (CTE GlobalAvg + CountryRates + Stats).
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        WITH GlobalAvg AS (
            SELECT AVG(
                CAST(i.total_cases AS FLOAT) / NULLIF(c.population, 0) * 100000
            ) AS global_rate
            FROM InfectionData i
            JOIN Countries c ON i.country_id = c.country_id
            JOIN Diseases  d ON i.disease_id = d.disease_id
            WHERE d.disease_name = ? AND i.year = ?
        ),
        CountryRates AS (
            SELECT
                c.country_name,
                ROUND(
                    CAST(i.total_cases AS FLOAT) / NULLIF(c.population, 0) * 100000
                , 2) AS rate
            FROM InfectionData i
            JOIN Countries c ON i.country_id = c.country_id
            JOIN Diseases  d ON i.disease_id = d.disease_id
            WHERE d.disease_name = ? AND i.year = ?
        ),
        Stats AS (
            SELECT
                ROUND(g.global_rate, 2)                                    AS global_avg,
                SUM(CASE WHEN cr.rate > g.global_rate THEN 1 ELSE 0 END)   AS countries_above,
                COUNT(cr.country_name)                                      AS total_countries,
                MAX(cr.rate)                                                AS highest_rate
            FROM CountryRates cr
            CROSS JOIN GlobalAvg g
            GROUP BY g.global_rate
        )
        SELECT
            s.global_avg,
            s.countries_above,
            s.total_countries,
            -- TOP 1 subquery để lấy tên quốc gia cao nhất (hợp lệ trong SQL Server)
            (SELECT TOP 1 cr2.country_name
             FROM CountryRates cr2
             ORDER BY cr2.rate DESC)  AS highest_country,
            s.highest_rate
        FROM Stats s
    """, [disease_name, year, disease_name, year])

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            'global_avg':      round(float(row[0]), 2) if row[0] is not None else 0.0,
            'countries_above': int(row[1])             if row[1] is not None else 0,
            'total_countries': int(row[2])             if row[2] is not None else 0,
            'highest_country': row[3]                  if row[3] is not None else '–',
            'highest_rate':    round(float(row[4]), 2) if row[4] is not None else 0.0,
        }
    return {
        'global_avg': 0.0, 'countries_above': 0,
        'total_countries': 0, 'highest_country': '–', 'highest_rate': 0.0,
    }
