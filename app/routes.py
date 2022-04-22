from flask import redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash
from functools import wraps
from . import app, db
from .schema import Pengguna, Surat
from .forms import FormMasuk


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

    surat = (
        Surat.query.filter_by(id_penerima=session["id_pengguna"])
        .order_by(Surat.tanggal.desc())
        .all()
    )
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
    if session.get("id_pengguna") is not None:
        return redirect(url_for("index"))

    form = FormMasuk()

    if not form.validate_on_submit():
        return render_template("masuk.html", form=form)

    pengguna = Pengguna.query.filter_by(nama=form.nama.data).first()
    session["id_pengguna"] = pengguna.id
    return redirect("/")


@app.route("/keluar", methods=["POST"])
def keluar():
    session.clear()
    return redirect("/")
