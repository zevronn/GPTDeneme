from __future__ import annotations

import argparse
import csv
import io
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.middleware.proxy_fix import ProxyFix

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "isg.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key"
# Reverse proxy arkasında yanlış host/proto algısını düzeltir.
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)  # type: ignore[assignment]
# Local erişim senaryolarında host doğrulama hatalarını önlemek için.
app.config["TRUSTED_HOSTS"] = ["localhost", "127.0.0.1", "[::1]"]


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_conn()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            city TEXT NOT NULL,
            district TEXT,
            risk_level TEXT NOT NULL DEFAULT 'Orta'
        );

        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            location_code TEXT NOT NULL,
            department TEXT NOT NULL,
            position TEXT NOT NULL,
            employment_start_date TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_no TEXT UNIQUE NOT NULL,
            location_code TEXT NOT NULL,
            incident_datetime TEXT NOT NULL,
            incident_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Açık'
        );
        """
    )

    existing = conn.execute("SELECT COUNT(*) as cnt FROM locations").fetchone()["cnt"]
    if existing == 0:
        conn.executemany(
            "INSERT INTO locations(code, name, city, district, risk_level) VALUES(?,?,?,?,?)",
            [
                ("LOC-IST-01", "Merkez Mutfak İstanbul", "İstanbul", "Kadıköy", "Orta"),
                ("LOC-ANK-01", "Merkez Mutfak Ankara", "Ankara", "Çankaya", "Düşük"),
                ("LOC-IZM-01", "Merkez Mutfak İzmir", "İzmir", "Bornova", "Yüksek"),
            ],
        )
    conn.commit()
    conn.close()


def generate_incident_no() -> str:
    now = datetime.now()
    return f"KZ-{now:%Y%m%d-%H%M%S}"


@app.route("/")
def dashboard():
    conn = get_conn()
    locations = conn.execute("SELECT * FROM locations ORDER BY name").fetchall()

    start_date = (datetime.now() - timedelta(days=30)).isoformat()
    cards = []
    for loc in locations:
        incident_count = conn.execute(
            """
            SELECT COUNT(*) as cnt
            FROM incidents
            WHERE location_code = ? AND incident_datetime >= ?
            """,
            (loc["code"], start_date),
        ).fetchone()["cnt"]

        active_emp = conn.execute(
            "SELECT COUNT(*) as cnt FROM employees WHERE location_code = ? AND is_active = 1",
            (loc["code"],),
        ).fetchone()["cnt"]

        cards.append(
            {
                "code": loc["code"],
                "name": loc["name"],
                "city": loc["city"],
                "district": loc["district"],
                "risk_level": loc["risk_level"],
                "incident_count": incident_count,
                "active_emp": active_emp,
            }
        )

    summary = {
        "location_total": len(locations),
        "incident_total": conn.execute("SELECT COUNT(*) as cnt FROM incidents").fetchone()["cnt"],
        "employee_total": conn.execute("SELECT COUNT(*) as cnt FROM employees").fetchone()["cnt"],
    }
    conn.close()
    return render_template("dashboard.html", cards=cards, summary=summary)


@app.route("/incidents/new", methods=["GET", "POST"])
def new_incident():
    conn = get_conn()
    locations = conn.execute("SELECT code, name FROM locations ORDER BY name").fetchall()

    if request.method == "POST":
        location_code = request.form.get("location_code", "").strip()
        incident_type = request.form.get("incident_type", "").strip()
        severity = request.form.get("severity", "").strip()
        description = request.form.get("description", "").strip()

        if not all([location_code, incident_type, severity, description]):
            flash("Lütfen tüm zorunlu alanları doldurun.", "error")
            conn.close()
            return render_template("new_incident.html", locations=locations)

        incident_no = generate_incident_no()
        conn.execute(
            """
            INSERT INTO incidents(incident_no, location_code, incident_datetime, incident_type, severity, description)
            VALUES(?,?,?,?,?,?)
            """,
            (incident_no, location_code, datetime.now().isoformat(), incident_type, severity, description),
        )
        conn.commit()
        conn.close()
        flash(f"Kaza kaydı oluşturuldu: {incident_no}", "success")
        return redirect(url_for("dashboard"))

    conn.close()
    return render_template("new_incident.html", locations=locations)


@app.route("/employees/import", methods=["GET", "POST"])
def import_employees():
    result = None

    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            flash("Lütfen CSV dosyası seçin.", "error")
            return render_template("import_employees.html", result=result)

        content = file.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(content))

        required_cols = {
            "employee_id",
            "full_name",
            "location_code",
            "department",
            "position",
            "employment_start_date",
            "is_active",
        }

        missing = required_cols - set(reader.fieldnames or [])
        if missing:
            flash(f"Eksik kolon(lar): {', '.join(sorted(missing))}", "error")
            return render_template("import_employees.html", result=result)

        conn = get_conn()
        total, success, failed = 0, 0, 0
        errors: list[str] = []

        for row_num, row in enumerate(reader, start=2):
            total += 1
            if any(not row.get(col) for col in required_cols):
                failed += 1
                errors.append(f"Satır {row_num}: Zorunlu alan boş")
                continue

            try:
                is_active = 1 if str(row["is_active"]).lower() == "true" else 0
                conn.execute(
                    """
                    INSERT INTO employees(employee_id, full_name, location_code, department, position, employment_start_date, is_active)
                    VALUES(?,?,?,?,?,?,?)
                    ON CONFLICT(employee_id) DO UPDATE SET
                        full_name=excluded.full_name,
                        location_code=excluded.location_code,
                        department=excluded.department,
                        position=excluded.position,
                        employment_start_date=excluded.employment_start_date,
                        is_active=excluded.is_active
                    """,
                    (
                        row["employee_id"],
                        row["full_name"],
                        row["location_code"],
                        row["department"],
                        row["position"],
                        row["employment_start_date"],
                        is_active,
                    ),
                )
                success += 1
            except Exception as exc:  # noqa: BLE001
                failed += 1
                errors.append(f"Satır {row_num}: {exc}")

        conn.commit()
        conn.close()

        result = {"total": total, "success": success, "failed": failed, "errors": errors}

    return render_template("import_employees.html", result=result)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="İSG demo uygulamasını başlatır.")
    parser.add_argument("--host", default="0.0.0.0", help="Dinlenecek host (varsayılan: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=5000, help="Dinlenecek port (varsayılan: 5000)")
    parser.add_argument("--debug", action="store_true", help="Flask debug modunu aç")
    return parser.parse_args()


if __name__ == "__main__":
    init_db()
    args = parse_args()
    app.run(debug=args.debug, host=args.host, port=args.port)
