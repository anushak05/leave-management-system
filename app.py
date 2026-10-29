
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import sqlite3
import os
import re

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "v2-classroom-demo")

DATABASE = os.path.join(os.path.dirname(__file__), "leaves.db")


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS leaves (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                register_number TEXT NOT NULL,
                from_date TEXT NOT NULL,
                to_date TEXT NOT NULL,
                reason TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pending'
            )
        """)

        columns = {
            row["name"]
            for row in conn.execute("PRAGMA table_info(leaves)")
        }

        if "leave_type" not in columns:
            conn.execute("""
                ALTER TABLE leaves
                ADD COLUMN leave_type TEXT DEFAULT 'Personal'
            """)

        conn.commit()


def get_leaves():
    with get_db() as conn:
        records = conn.execute(
            "SELECT * FROM leaves ORDER BY id DESC"
        ).fetchall()

    leaves = []

    for row in records:
        leave = dict(row)

        start = datetime.strptime(
            leave["from_date"], "%Y-%m-%d"
        ).date()

        end = datetime.strptime(
            leave["to_date"], "%Y-%m-%d"
        ).date()

        leave["days"] = (end - start).days + 1
        leaves.append(leave)

    return leaves


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("student_name", "").strip()
        regno = request.form.get("register_number", "").strip().upper()
        leave_type = request.form.get("leave_type", "").strip()
        from_date = request.form.get("from_date", "")
        to_date = request.form.get("to_date", "")
        reason = request.form.get("reason", "").strip()

        if not all([
            name, regno, leave_type,
            from_date, to_date, reason
        ]):
            flash("Please fill in all required fields.", "error")

        elif not re.fullmatch(r"\d{2}MIS\d{4}", regno):
            flash("Enter a valid register number.", "error")

        elif leave_type not in [
            "Medical", "Personal", "Family",
            "Emergency", "Other"
        ]:
            flash("Select a valid leave type.", "error")

        else:
            try:
                start = datetime.strptime(
                    from_date, "%Y-%m-%d"
                ).date()

                end = datetime.strptime(
                    to_date, "%Y-%m-%d"
                ).date()

                if end < start:
                    flash(
                        "To Date cannot be before From Date.",
                        "error"
                    )
                else:
                    with get_db() as conn:
                        conn.execute("""
                            INSERT INTO leaves
                            (student_name, register_number,
                             leave_type, from_date, to_date,
                             reason, status)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (
                            name, regno, leave_type,
                            from_date, to_date,
                            reason, "Pending"
                        ))
                        conn.commit()

                    flash(
                        "Leave request submitted successfully!",
                        "success"
                    )

            except ValueError:
                flash("Please enter valid dates.", "error")

        return redirect(url_for("home"))

    leaves = get_leaves()

    return render_template(
        "index.html",
        leaves=leaves,
        total_requests=len(leaves),
        pending_requests=sum(
            1 for leave in leaves
            if leave["status"] == "Pending"
        ),
        approved_requests=sum(
            1 for leave in leaves
            if leave["status"] == "Approved"
        ),
        version="V2"
    )


@app.route("/admin")
def admin():
    leaves = get_leaves()

    return render_template(
        "admin.html",
        leaves=leaves,
        total_requests=len(leaves),
        pending_requests=sum(
            1 for leave in leaves
            if leave["status"] == "Pending"
        ),
        approved_requests=sum(
            1 for leave in leaves
            if leave["status"] == "Approved"
        )
    )

@app.route("/approve/<int:leave_id>", methods=["POST"])
def approve_leave(leave_id):
    with get_db() as conn:
        cursor = conn.execute("""
            UPDATE leaves
            SET status = 'Approved'
            WHERE id = ? AND status = 'Pending'
        """, (leave_id,))
        conn.commit()

    if cursor.rowcount == 1:
        flash("Leave request approved successfully!", "success")
    else:
        flash("Request not found or already processed.", "error")

    return redirect(url_for("admin"))

@app.route("/reject/<int:leave_id>", methods=["POST"])
def reject_leave(leave_id):
    conn = sqlite3.connect("leaves.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE leaves
        SET status = 'Rejected'
        WHERE id = ? AND status = 'Pending'
        """,
        (leave_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("admin"))


@app.route("/health")
def health():
    return {"status": "ok", "version": "v3"}, 200


initialize_database()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
