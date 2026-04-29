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
    conn.row_factory = sqlite3.Row  # Возвращает строки как словари
    return conn