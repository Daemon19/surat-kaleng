from app import db
from datetime import datetime


class Pengguna(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(64), index=True, unique=True, nullable=False)
    hash_password = db.Column(db.String(128), nullable=False)
    surat = db.relationship("Surat", backref="penerima", lazy="dynamic")

    def __repr__(self):
        return f"<Pengguna {self.nama_pengguna}>"


class Surat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pesan = db.Column(db.String(140), nullable=False)
    tanggal = db.Column(
        db.DateTime, index=True, nullable=False, default=datetime.utcnow
    )
    id_pengguna = db.Column(db.Integer, db.ForeignKey("pengguna.id"))

    def __repr__(self):
        return "<Surat {}>".format(self.pesan)
