import mysql.connector

try:
    print("Connecting to DB...")
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="actbayan"
    )
    print("Connected! Executing ALTER TABLE...")
    cursor = db.cursor()
    cursor.execute("ALTER TABLE reports ADD COLUMN public_key VARCHAR(255) DEFAULT NULL")
    db.commit()
    print("Column 'public_key' added successfully!")
except mysql.connector.Error as err:
    if err.errno == 1060: # Duplicate column name
        print("Column 'public_key' already exists!")
    else:
        print(f"Error: {err}")
finally:
    if 'db' in locals() and db.is_connected():
        cursor.close()
        db.close()
