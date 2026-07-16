import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    send_from_directory,
)

from src.dashboard.executive_dashboard import get_executive_summary
from src.dashboard.incident_risk_service import calculate_incident_risk
from src.database.fetch_related_logs import fetch_related_logs
from src.database.update_incident import update_incident
from src.database.fetch_incident_details import fetch_incident_details
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

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False,   # Change to True after HTTPS deployment
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30),
)


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
            session.permanent = True

            return redirect(url_for("dashboard"))

        error = "Invalid username or password"

    return render_template("login.html", error=error)


@app.route("/")
def dashboard():
    if not is_logged_in():
        return redirect(url_for("login"))

    data = get_dashboard_data()
    executive_summary = get_executive_summary()

    return render_template(
        "dashboard.html",
        **data,
        executive_summary=executive_summary,
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
    if not is_logged_in():
        return redirect(url_for("login"))

    return send_from_directory(
        "reports_output",
        filename,
        as_attachment=True,
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


@app.route(
    "/incident/<int:incident_id>",
    methods=["GET", "POST"],
)
def incident_details_page(incident_id):
    if not is_logged_in():
        return redirect(url_for("login"))

    error = None
    success = None

    if request.method == "POST":
        notes = request.form.get("notes", "").strip()
        status = request.form.get("status", "Open").strip()
        assigned_to = request.form.get(
            "assigned_to",
            "SOC Analyst",
        ).strip()

        try:
            updated = update_incident(
                incident_id=incident_id,
                notes=notes,
                status=status,
                assigned_to=assigned_to,
            )

            if updated:
                success = "Incident updated successfully."
            else:
                error = "Incident could not be updated."

        except ValueError as exc:
            error = str(exc)

        except Exception as exc:
            print(f"Incident update failed: {exc}")
            error = "An unexpected error occurred."

    incident = fetch_incident_details(incident_id)

    if not incident:
        return "Incident not found", 404
    
    related_logs = fetch_related_logs(
    incident["source_ip"],
    limit=20,
)
    
    risk_assessment = calculate_incident_risk(
    incident,
    related_logs,
)

    return render_template(
        "incident_details.html",
        incident=incident,
        related_logs=related_logs,
        risk_assessment=risk_assessment,
        username=session["username"],
        role=session["role"],
        error=error,
        success=success,
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)