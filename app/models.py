from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Pengguna(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(64), index=True, unique=True, nullable=False)
    hash_password = db.Column(db.String(128), nullable=False)
    surat = db.relationship("Surat", backref="penerima", lazy="dynamic")

    def __repr__(self):
        return f"<Pengguna {self.nama}>"

    def set_password(self, password):
        self.hash_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hash_password, password)


class Surat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pesan = db.Column(db.String(140), nullable=False)
    tanggal = db.Column(
        db.DateTime, index=True, nullable=False, default=datetime.utcnow
    )
    id_pengguna = db.Column(db.Integer, db.ForeignKey("pengguna.id"))

    def __repr__(self):
        return "<Surat {}>".format(self.pesan)


@login.user_loader
def load_user(id):
    return Pengguna.query.get(int(id))
