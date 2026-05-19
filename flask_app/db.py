import pyodbc
from config import Config


def get_connection():
    """Trả về một kết nối pyodbc mới đến SQL Server."""
    conn_str = Config.get_connection_string()
    return pyodbc.connect(conn_str)
