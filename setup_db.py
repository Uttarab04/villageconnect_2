import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect('villageconnect.db')
cursor = conn.cursor()

# ------------------------------
# 1. Announcements Table
# ------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS announcements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    date_posted TEXT NOT NULL
);
""")

cursor.execute("""
INSERT INTO announcements (title, message, date_posted) VALUES
('Water Supply Notice', 'Water supply will be interrupted on 25th June for repairs.', '2025-06-24'),
('Health Camp', 'Free health camp on 28th June at the community center.', '2025-06-22');
""")

# ------------------------------
# 2. Jobs Table
# ------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    salary TEXT,
    location TEXT
);
""")

cursor.execute("""
INSERT INTO jobs (title, description, salary, location) VALUES
('Farm Assistant', 'Help needed for rice planting, 10 days', '₹300/day', 'Ward 5'),
('Tailor Needed', 'Part-time tailoring for school uniforms', '₹5000/month', 'Main Bazaar');
""")

# ------------------------------
# 3. Grievances Table
# ------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS grievances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact TEXT NOT NULL,
    message TEXT NOT NULL,
    status TEXT DEFAULT 'Pending'
);
""")

cursor.execute("""
INSERT INTO grievances (name, contact, message) VALUES
('Sita Devi', '9876543210', 'Streetlight not working in front of my house'),
('Ramesh Kumar', '9876541111', 'Drainage issue near the school');
""")

# ------------------------------
# 4. Users Table (Optional)
# ------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    role TEXT DEFAULT 'villager'  -- Can be 'admin', 'staff', etc.
);
""")

cursor.execute("""
INSERT INTO users (name, email, role) VALUES
('Asha Worker', 'asha@villageconnect.in', 'staff'),
('Panchayat Admin', 'admin@villageconnect.in', 'admin'),
('Ram Lal', 'ramlal@gmail.com', 'villager');
""")


# Commit changes and close the connection
conn.commit()
conn.close()

print("✅ Database created and sample data inserted into: announcements, jobs, grievances")
