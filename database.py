import sqlite3
import os
import uuid
from werkzeug.utils import secure_filename

DATABASE = 'tebak_profesi.db'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
UPLOAD_FOLDER = 'static/images/uploads'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS professions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_all_professions():
    conn = get_db()
    rows = conn.execute('SELECT * FROM professions ORDER BY created_at DESC').fetchall()
    conn.close()
    return rows

def add_profession(image_path, answer):
    conn = get_db()
    cursor = conn.execute('INSERT INTO professions (image_path, answer) VALUES (?, ?)', (image_path, answer))
    conn.commit()
    conn.close()
    return cursor.lastrowid

def get_profession_by_id(prof_id):
    conn = get_db()
    row = conn.execute('SELECT * FROM professions WHERE id = ?', (prof_id,)).fetchone()
    conn.close()
    return row

def get_random_professions(count):
    conn = get_db()
    rows = conn.execute('SELECT * FROM professions ORDER BY RANDOM() LIMIT ?', (count,)).fetchall()
    conn.close()
    return rows

def count_professions():
    conn = get_db()
    row = conn.execute('SELECT COUNT(*) as count FROM professions').fetchone()
    conn.close()
    return row['count']

def delete_profession(prof_id):
    conn = get_db()
    prof = conn.execute('SELECT * FROM professions WHERE id = ?', (prof_id,)).fetchone()
    if prof:
        # Delete image file
        image_path = prof['image_path']
        if os.path.exists(image_path):
            os.remove(image_path)
        conn.execute('DELETE FROM professions WHERE id = ?', (prof_id,))
        conn.commit()
    conn.close()

