from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'ADMIN@01'  # Replace with something secure

def get_db_connection():
    conn = sqlite3.connect('villageconnect.db')
    conn.row_factory = sqlite3.Row
    return conn

# -------------------------
# 🏠 Home Page 
# -------------------------
@app.route("/")
def home():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    return render_template("home.html")

# -------------------------
# 📢 Jobs and Announcements
# -------------------------
@app.route("/view-jobs")
def view_jobs():
    conn = get_db_connection()
    jobs = conn.execute("SELECT * FROM jobs ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("jobs.html", jobs=jobs)

@app.route("/view-announcements")
def view_announcements():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM announcements ORDER BY date_posted DESC").fetchall()
    conn.close()
    return render_template("announcements.html", announcements=rows)

# -------------------------
# 💼 Add Job and Add Announcements 
# -------------------------
@app.route("/add-job", methods=["GET", "POST"])
def add_job():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    
    if session.get("role") != "admin":
        return redirect(url_for("home"))
    
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        salary = request.form.get("salary", "").strip()
        location = request.form.get("location", "").strip()

        if not title or not description:
            return "Title and Description are required", 400

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO jobs (title, description, salary, location)
            VALUES (?, ?, ?, ?)""",
            (title, description, salary, location)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('home'))

    return render_template("add_job.html")

@app.route("/add-announcement", methods=["GET", "POST"])
def add_announcement():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    
    if session.get("role") != "admin":
        return redirect(url_for("home"))
    
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        message = request.form.get("message", "").strip()
        date_posted = request.form.get("date_posted", "").strip()

        if not title or not message or not date_posted:
            return "All fields are required!", 400

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO announcements (title, message, date_posted)
            VALUES (?, ?, ?)""",
            (title, message, date_posted)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('view_announcements'))

    return render_template("add_announcement.html")

@app.route("/services")
def view_services():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    query = request.args.get("q", "").strip()
    conn = get_db_connection()

    if query:
        announcements = conn.execute(
            "SELECT * FROM announcements WHERE title LIKE ? OR message LIKE ?",
            (f"%{query}%", f"%{query}%")
        ).fetchall()
        jobs = conn.execute(
            "SELECT * FROM jobs WHERE title LIKE ? OR description LIKE ?",
            (f"%{query}%", f"%{query}%")
        ).fetchall()
    else:
        announcements = conn.execute("SELECT * FROM announcements").fetchall()
        jobs = conn.execute("SELECT * FROM jobs").fetchall()

    conn.close()
    return render_template("services.html", announcements=announcements, jobs=jobs, query=query)

@app.route("/forum", methods=["GET", "POST"])
def forum():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    conn = get_db_connection()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not message:
            conn.close()
            return "Name and message are required.", 400

        conn.execute("INSERT INTO posts (name, message) VALUES (?, ?)", (name, message))
        conn.commit()

    posts = conn.execute("SELECT * FROM posts ORDER BY timestamp DESC").fetchall()
    conn.close()
    return render_template("forum.html", posts=posts)

# -------------------------
# 👥 View Users 
# -------------------------
@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return jsonify([dict(u) for u in users])

# -------------------------
# 🧾 API Routes
# -------------------------

@app.route("/announcements", methods=["GET", "POST"])
def api_announcements():
    conn = get_db_connection()
    if request.method == "GET":
        rows = conn.execute("SELECT * FROM announcements ORDER BY date_posted DESC").fetchall()
        conn.close()
        return jsonify([dict(r) for r in rows])
    else:
        data = request.get_json()
        conn.execute("INSERT INTO announcements (title, message, date_posted) VALUES (?, ?, ?)",
                     (data["title"], data["message"], data["date_posted"]))
        conn.commit()
        conn.close()
        return jsonify({"message": "Announcement added"}), 201

@app.route("/announcements/<int:id>", methods=["DELETE"])
def delete_announcement(id):
    conn = get_db_connection()
    announcement = conn.execute("SELECT * FROM announcements WHERE id = ?", (id,)).fetchone()

    if not announcement:
        conn.close()
        return jsonify({"error": "Announcement not found"}), 404

    conn.execute("DELETE FROM announcements WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Announcement ID {id} deleted"}), 200

@app.route("/jobs", methods=["GET", "POST"])
def api_jobs():
    conn = get_db_connection()
    if request.method == "GET":
        jobs = conn.execute("SELECT * FROM jobs").fetchall()
        conn.close()
        return jsonify([dict(job) for job in jobs])
    else:
        data = request.get_json()
        conn.execute("INSERT INTO jobs (title, description, salary, location) VALUES (?, ?, ?, ?)",
                     (data["title"], data["description"], data["salary"], data["location"]))
        conn.commit()
        conn.close()
        return jsonify({"message": "Job added"}), 201

@app.route("/jobs/<int:id>", methods=["DELETE"])
def delete_job(id):
    conn = get_db_connection()
    job = conn.execute("SELECT * FROM jobs WHERE id = ?", (id,)).fetchone()

    if not job:
        conn.close()
        return jsonify({"error": "Job not found"}), 404

    conn.execute("DELETE FROM jobs WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Job ID {id} deleted"}), 200

@app.route("/view-users")
def view_users():
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return render_template("users.html", users=users)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        role = request.form.get("role", "user")

        hashed_pw = generate_password_hash(password)

        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                (name, email, hashed_pw, role)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "Email already registered.", 400

        conn.close()
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            session["name"] = user["name"]
            return redirect(url_for("home"))
        else:
            return "Invalid credentials", 401

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# -------------------------
# Run the app
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
