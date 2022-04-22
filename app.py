from app import app, db


@app.cli.command("buat_tabel")
def buat_tabel():
    db.create_all()


if __name__ == "__main__":
    app.run()
