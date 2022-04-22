from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError
from wtforms.validators import DataRequired, EqualTo
from werkzeug.security import check_password_hash
from .schema import Pengguna


class FormMasuk(FlaskForm):
    nama = StringField("Nama pengguna", [DataRequired()])
    kata_sandi = PasswordField("Kata sandi", [DataRequired()])

    def validate_nama(self, nama):
        pengguna = Pengguna.query.filter_by(nama=nama.data).first()
        if pengguna is None:
            raise ValidationError("Nama pengguna tidak ditemukan.")

    def validate_kata_sandi(self, kata_sandi):
        pengguna = Pengguna.query.filter_by(nama=self.nama.data).first()

        # Akan ditangani pada metode validate_nama
        if pengguna is None:
            return

        if not check_password_hash(pengguna.hash, kata_sandi.data):
            raise ValidationError("Kata sandi salah.")


class FormDaftar(FlaskForm):
    nama = StringField("Nama pengguna", [DataRequired()])
    kata_sandi = PasswordField("Kata sandi", [DataRequired()])
    kata_sandi2 = PasswordField(
        "Kata sandi (lagi)", [DataRequired(), EqualTo("kata_sandi")]
    )

    def validate_nama(self, nama):
        pengguna = Pengguna.query.filter_by(nama=nama.data).first()
        if pengguna is not None:
            raise ValidationError("Nama pengguna telah dipakai.")
