import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("../villageconnect.db")
cursor = conn.cursor()

# Check if admin already exists
admin_email = "admin01@gmail.com"
admin_exists = cursor.execute("SELECT * FROM users WHERE email = ?", (admin_email,)).fetchone()

if not admin_exists:
    cursor.execute("""
        INSERT INTO users (name, email, password, role)
        VALUES (?, ?, ?, ?)
    """, ("ADMIN", admin_email, generate_password_hash("ADMIN@01"), "admin"))
    conn.commit()
    print("✅ Admin created.")
else:
    print("✅ Admin already exists.")

conn.close()
