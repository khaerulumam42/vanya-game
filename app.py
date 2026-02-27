from flask import Flask, render_template, session, redirect, url_for
from database import init_db, get_all_professions, count_professions

app = Flask(__name__)
app.secret_key = 'change-this-secret-key-in-production'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max upload
app.config['UPLOAD_FOLDER'] = 'static/images/uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    professions = get_all_professions()
    return render_template('admin.html', professions=professions)

@app.route('/play')
def play():
    count = count_professions()
    return render_template('select_count.html', available_count=count)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
