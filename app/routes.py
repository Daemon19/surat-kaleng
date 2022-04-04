from app import app
from .forms import KirimSuratForm
from flask import redirect, render_template, url_for


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
