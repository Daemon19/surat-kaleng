from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class KirimSuratForm(FlaskForm):
    nama_penerima = StringField("Nama penerima", [DataRequired()])
    pesan = TextAreaField("Pesan", [DataRequired()])
    submit = SubmitField("Kirim")
