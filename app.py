import os
import uuid
from flask import Flask, render_template, session, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
from database import init_db, get_all_professions, count_professions, add_profession, delete_profession, allowed_file

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

@app.route('/admin/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        flash('Tidak ada file yang dipilih', 'error')
        return redirect(url_for('admin'))

    file = request.files['image']
    answer = request.form.get('answer', '').strip()

    if file.filename == '':
        flash('Tidak ada file yang dipilih', 'error')
        return redirect(url_for('admin'))

    if not allowed_file(file.filename):
        flash('Format file harus PNG, JPG, JPEG, atau WebP', 'error')
        return redirect(url_for('admin'))

    if not answer:
        flash('Jawaban tidak boleh kosong', 'error')
        return redirect(url_for('admin'))

    # Generate unique filename
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Save to database
    image_path = f"static/images/uploads/{filename}"
    add_profession(image_path, answer)

    flash('Profesi berhasil ditambahkan!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/delete/<int:id>', methods=['POST'])
def delete_prof(id):
    delete_profession(id)
    flash('Profesi berhasil dihapus!', 'success')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
