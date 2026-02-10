import os
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests as http_requests

app = Flask(__name__)

DEFAULT_SOURCE_BASE_URL = "https://loan-decision-contract.replit.app"
DB_PATH = "governance.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()


def get_source_url():
    env_url = os.environ.get("SOURCE_BASE_URL")
    if env_url:
        return env_url.rstrip("/")
    try:
        conn = get_db()
        row = conn.execute("SELECT value FROM settings WHERE key='source_base_url'").fetchone()
        conn.close()
        if row and row["value"]:
            return row["value"].rstrip("/")
    except Exception:
        pass
    return DEFAULT_SOURCE_BASE_URL.rstrip("/")


def proxy_get(path, params=None):
    base = get_source_url()
    url = f"{base}{path}"
    try:
        resp = http_requests.get(url, params=params, timeout=5)
        resp.raise_for_status()
        return resp.json(), None
    except http_requests.exceptions.Timeout:
        return None, f"Timeout fetching {url}"
    except http_requests.exceptions.ConnectionError:
        return None, f"Cannot connect to {url}"
    except http_requests.exceptions.HTTPError as e:
        return None, f"HTTP error {e.response.status_code} from {url}"
    except Exception as e:
        return None, f"Error fetching {url}: {str(e)}"


@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/measure")
def measure():
    return render_template("measure.html")


@app.route("/contract")
def contract_page():
    return render_template("contract.html")


@app.route("/raw")
def raw():
    return render_template("raw.html")


@app.route("/settings", methods=["GET", "POST"])
def settings_page():
    conn = get_db()
    if request.method == "POST":
        new_url = request.form.get("source_base_url", "").strip()
        conn.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES ('source_base_url', ?)",
            (new_url,),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("settings_page"))
    row = conn.execute("SELECT value FROM settings WHERE key='source_base_url'").fetchone()
    current_url = row["value"] if row else ""
    conn.close()
    return render_template("settings.html", current_url=current_url, default_url=DEFAULT_SOURCE_BASE_URL)


@app.route("/proxy/measure_summary")
def proxy_measure_summary():
    window = request.args.get("window", "7d")
    data, err = proxy_get("/api/measure/summary", {"window": window})
    if err:
        return jsonify({"error": err}), 502
    return jsonify(data)


@app.route("/proxy/alerts")
def proxy_alerts():
    limit = request.args.get("limit", "50")
    data, err = proxy_get("/api/alerts", {"limit": limit})
    if err:
        return jsonify({"error": err}), 502
    return jsonify(data)


@app.route("/proxy/events")
def proxy_events():
    limit = request.args.get("limit", "200")
    data, err = proxy_get("/api/events", {"limit": limit})
    if err:
        return jsonify({"error": err}), 502
    return jsonify(data)


@app.route("/proxy/decisions")
def proxy_decisions():
    limit = request.args.get("limit", "200")
    data, err = proxy_get("/api/decisions", {"limit": limit})
    if err:
        return jsonify({"error": err}), 502
    return jsonify(data)


@app.route("/proxy/contract")
def proxy_contract():
    data, err = proxy_get("/api/contract")
    if err:
        return jsonify({"error": err}), 502
    return jsonify(data)


@app.after_request
def add_cache_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=5000, debug=debug)
