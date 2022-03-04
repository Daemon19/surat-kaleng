from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

app = Flask(__name__)

# Memastikan templates otomatis dimuat ulang
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Mengatur sesi agar menggunakan filesystem (dibandingkan signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///surat_kaleng.db")


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

    rows = db.execute("SELECT * FROM pengguna WHERE nama = ?", nama)
    if not rows:
        return minta_maaf("penerima tidak ditemukan")
    penerima = rows[0]["id"]

    pesan = request.form.get("pesan")
    if not pesan:
        return minta_maaf("pesan harus dicantumkan")

    db.execute("INSERT INTO surat (penerima, pesan) VALUES (?, ?)", penerima, pesan)

    return redirect("/")


@app.route("/kotak-surat")
@perlu_masuk
def kotak_surat():
    """Menampilkan semua surat yang diterima pengguna"""

    surat = db.execute(
        "SELECT * FROM surat WHERE penerima = ? ORDER BY tanggal DESC",
        session["id_pengguna"],
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
    if db.execute("SELECT * FROM pengguna WHERE nama = ?", nama):
        return minta_maaf("nama sudah dimiliki")

    kata_sandi = request.form.get("kata-sandi")
    konfirmasi = request.form.get("konfirmasi")
    if not (kata_sandi and konfirmasi):
        return minta_maaf("kata sandi harus dicantumkan")
    if kata_sandi != konfirmasi:
        return minta_maaf("kata sandi dan konfirmasi tidak sama")

    session["id_pengguna"] = db.execute(
        "INSERT INTO pengguna (nama, hash) VALUES (?, ?)",
        nama,
        generate_password_hash(kata_sandi),
    )

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

    rows = db.execute("SELECT * FROM pengguna WHERE nama = ?", nama)
    if not rows:
        return minta_maaf("nama tidak terdaftar")
    if not check_password_hash(rows[0]["hash"], kata_sandi):
        return minta_maaf("kata sandi salah")

    session["id_pengguna"] = rows[0]["id"]

    return redirect("/")


@app.route("/keluar")
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
