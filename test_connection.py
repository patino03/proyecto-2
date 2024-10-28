from database import DatabaseOperations

try:
    db = DatabaseOperations()
    print("Connection successful!")
    
    # Test query
    cursor = db.connection.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    print("Available tables:", tables)
    
except Exception as e:
    print(f"Connection failed: {e}")
finally:
    if 'db' in locals():
        db.close()
