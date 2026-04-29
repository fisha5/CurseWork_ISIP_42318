from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__, template_folder='templates')
CORS(app)

DB_NAME = 'database.db'

def get_db():
    """Возвращает соединение с базой данных"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    """Создаёт таблицы и демо-данные, если их нет"""
    conn = get_db()
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            spec TEXT,
            email TEXT UNIQUE NOT NULL,
            pass TEXT NOT NULL,
            role TEXT DEFAULT 'doctor',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_id INTEGER NOT NULL,
            patient_name TEXT NOT NULL,
            patient_phone TEXT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            type TEXT DEFAULT 'Первичный приём',
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (doctor_id) REFERENCES users (id)
        )
    ''')

    c.execute('SELECT COUNT(*) FROM users')
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO users (name, spec, email, pass, role) VALUES (?, ?, ?, ?, ?)",
                  ('Иванов Иван Иванович', 'Терапевт', 'demo@h.ru', '123', 'doctor'))
        c.execute("INSERT INTO users (name, spec, email, pass, role) VALUES (?, ?, ?, ?, ?)",
                  ('Администратор', 'IT', 'admin@hospital.ru', 'admin123', 'admin'))
        conn.commit()

    conn.close()

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db()
    user = conn.execute(
        'SELECT id, name, spec, email, role FROM users WHERE email = ? AND pass = ? AND role = "doctor"',
        (data['email'], data['pass'])
    ).fetchone()
    conn.close()

    if user:
        return jsonify({'success': True, 'user': dict(user)})
    return jsonify({'success': False, 'message': 'Неверный email или пароль'}), 401
