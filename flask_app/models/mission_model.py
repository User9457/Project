"""
models/mission_model.py
Level 1 – Sub-Task B: Mission Statement
Truy xuất Personas & Team Members từ database.
"""
from db import get_connection


def get_personas():
    """Lấy danh sách personas từ bảng Personas."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT persona_id, name, role, organisation, description, tag1, tag2, icon_color
        FROM Personas
        ORDER BY persona_id
    """)
    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_team_members():
    """Lấy danh sách thành viên nhóm từ bảng TeamMembers."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT member_id, full_name, student_id
        FROM TeamMembers
        ORDER BY member_id
    """)
    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return rows
