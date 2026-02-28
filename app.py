import os
import uuid
from flask import Flask, render_template, session, redirect, url_for, request, flash, jsonify
from werkzeug.utils import secure_filename
from database import init_db, get_all_professions, count_professions, add_profession, delete_profession, get_profession_by_id, get_random_professions, allowed_file

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

@app.route('/play/start', methods=['POST'])
def start_game():
    count = int(request.form.get('count', 5))
    available = count_professions()

    if available == 0:
        return redirect(url_for('play'))

    # Cap at available count
    actual_count = min(count, available)

    # Get random professions
    professions = get_random_professions(actual_count)

    # Initialize game session
    session['game'] = {
        'profession_ids': [p['id'] for p in professions],
        'current_index': 0,
        'score': 0,
        'total': actual_count,
        'answers': []
    }

    return redirect(url_for('game'))

@app.route('/game')
def game():
    if 'game' not in session:
        return redirect(url_for('index'))

    game_data = session['game']
    current_index = game_data['current_index']

    # Check if game is finished
    if current_index >= game_data['total']:
        return redirect(url_for('result'))

    # Get current profession
    prof_id = game_data['profession_ids'][current_index]
    profession = get_profession_by_id(prof_id)

    return render_template('game.html',
        profession=profession,
        score=game_data['score'],
        total=game_data['total'],
        current=current_index + 1
    )

@app.route('/game/submit', methods=['POST'])
def submit_answer():
    if 'game' not in session:
        return jsonify({'error': 'No active game'}), 400

    user_answer = request.json.get('answer', '').strip().lower()
    game_data = session['game']
    current_index = game_data['current_index']
    prof_id = game_data['profession_ids'][current_index]
    profession = get_profession_by_id(prof_id)

    correct_answer = profession['answer'].strip().lower()
    is_correct = user_answer == correct_answer

    # Record answer
    game_data['answers'].append({
        'id': prof_id,
        'user_answer': user_answer,
        'correct': is_correct,
        'correct_answer': correct_answer
    })

    if is_correct:
        game_data['score'] += 1

    # Move to next question
    game_data['current_index'] += 1
    session['game'] = game_data

    finished = game_data['current_index'] >= game_data['total']

    return jsonify({
        'correct': is_correct,
        'correct_answer': profession['answer'],
        'finished': finished,
        'score': game_data['score'],
        'total': game_data['total']
    })

@app.route('/result')
def result():
    if 'game' not in session:
        return redirect(url_for('index'))

    game_data = session['game']
    score = game_data['score']
    total = game_data['total']

    # Clear session
    session.pop('game', None)

    return render_template('result.html', score=score, total=total)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
