from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class KirimSuratForm(FlaskForm):
    nama_penerima = StringField("Nama penerima", [DataRequired()])
    pesan = TextAreaField("Pesan", [DataRequired()])
    submit = SubmitField("Kirim")


class LoginForm(FlaskForm):
    nama = StringField("Nama pengguna", [DataRequired()])
    password = PasswordField("Kata sandi", [DataRequired()])
    submit = SubmitField("Masuk")
