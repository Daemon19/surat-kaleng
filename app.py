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

    # TODO: Kirim surat ke pengguna tujuan
    return "TODO"


@app.route("/inbox")
def inbox():
    # TODO: Tampilkan surat yang diterima pengguna
    return "TODO"


@app.route("/daftar", methods=["GET", "POST"])
def daftar():
    if request.method == "GET":
        return render_template("daftar.html")

    # TODO: Buatkan akun untuk pengguna, lalu masuk ke akun tersebut
    return "TODO"


@app.route("/masuk", methods=["GET", "POST"])
def masuk():
    if request.method == "GET":
        return render_template("masuk.html")

    # TODO: Masukkan pengguna
    return "TODO"
