from datetime import datetime
from . import db


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

    id_penerima = db.Column(db.Integer, db.ForeignKey("pengguna.id"), nullable=False)
    penerima = db.relationship("Pengguna", backref=db.backref("pesan", lazy=True))

    def __repr__(self) -> str:
        id = self.id
        pesan = self.pesan
        tanggal = self.tanggal
        return f"<{self.__class__.__name__}({id=}, {pesan=}, {tanggal=})>"
