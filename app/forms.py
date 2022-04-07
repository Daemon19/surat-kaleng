from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    PasswordField,
    ValidationError,
)
from wtforms.validators import DataRequired, EqualTo
from app.models import Pengguna


class DataDiperlukan(DataRequired):
    def __init__(self, message="Data ini diperlukan."):
        super().__init__(message)


class SamaDengan(EqualTo):
    def __init__(self, fieldname, message=None):
        super().__init__(
            fieldname, message or f"Kolom ini harus sama dengan {fieldname}"
        )


class KirimSuratForm(FlaskForm):
    nama_penerima = StringField("Nama penerima", [DataDiperlukan()])
    pesan = TextAreaField("Pesan", [DataDiperlukan()])
    submit = SubmitField("Kirim")


class LoginForm(FlaskForm):
    nama = StringField("Nama pengguna", [DataDiperlukan()])
    password = PasswordField("Kata sandi", [DataDiperlukan()])
    submit = SubmitField("Masuk")


class RegistrationForm(FlaskForm):
    nama = StringField("Nama pengguna", [DataDiperlukan()])
    password = PasswordField("Kata sandi", [DataDiperlukan()])
    password2 = PasswordField(
        "Ulangi kata sandi", [DataDiperlukan(), SamaDengan("password")]
    )
    submit = SubmitField("Daftar")

    def validate_nama(self, nama):
        pengguna = Pengguna.query.filter_by(nama=nama.data).first()
        if pengguna is not None:
            raise ValidationError("Nama pengguna sudah dimiliki.")
