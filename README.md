# Flask App – WHO Infectious Disease Dashboard

## Cấu trúc MVC

```
flask_app/
├── app.py                          # Entry point
├── config.py                       # Cấu hình kết nối SQL Server
├── db.py                           # Helper kết nối database
├── .env                            # Biến môi trường (không commit)
├── requirements.txt
├── setup_database.sql              # Script tạo bảng & dữ liệu mẫu
│
├── controllers/
│   ├── mission_controller.py       # Level 1 – Mission Statement
│   ├── economic_controller.py      # Level 2 – Economic Infection Data
│   └── above_average_controller.py # Level 3 – Above Average Analysis
│
├── models/
│   ├── mission_model.py            # Truy vấn Personas + TeamMembers
│   ├── economic_model.py           # Truy vấn lọc/sắp xếp/tổng hợp kinh tế
│   └── above_average_model.py      # Truy vấn CTE + UNION ALL (Level 3)
│
└── templates/
    ├── base.html                   # Layout chung (sidebar navigation)
    ├── mission.html                # Level 1
    ├── level2.html                 # Level 2
    └── level3.html                 # Level 3
```

## Cài đặt

```bash
# 1. Tạo virtual environment
python -m venv venv
venv\Scripts\activate     # Windows

# 2. Cài dependencies
pip install -r requirements.txt

# 3. Cấu hình database
# Chỉnh sửa file .env theo thông tin SQL Server của bạn

# 4. Tạo database và bảng
# Mở SQL Server Management Studio, tạo database WHO_Immunisation
# rồi chạy file setup_database.sql

# 5. Chạy ứng dụng
python app.py
# Truy cập: http://localhost:5000
```

## Cấu hình .env

```env
SQL_SERVER=localhost
SQL_DATABASE=WHO_Immunisation
SQL_DRIVER=ODBC Driver 17 for SQL Server
SQL_TRUSTED=yes           # Windows Authentication
# Nếu dùng SQL Auth:
# SQL_TRUSTED=no
# SQL_USERNAME=sa
# SQL_PASSWORD=your_password
```

## Pages & Routes

| URL         | Page                      | Level  |
|-------------|---------------------------|--------|
| `/`         | Mission Statement         | L1 – B |
| `/level2`   | Economic Infection Data   | L2 – B |
| `/level3`   | Above Average Analysis    | L3 – B |

## SQL Highlights

### Level 2 – Aggregation (summary by economic phase)
```sql
SELECT c.economic_status, d.disease_name, i.year,
       COUNT(DISTINCT c.country_id) AS total_countries,
       SUM(i.total_cases)           AS total_cases
FROM InfectionData i
JOIN Countries c ON i.country_id = c.country_id
JOIN Diseases  d ON i.disease_id = d.disease_id
WHERE d.disease_name = ? AND i.year = ?
GROUP BY c.economic_status, d.disease_name, i.year
```

### Level 3 – Single CTE query (global avg + countries above)
```sql
WITH GlobalAvg AS (
    SELECT AVG(CAST(total_cases AS FLOAT) / population * 100000) AS global_rate ...
),
CountryRates AS (
    SELECT country_name, cases_per_100k ...
)
SELECT 'Global' AS country_name, global_rate, ...  -- pinned row
UNION ALL
SELECT country_name, cases_per_100k, pct_above_avg, ...
FROM CountryRates CROSS JOIN GlobalAvg
WHERE cases_per_100k > global_rate
ORDER BY row_order ASC, cases_per_100k DESC
```
