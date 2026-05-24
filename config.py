import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # SQL Server connection – chỉnh lại SERVER / DATABASE theo môi trường thực tế
    SQL_SERVER   = os.getenv("SQL_SERVER",   r".\SQLEXPRESS")
    SQL_DATABASE = os.getenv("SQL_DATABASE", "WHO_Immunisation")
    SQL_DRIVER   = os.getenv("SQL_DRIVER",   "ODBC Driver 17 for SQL Server")
    SQL_TRUSTED  = os.getenv("SQL_TRUSTED",  "yes")   # Dùng Windows Auth
    SQL_USERNAME = os.getenv("SQL_USERNAME", "")       # Để trống nếu dùng Trusted
    SQL_PASSWORD = os.getenv("SQL_PASSWORD", "")

    @classmethod
    def get_connection_string(cls):
        if cls.SQL_TRUSTED.lower() in ("yes", "true", "1"):
            return (
                f"DRIVER={{{cls.SQL_DRIVER}}};"
                f"SERVER={cls.SQL_SERVER};"
                f"DATABASE={cls.SQL_DATABASE};"
                f"Trusted_Connection=yes;"
            )
        return (
            f"DRIVER={{{cls.SQL_DRIVER}}};"
            f"SERVER={cls.SQL_SERVER};"
            f"DATABASE={cls.SQL_DATABASE};"
            f"UID={cls.SQL_USERNAME};"
            f"PWD={cls.SQL_PASSWORD};"
        )
