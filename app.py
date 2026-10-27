
from flask import Flask, request, render_template_string

app = Flask(__name__)

leaves = []

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Leave Management System - V1</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #eef3f9;
            padding: 40px;
        }
        .container {
            max-width: 650px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 15px #ddd;
        }
        h1 { color: #234c8a; }
        input, textarea, button {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            box-sizing: border-box;
        }
        button {
            background: #2563eb;
            color: white;
            border: none;
            cursor: pointer;
        }
        .leave {
            background: #f1f5f9;
            padding: 12px;
            margin-top: 10px;
            border-radius: 6px;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>Leave Management System</h1>
    <p>Version 1 - Request Leave</p>
    <p>Register Number: 24MIS0329</p>

    <h2>Apply for Leave</h2>
    <form method="POST" action="/request">
        <input name="name" placeholder="Student Name" required>
        <input name="regno" placeholder="Register Number" required>
        <input type="date" name="date" required>
        <textarea name="reason" placeholder="Reason for Leave" required></textarea>
        <button type="submit">Submit Leave Request</button>
    </form>

    <h2>Leave Requests</h2>
    {% for leave in leaves %}
        <div class="leave">
            <b>{{ leave.name }}</b> ({{ leave.regno }})
            <p>Date: {{ leave.date }}</p>
            <p>Reason: {{ leave.reason }}</p>
            <p>Status: {{ leave.status }}</p>
        </div>
    {% else %}
        <p>No leave requests yet.</p>
    {% endfor %}
</div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, leaves=leaves)

@app.route("/request", methods=["POST"])
def request_leave():
    name = request.form["name"].strip()
    regno = request.form["regno"].strip()
    date = request.form["date"]
    reason = request.form["reason"].strip()

    if not name or not regno or not date or not reason:
        return "All fields are required", 400

    leaves.append({
        "id": len(leaves) + 1,
        "name": name,
        "regno": regno,
        "date": date,
        "reason": reason,
        "status": "Pending"
    })

    return render_template_string(
        HTML, leaves=leaves
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
