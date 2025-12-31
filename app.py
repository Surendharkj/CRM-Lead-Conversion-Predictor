from flask import Flask, render_template, request
import sqlite3
import pickle
import pandas as pd
import os

app = Flask(__name__)

DB_PATH = "database/leads.db"
MODEL_PATH = "model/lead_model.pkl"

def get_db_connection():
    return sqlite3.connect(DB_PATH)

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    probability = None

    if request.method == "POST":
        # 1. Read form inputs
        lead_source = request.form["lead_source"]
        calls = int(request.form["calls"])
        emails = int(request.form["emails"])
        time = int(request.form["time"])

        # 2. Load ML model + encoder
        with open(MODEL_PATH, "rb") as f:
            model, le = pickle.load(f)

        # 3. Prepare input for prediction
        input_df = pd.DataFrame([{
            "lead_source": lead_source,
            "calls_made": calls,
            "emails_sent": emails,
            "time_on_site": time
        }])

        input_df["lead_source"] = le.transform(input_df["lead_source"])

        # 4. Predict
        prediction = int(model.predict(input_df)[0])
        probability = round(model.predict_proba(input_df)[0][1] * 100, 2)

        # 5. Save to database (UPGRADE 2)
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO leads 
            (lead_source, calls_made, emails_sent, time_on_site, prediction, probability)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            lead_source,
            calls,
            emails,
            time,
            prediction,
            probability
        ))

        conn.commit()
        conn.close()

    return render_template(
        "index.html",
        prediction=prediction,
        probability=probability
    )
@app.route("/leads")
def view_leads():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, lead_source, calls_made, emails_sent,
               time_on_site, prediction, probability
        FROM leads
        ORDER BY id DESC
    """)

    leads = cursor.fetchall()
    conn.close()

    return render_template("leads.html", leads=leads)


if __name__ == "__main__":
    app.run(debug=True)
