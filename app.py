from flask import Flask, render_template, request, redirect, url_for, session

from src.auth.auth_service import authenticate_user
from src.dashboard.services import get_dashboard_data
from src.database.fetch_alerts import fetch_alerts
from src.database.incidents import fetch_incidents
from src.dashboard.ai_service import get_ai_anomalies

app = Flask(__name__)
app.secret_key = "change_this_secret_key"


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


@app.route("/reports")
def reports_page():
    if not is_logged_in():
        return redirect(url_for("login"))

    return render_template(
        "reports.html",
        username=session["username"],
        role=session["role"]
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)