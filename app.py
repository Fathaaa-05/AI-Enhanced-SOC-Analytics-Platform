from flask import Flask, render_template, request, redirect, url_for, session
from src.dashboard.services import get_dashboard_data
from src.auth.auth_service import authenticate_user

app = Flask(__name__)
app.secret_key = "change_this_secret_key"


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
    if "username" not in session:
        return redirect(url_for("login"))

    data = get_dashboard_data()

    return render_template(
        "dashboard.html",
        **data,
        username=session["username"],
        role=session["role"]
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)