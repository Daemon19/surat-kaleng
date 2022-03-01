from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)


@app.route("/")
def index():
    if not session.get("user_id"):
        return redirect("/kirim")

    return redirect("/inbox")


@app.route("/kirim", methods=["GET", "POST"])
def kirim():
    if request.method == "GET":
        return render_template("kirim.html")

    # TODO: Menangani request via POST


@app.route("/inbox")
def inbox():
    return "TODO"


@app.route("/masuk", methods=["GET", "POST"])
def masuk():
    if request.method == "GET":
        return render_template("masuk.html")

    return "TODO"
