from app import app, db
from app.models import Pengguna
from .forms import KirimSuratForm, LoginForm, RegistrationForm
from flask import redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse


@app.route("/index")
@app.route("/")
def index():
    return redirect(url_for("kirim_surat"))


@app.route("/kirim_surat")
def kirim_surat():
    form = KirimSuratForm()

    if not form.validate_on_submit():
        return render_template("kirim_surat.html", form=form)

    return "TODO"


@app.route("/kotak_surat")
@login_required
def kotak_surat():
    return "TODO"


def login_pengguna(nama, password):
    pengguna = Pengguna.query.filter_by(nama=nama).first()
    if pengguna is None or not pengguna.check_password(password):
        flash("Nama pengguna atau password salah")
        return redirect(url_for("login"))

    login_user(pengguna, True)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    if not form.validate_on_submit():
        return render_template("login.html", form=form)

    next_page = request.args.get("next")
    if not next_page or url_parse(next_page).netloc != "":
        next_page = url_for("index")

    if (ret := login_pengguna(form.nama.data, form.password.data)) is not None:
        return ret
    flash(f"Selamat datang {current_user.nama}.")
    return redirect(next_page)


@app.route("/daftar", methods=["GET", "POST"])
def daftar():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()

    if not form.validate_on_submit():
        return render_template("daftar.html", form=form)

    pengguna = Pengguna(nama=form.nama.data)
    pengguna.set_password(form.password.data)

    db.session.add(pengguna)
    db.session.commit()
    flash("Selamat, kamu sudah terdaftar!")

    if (ret := login_pengguna(form.nama.data, form.password.data)) is not None:
        return ret
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
