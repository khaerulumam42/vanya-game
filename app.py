from flask import Flask, render_template, session, redirect, url_for
from database import init_db, get_all_professions, add_profession, delete_profession, get_profession_by_id

app = Flask(__name__)
app.secret_key = 'change-this-secret-key-in-production'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max upload
app.config['UPLOAD_FOLDER'] = 'static/images/uploads'

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
