import os

from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    send_from_directory
)

from src.services.pipeline_service import execute_pipeline
from src.reports.pdf_report import generate_incident_report
from src.auth.auth_service import authenticate_user
from src.dashboard.services import get_dashboard_data
from src.database.fetch_alerts import fetch_alerts
from src.database.incidents import fetch_incidents
from src.dashboard.ai_service import get_ai_anomalies

app = Flask(__name__)
import os
from dotenv import load_dotenv

load_dotenv()

app.secret_key = os.getenv("FLASK_SECRET_KEY")


def is_logged_in():
    return "username" in session


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        result = authenticate_user(username, password)

        if result["success"]:
            session["username"] = result["username"]
            session["role"] = result["role"]
            return redirect(url_for("dashboard"))

        error = "Invalid username or password"

    return render_template("login.html", error=error)


@app.route("/")
def dashboard():
    if not is_logged_in():
        return redirect(url_for("login"))

    data = get_dashboard_data()

    return render_template(
        "dashboard.html",
        **data,
        username=session["username"],
        role=session["role"]
    )


@app.route("/alerts")
def alerts_page():
    if not is_logged_in():
        return redirect(url_for("login"))

    alerts = fetch_alerts()

    return render_template(
        "alerts.html",
        alerts=alerts,
        username=session["username"],
        role=session["role"]
    )


@app.route("/incidents")
def incidents_page():
    if not is_logged_in():
        return redirect(url_for("login"))

    incidents = fetch_incidents()

    return render_template(
        "incidents.html",
        incidents=incidents,
        username=session["username"],
        role=session["role"]
    )


@app.route("/ai")
def ai_page():
    if not is_logged_in():
        return redirect(url_for("login"))

    ai_anomalies = get_ai_anomalies()

    return render_template(
        "ai.html",
        ai_anomalies=ai_anomalies,
        username=session["username"],
        role=session["role"]
    )


@app.route("/analytics")
def analytics_page():
    if not is_logged_in():
        return redirect(url_for("login"))

    data = get_dashboard_data()

    return render_template(
        "analytics.html",
        **data,
        username=session["username"],
        role=session["role"]
    )

@app.route("/reports/download/<filename>")
def download_report(filename):

    return send_from_directory(

        "reports_output",

        filename,

        as_attachment=True

    )

@app.route("/reports")
def reports_page():

    if not is_logged_in():
        return redirect(url_for("login"))

    report_folder = "reports_output"

    reports = []

    if os.path.exists(report_folder):

        for file in sorted(os.listdir(report_folder), reverse=True):

            if file.endswith(".pdf"):

                reports.append({

                    "filename": file,

                    "date": file.replace(".pdf","")

                })

    return render_template(

        "reports.html",

        reports=reports,

        username=session["username"],

        role=session["role"]

    )

@app.route("/collect-live-logs")
def collect_live_logs():
    if not is_logged_in():
        return redirect(url_for("login"))

    try:
        execute_pipeline()
    except RuntimeError as error:
        print(f"Live collector unavailable: {error}")

    return redirect(url_for("dashboard"))

@app.route("/generate-report")
def generate_report():
    if not is_logged_in():
        return redirect(url_for("login"))

    generate_incident_report()

    return redirect(url_for("reports_page"))

@app.route("/api/dashboard-summary")
def dashboard_summary():
    if not is_logged_in():
        return {"error": "Unauthorized"}, 401

    data = get_dashboard_data()

    return {
        "total_logs": data["total_logs"],
        "total_alerts": data["total_alerts"],
        "total_incidents": data["total_incidents"],
        "ai_anomalies": len(data["ai_anomalies"]),
        "critical_users": data["critical_users"]
    }


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)