from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
from datetime import date, datetime

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
DB_PATH = Path(__file__).with_name("carnet_sante.db")

def db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with db() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS vaccinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vaccine TEXT NOT NULL,
            dose TEXT,
            date_received TEXT NOT NULL,
            next_date TEXT,
            notes TEXT
        );
        CREATE TABLE IF NOT EXISTS breast_followups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_type TEXT NOT NULL,
            exam_date TEXT NOT NULL,
            result TEXT,
            next_step TEXT,
            next_date TEXT,
            doctor TEXT,
            notes TEXT
        );
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            doctor TEXT,
            notes TEXT
        );
        """)

@app.route("/")
def index():
    with db() as con:
        vaccines = con.execute("SELECT * FROM vaccinations ORDER BY date_received DESC").fetchall()
        breast = con.execute("SELECT * FROM breast_followups ORDER BY exam_date DESC").fetchall()
        appointments = con.execute("SELECT * FROM appointments ORDER BY appointment_date ASC").fetchall()
    today = date.today().isoformat()
    upcoming_vaccines = [v for v in vaccines if v["next_date"] and v["next_date"] >= today]
    upcoming_breast = [b for b in breast if b["next_date"] and b["next_date"] >= today]
    return render_template("index.html", vaccines=vaccines, breast=breast,
                           appointments=appointments, upcoming_vaccines=upcoming_vaccines,
                           upcoming_breast=upcoming_breast, today=today)

@app.post("/vaccination/add")
def add_vaccination():
    vaccine = request.form.get("vaccine", "").strip()
    received = request.form.get("date_received", "").strip()
    if not vaccine or not received:
        flash("Veuillez renseigner le nom du vaccin et la date.", "error")
        return redirect(url_for("index") + "#vaccination")
    with db() as con:
        con.execute("""INSERT INTO vaccinations(vaccine,dose,date_received,next_date,notes)
                       VALUES(?,?,?,?,?)""",
                    (vaccine, request.form.get("dose"), received,
                     request.form.get("next_date") or None, request.form.get("notes")))
    flash("Vaccination ajoutée avec succès.", "success")
    return redirect(url_for("index") + "#vaccination")

@app.post("/vaccination/delete/<int:item_id>")
def delete_vaccination(item_id):
    with db() as con:
        con.execute("DELETE FROM vaccinations WHERE id=?", (item_id,))
    flash("Entrée de vaccination supprimée.", "success")
    return redirect(url_for("index") + "#vaccination")

@app.post("/breast/add")
def add_breast_followup():
    exam_type = request.form.get("exam_type", "").strip()
    exam_date = request.form.get("exam_date", "").strip()
    if not exam_type or not exam_date:
        flash("Veuillez renseigner le type d'examen et sa date.", "error")
        return redirect(url_for("index") + "#sein")
    with db() as con:
        con.execute("""INSERT INTO breast_followups
            (exam_type,exam_date,result,next_step,next_date,doctor,notes)
            VALUES(?,?,?,?,?,?,?)""",
            (exam_type, exam_date, request.form.get("result"),
             request.form.get("next_step"), request.form.get("next_date") or None,
             request.form.get("doctor"), request.form.get("notes")))
    flash("Suivi ajouté. Pensez à conserver vos comptes rendus médicaux.", "success")
    return redirect(url_for("index") + "#sein")

@app.post("/breast/delete/<int:item_id>")
def delete_breast_followup(item_id):
    with db() as con:
        con.execute("DELETE FROM breast_followups WHERE id=?", (item_id,))
    flash("Entrée de suivi supprimée.", "success")
    return redirect(url_for("index") + "#sein")

@app.post("/appointment/add")
def add_appointment():
    title = request.form.get("title", "").strip()
    appt_date = request.form.get("appointment_date", "").strip()
    if not title or not appt_date:
        flash("Veuillez renseigner le motif et la date du rendez-vous.", "error")
        return redirect(url_for("index") + "#rendezvous")
    with db() as con:
        con.execute("INSERT INTO appointments(title,appointment_date,doctor,notes) VALUES(?,?,?,?)",
                    (title, appt_date, request.form.get("doctor"), request.form.get("notes")))
    flash("Rendez-vous ajouté.", "success")
    return redirect(url_for("index") + "#rendezvous")

@app.post("/appointment/delete/<int:item_id>")
def delete_appointment(item_id):
    with db() as con:
        con.execute("DELETE FROM appointments WHERE id=?", (item_id,))
    flash("Rendez-vous supprimé.", "success")
    return redirect(url_for("index") + "#rendezvous")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
