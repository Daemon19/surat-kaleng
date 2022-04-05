from app import app
from app.models import Pengguna
from .forms import KirimSuratForm, LoginForm
from flask import redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse


@app.route("/index")
@app.route("/")
def index():
    return redirect(url_for("kirim_surat"))


@app.route("/kirim_surat")
@login_required
def kirim_surat():
    form = KirimSuratForm()

    if not form.validate_on_submit():
        return render_template("kirim_surat.html", form=form)

    return "TODO"


@app.route("/kotak_surat")
def kotak_surat():
    return "TODO"


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    if not form.validate_on_submit():
        return render_template("login.html", form=form)

    pengguna = Pengguna.query.filter_by(nama=form.nama.data).first()
    if pengguna is None or not pengguna.check_password(form.password.data):
        flash("Nama pengguna atau password salah")
        return redirect(url_for("login"))

    login_user(pengguna, True)
    next_page = request.args.get("next")
    if not next_page or url_parse(next_page).netloc != "":
        next_page = url_for("index")

    return redirect(next_page)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
