import mysql.connector

con = mysql.connector.connect(host='localhost', user='root', password='', database='acttest')
cursor = con.cursor()

try:
    cursor.execute("SHOW COLUMNS FROM reports LIKE 'embedding'")
    result = cursor.fetchone()
    if result:
        print("Column 'embedding' already exists:", result)
    else:
        cursor.execute("ALTER TABLE reports ADD COLUMN embedding TEXT DEFAULT NULL")
        con.commit()
        print("Column 'embedding' added successfully!")
except Exception as e:
    print(f"Error: {e}")

con.close()

