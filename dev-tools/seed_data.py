import sqlite3
from datetime import datetime
import random

conn = sqlite3.connect("../villageconnect.db")
cursor = conn.cursor()

# ---------------------------------
# 🔄 Step 1: Clear existing data
# ---------------------------------
cursor.execute("DELETE FROM announcements;")
cursor.execute("DELETE FROM jobs;")
cursor.execute("DELETE FROM posts;")
conn.commit()

# ---------------------------------
# 📢 Announcements with titles
# ---------------------------------
announcement_data = [
    ("Water Supply Notice", "Water supply will be interrupted on 25th June for repairs."),
    ("Health Camp", "Free health camp on 28th June at the community center."),
    ("Grain Distribution", "Grain distribution starts tomorrow."),
    ("Village Meeting", "Village meeting at Panchayat Bhavan this Sunday."),
    ("Vaccination Drive", "Free vaccination drive for kids under 5."),
    ("Electricity Maintenance", "Electricity outage due to transformer check."),
    ("Ration Card Update", "New ration cards are being issued."),
    ("Soil Testing", "Soil testing for farmers next week."),
    ("Yoga Classes", "Yoga classes start on Monday at the school ground."),
    ("Tree Plantation", "Tree plantation drive this weekend."),
    ("Scholarship Forms", "Scholarship forms available at Taluka office."),
    ("Blood Donation", "Blood donation camp on 15th at PHC."),
    ("Govt Scheme Awareness", "Govt scheme awareness session on Saturday."),
    ("Cattle Health Check", "Cattle health checkup camp next month."),
    ("Library Notice", "Village library reopened."),
    ("Cleanliness Drive", "Cleanliness drive on 1st of next month."),
    ("Aadhar Update", "Aadhar update camp on Tuesday."),
    ("Skill Training", "Skill training registration open now."),
    ("Water Harvesting", "Rainwater harvesting awareness session."),
    ("Grievance System", "Online grievance system is now live.")
]

for title, msg in announcement_data:
    cursor.execute("""
        INSERT INTO announcements (title, message, date_posted)
        VALUES (?, ?, ?)
    """, (title, msg, datetime.now().strftime("%Y-%m-%d")))

# ---------------------------------
# 💼 Jobs
# ---------------------------------
job_titles = [
    "Electrician", "Health Worker", "Teacher Assistant", "Farmer Helper", "Anganwadi Worker",
    "Tailor", "Construction Labor", "Ration Distributor", "Data Entry Operator", "Cleaner",
    "Mobile Repair Technician", "Field Surveyor", "Cook", "Gardener", "Welder",
    "Painter", "Driver", "Mason", "Nurse", "Clerk"
]

locations = ["Sector 1", "Sector 2", "Main Street", "Ward 5", "Taluka Road", "Hill Area"]
salaries = ["₹6000/month", "₹8000/month", "₹500/day", "₹10000", "₹400/day"]

for job in job_titles:
    cursor.execute("""
        INSERT INTO jobs (title, description, salary, location)
        VALUES (?, ?, ?, ?)
    """, (
        job,
        f"We're hiring a {job.lower()} in your village. Apply now!",
        random.choice(salaries),
        random.choice(locations)
    ))

# ---------------------------------
# 🗣 Forum Posts
# ---------------------------------
forum_posts = [
    "Can anyone help with land record corrections?",
    "What is the latest update on ration card forms?",
    "Is the doctor available tomorrow?",
    "Anyone know about the new loan scheme?",
    "What time is the village meeting?",
    "Looking for part-time job suggestions.",
    "Water supply issues in Sector 4!",
    "Health camp feedback?",
    "Can we get street lights near the temple?",
    "Any tuition teacher available for Class 5?"
]

names = ["Ravi", "Sunita", "Geeta", "Suresh", "Kiran", "Vikram", "Asha", "Deepak", "Ramesh"]

for post in forum_posts:
    cursor.execute("""
        INSERT INTO posts (name, message)
        VALUES (?, ?)
    """, (
        random.choice(names),
        post
    ))

conn.commit()
conn.close()

print("✅ Dummy data inserted successfully (announcements, jobs, forum posts).")
