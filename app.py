from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from dotenv import load_dotenv
import os
from datetime import datetime
from babel.dates import format_datetime
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

load_dotenv()

app = Flask(__name__)

# Memastikan templates otomatis dimuat ulang
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Mengatur sesi agar menggunakan filesystem (dibandingkan signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

DATABASE_URI = os.getenv("DATABASE_URL").replace("://", "ql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

moment = Moment(app)


class Pengguna(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String, unique=True, nullable=False)
    hash = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        id = self.id
        nama = self.nama
        hash = self.hash
        return f"<{self.__class__.__name__}({id=}, {nama=}, {hash=})>"


class Surat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pesan = db.Column(db.String, nullable=False)
    tanggal = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    id_penerima = db.Column(db.Integer, db.ForeignKey(
        "pengguna.id"), nullable=False)
    penerima = db.relationship(
        "Pengguna", backref=db.backref("pesan", lazy=True))

    def __repr__(self) -> str:
        id = self.id
        pesan = self.pesan
        tanggal = self.tanggal
        return f"<{self.__class__.__name__}({id=}, {pesan=}, {tanggal=})>"


def perlu_masuk(f):
    """
    Mendekorasi rute agar memerlukan masuk ke akun.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id_pengguna") is None:
            return redirect(url_for("masuk", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def index():
    if session.get("id_pengguna"):
        return redirect("/kotak-surat")
    return redirect("/kirim")


@app.route("/kirim", methods=["GET", "POST"])
def kirim():
    """Mengirim surat kaleng ke penerima"""

    if request.method == "GET":
        return render_template("kirim_surat.html")

    nama = request.form.get("nama")
    if not nama:
        return minta_maaf("nama penerima harus dicantumkan")

    penerima = Pengguna.query.filter_by(nama=nama).first()
    if not penerima:
        return minta_maaf("penerima tidak ditemukan")

    pesan = request.form.get("pesan")
    if not pesan:
        return minta_maaf("pesan harus dicantumkan")
    surat = Surat(pesan=pesan, penerima=penerima)

    db.session.add(surat)
    db.session.commit()

    return redirect("/")


@app.route("/kotak-surat")
@perlu_masuk
def kotak_surat():
    """Menampilkan semua surat yang diterima pengguna"""

    surat = Surat.query.filter_by(id_penerima=session["id_pengguna"]).order_by(
        Surat.tanggal.desc()).all()
    return render_template("kotak_surat.html", surat=surat)


@app.route("/daftar", methods=["GET", "POST"])
def daftar():
    if request.method == "GET":
        return render_template("daftar.html")

    # Membuat akun untuk pengguna, lalu masuk ke akun tersebut
    nama = request.form.get("nama")
    if not nama:
        return minta_maaf("nama harus dicantumkan")
    if Pengguna.query.filter_by(nama=nama).first():
        return minta_maaf("nama sudah dimiliki")

    kata_sandi = request.form.get("kata-sandi")
    konfirmasi = request.form.get("konfirmasi")
    if not (kata_sandi and konfirmasi):
        return minta_maaf("kata sandi harus dicantumkan")
    if kata_sandi != konfirmasi:
        return minta_maaf("kata sandi dan konfirmasi tidak sama")

    pengguna = Pengguna(nama=nama, hash=generate_password_hash(kata_sandi))
    db.session.add(pengguna)
    db.session.commit()

    session["id_pengguna"] = pengguna.id

    return redirect("/")


@app.route("/masuk", methods=["GET", "POST"])
def masuk():
    # Melupakan id pengguna
    session.clear()

    if request.method == "GET":
        return render_template("masuk.html")

    # Memasukkan pengguna
    nama = request.form.get("nama")
    if not nama:
        return minta_maaf("nama harus dicantumkan")

    kata_sandi = request.form.get("kata-sandi")
    if not kata_sandi:
        return minta_maaf("kata sandi harus dicantumkan")

    pengguna = Pengguna.query.filter_by(nama=nama).first()
    if not pengguna:
        return minta_maaf("nama tidak terdaftar")
    if not check_password_hash(pengguna.hash, kata_sandi):
        return minta_maaf("kata sandi salah")

    session["id_pengguna"] = pengguna.id

    return redirect("/")


@app.route("/keluar", methods=["POST"])
def keluar():
    session.clear()
    return redirect("/")


def minta_maaf(pesan, kode=400):
    """Menampilkan pesan sebagai permohonan maaf kepada pengguna."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("maaf.html", atas=kode, bawah=escape(pesan)), kode


@app.cli.command("buat_tabel")
def buat_tabel():
    db.create_all()


if __name__ == "__main__":
    app.run(load_dotenv=True)
