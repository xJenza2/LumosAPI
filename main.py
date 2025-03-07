from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")  # Use environment variable from Render

def init_db():
    with psycopg2.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS warnings (
                            id SERIAL PRIMARY KEY,
                            user_id TEXT,
                            reason TEXT,
                            moderator TEXT,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS bans (
                            id SERIAL PRIMARY KEY,
                            user_id TEXT,
                            reason TEXT,
                            moderator TEXT,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()

@app.route('/warnings/<user_id>', methods=['GET'])
def get_warnings(user_id):
    with psycopg2.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM warnings WHERE user_id = %s", (user_id,))
        warnings = cursor.fetchall()
    return jsonify(warnings)

@app.route('/warnings', methods=['POST'])
def add_warning():
    data = request.json
    with psycopg2.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO warnings (user_id, reason, moderator) VALUES (%s, %s, %s)",
                       (data['user_id'], data['reason'], data['moderator']))
        conn.commit()
    return jsonify({"message": "Warning added successfully"})

@app.route('/warnings/<int:warning_id>', methods=['DELETE'])
def remove_warning(warning_id):
    with psycopg2.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM warnings WHERE id = %s", (warning_id,))
        conn.commit()
    return jsonify({"message": "Warning removed successfully"})

@app.route('/bans/<user_id>', methods=['GET'])
def get_bans(user_id):
    with psycopg2.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bans WHERE user_id = %s", (user_id,))
        bans = cursor.fetchall()
    return jsonify(bans)

@app.route('/bans', methods=['POST'])
def add_ban():
    data = request.json
    with psycopg2.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bans (user_id, reason, moderator) VALUES (%s, %s, %s)",
                       (data['user_id'], data['reason'], data['moderator']))
        conn.commit()
    return jsonify({"message": "Ban added successfully"})

@app.route('/bans/<int:ban_id>', methods=['DELETE'])
def remove_ban(ban_id):
    with psycopg2.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bans WHERE id = %s", (ban_id,))
        conn.commit()
    return jsonify({"message": "Ban removed successfully"})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
