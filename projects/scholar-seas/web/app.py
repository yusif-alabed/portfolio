import sqlite3

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from shared.database import (
    create_parent,
    create_user,
    get_parent_by_user,
    get_parent_children,
    get_seconds_played_today,
    get_settings,
    get_topic_accuracy,
    get_user_by_username,
    link_parent_to_student,
    reset_student_password,
    save_settings,
)

app = Flask(__name__)

app.secret_key = "scholar-seas-development-key"


@app.route("/", methods=["GET", "POST"])
def parent_login():
    message = ""

    if request.method == "POST":
        action = request.form.get("action")
        username = request.form.get(
            "username",
            "",
        ).strip()
        password = request.form.get("password", "")

        if len(username) < 3:
            message = (
                "Username must contain at least 3 characters."
            )

        elif len(password) < 6:
            message = (
                "Password must contain at least 6 characters."
            )

        elif action == "register":
            try:
                password_hash = generate_password_hash(
                    password,
                    method="pbkdf2:sha256",
                )

                user_id = create_user(
                    username,
                    password_hash,
                    "parent",
                )

                create_parent(user_id)

                message = (
                    "Parent account created. You can now log in."
                )

            except sqlite3.IntegrityError:
                message = (
                    "That username is already being used."
                )

        elif action == "login":
            user = get_user_by_username(username)

            if user is None:
                message = "That account does not exist."

            elif user["role"] != "parent":
                message = "Please use a parent account."

            elif not check_password_hash(
                user["password_hash"],
                password,
            ):
                message = "The password is incorrect."

            else:
                parent = get_parent_by_user(
                    user["user_id"]
                )

                session["parent_id"] = parent["parent_id"]
                session["username"] = username

                return redirect(url_for("dashboard"))

    return render_template(
        "parent_login.html",
        message=message,
    )


@app.route("/dashboard")
def dashboard():
    if "parent_id" not in session:
        return redirect(url_for("parent_login"))

    parent_id = session["parent_id"]
    children = get_parent_children(parent_id)

    playtime = {}

    for child in children:
        child_id = child["student_id"]

        seconds = get_seconds_played_today(
            child_id
        )

        minutes = round(seconds / 60, 1)
        playtime[child_id] = minutes

    selected_student = None
    accuracy = []

    student_id = request.args.get(
        "student_id",
        type=int,
    )

    if student_id is not None:
        for child in children:
            if child["student_id"] == student_id:
                selected_student = child
                accuracy = get_topic_accuracy(
                    student_id
                )
                break

    return render_template(
        "dashboard.html",
        username=session["username"],
        children=children,
        selected_student=selected_student,
        accuracy=accuracy,
        playtime=playtime,
    )


@app.route("/link-student", methods=["POST"])
def link_student():
    if "parent_id" not in session:
        return redirect(url_for("parent_login"))

    student_username = request.form.get(
        "student_username",
        "",
    ).strip()

    success, message = link_parent_to_student(
        session["parent_id"],
        student_username,
    )

    return redirect(
        url_for(
            "dashboard",
            message=message,
        )
    )


@app.route(
    "/settings/<int:student_id>",
    methods=["GET", "POST"],
)
def student_settings(student_id):
    if "parent_id" not in session:
        return redirect(url_for("parent_login"))

    children = get_parent_children(
        session["parent_id"]
    )

    selected_student = None

    for child in children:
        if child["student_id"] == student_id:
            selected_student = child
            break

    if selected_student is None:
        return redirect(url_for("dashboard"))

    message = ""

    if request.method == "POST":
        action = request.form.get("action", "save_limits")

        if action == "reset_password":
            new_password = request.form.get(
                "new_password",
                "",
            )

            if len(new_password) < 6:
                message = (
                    "The new password must contain at least 6 characters."
                )
            else:
                password_hash = generate_password_hash(
                    new_password,
                    method="pbkdf2:sha256",
                )
                reset_student_password(
                    student_id,
                    password_hash,
                )
                message = "The student's password has been reset."

        else:
            weekday_limit = request.form.get(
                "weekday_limit",
                type=int,
            )
            weekend_limit = request.form.get(
                "weekend_limit",
                type=int,
            )

            if (
                weekday_limit is None
                or weekend_limit is None
            ):
                message = "Please enter valid time limits."

            elif (
                weekday_limit < 0
                or weekend_limit < 0
            ):
                message = "Time limits cannot be negative."

            else:
                save_settings(
                    student_id,
                    weekday_limit,
                    weekend_limit,
                )

                message = "Playtime settings saved."

    settings = get_settings(student_id)

    return render_template(
        "settings.html",
        student=selected_student,
        settings=settings,
        message=message,
    )


@app.route("/logout")
def logout():
    session.clear()

    return redirect(url_for("parent_login"))


if __name__ == "__main__":
    app.run(debug=True)
