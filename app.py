import sqlite3
from flask import Flask, request, session, redirect
from flask import render_template
from flask_session import Session
import access_control
import uuid

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def perform_login(username, password):
    return access_control.is_valid_user(username, password)


@app.route("/")
def index():
    if not session.get("username"):
        return redirect("/login/")
    else:
        return redirect("/dashboard/")


@app.route("/dashboard/", methods=["POST", "GET"])
def dash():
    if not session["username"]:
        return redirect("/")
    files = []

    if request.method == "POST" and session["csrf"] == request.form["csrf"]:
        files = access_control.get_query_files(request.form["search"])
    else:
        files = access_control.get_files()
    # files
    files_final = []
    for file in files:
        read_req = access_control.check_read_req(session["username"], file[0])
        write_req = access_control.check_write_req(session["username"], file[0])
        files_final.append([file, read_req, write_req])
    csrf = str(uuid.uuid1())
    session["csrf"] = csrf
    return render_template("dashboard.html", files=files_final, csrf=csrf)


@app.route("/login/", methods=["POST", "GET"])
def login():
    if session["username"]:
        return redirect("/")
    print(request.form, session["csrf"])
    if request.method == "POST" and session["csrf"] == request.form["csrf"]:
        if perform_login(request.form["username"], request.form["password"]):
            session["username"] = request.form["username"]
            return redirect("/")
        else:
            session["username"] = None
            csrf = str(uuid.uuid1())
            session["csrf"] = csrf
            return render_template(
                "login.html", message="Login failed, try again!", csrf=csrf
            )

    else:
        csrf = str(uuid.uuid1())
        session["csrf"] = csrf
        return render_template("login.html", csrf=csrf)


@app.route("/logout/")
def logout():
    session["username"] = None
    return "done"


@app.route("/editor/<file_name>", methods=["POST", "GET"])
def editor(file_name):
    if not session["username"]:
        return redirect("/")
    read_req = access_control.check_read_req(session["username"], file_name)
    write_req = access_control.check_write_req(session["username"], file_name)
    if (not read_req) and (not write_req):
        return redirect("/dashboard")

    if (
        request.method == "POST"
        and session["csrf"] == request.form["csrf"]
        and write_req
    ):
        open("files/" + file_name, "w").write(request.form["content"])
        csrf = str(uuid.uuid1())
        session["csrf"] = csrf
        return redirect(request.host_url)
    csrf = str(uuid.uuid1())
    session["csrf"] = csrf
    file_cont = str(open("files/" + file_name).read())
    return render_template(
        "file_editor.html",
        csrf=csrf,
        read=read_req,
        write=write_req,
        file_name=file_name,
        file_cont=file_cont,
    )


if __name__ == "__main__":
    app.run("localhost", 5000, debug=True)
