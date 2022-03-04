CREATE TABLE pengguna (
    id INTEGER PRIMARY KEY NOT NULL,
    nama TEXT UNIQUE NOT NULL,
    hash TEXT NOT NULL
);

CREATE TABLE surat (
    id INTEGER PRIMARY KEY NOT NULL,
    id_penerima INTEGER NOT NULL,
    pesan TEXT NOT NULL,
    tanggal TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_penerima) REFERENCES pengguna(id)
);