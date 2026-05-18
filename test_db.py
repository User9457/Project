import pyodbc
from config import Config

def test_connection():
    conn_str = Config.get_connection_string()
    print("Connection String:")
    print(conn_str)
    print("-" * 50)
    
    try:
        conn = pyodbc.connect(conn_str, timeout=5)
        print("[SUCCESS] Connected to SQL Server!")
        
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 1 * FROM Diseases")
        row = cursor.fetchone()
        if row:
            print(f"[SUCCESS] Sample data retrieved: {row}")
        else:
            print("[WARNING] Connected but Diseases table is empty.")
            
        conn.close()
    except Exception as e:
        print("[ERROR] Failed to connect:")
        print(e)

if __name__ == "__main__":
    test_connection()
