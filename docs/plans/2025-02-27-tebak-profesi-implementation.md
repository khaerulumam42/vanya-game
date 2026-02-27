# Tebak Profesi Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a web-based educational guessing game for 5-6 year olds where parents upload profession images and kids guess the profession names.

**Architecture:** Simple MVC pattern with Flask backend, SQLite3 database, Jinja2 templating, and vanilla JavaScript for frontend interactions. Session-based game state management.

**Tech Stack:** Flask (Python), SQLite3, Jinja2, Vanilla JavaScript, canvas-confetti library

---

## Task 1: Project Setup & Dependencies

**Files:**
- Create: `requirements.txt`
- Create: `app.py`
- Create: `database.py`

**Step 1: Create requirements.txt**

```txt
Flask==3.0.0
Werkzeug==3.0.1
```

**Step 2: Install dependencies**

Run: `pip install -r requirements.txt`
Expected: Packages installed successfully

**Step 3: Create app.py skeleton**

```python
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
```

**Step 4: Create database.py skeleton**

```python
import sqlite3
import os
from werkzeug.utils import secure_filename

DATABASE = 'tebak_profesi.db'

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
```

**Step 5: Create upload directory**

Run: `mkdir -p static/images/uploads`

**Step 6: Commit**

```bash
git add requirements.txt app.py database.py
git commit -m "feat: setup Flask project skeleton with database"
```

---

## Task 2: Database Functions

**Files:**
- Modify: `database.py`

**Step 1: Add database functions**

Add to `database.py`:

```python
import os
import uuid
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
UPLOAD_FOLDER = 'static/images/uploads'

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
    prof = get_profession_by_id(prof_id)
    if prof:
        # Delete image file
        image_path = prof['image_path']
        if os.path.exists(image_path):
            os.remove(image_path)
        conn.execute('DELETE FROM professions WHERE id = ?', (prof_id,))
        conn.commit()
    conn.close()
```

**Step 2: Create simple test to verify database**

Run: `python3 -c "from database import init_db; init_db(); print('Database initialized')"`
Expected: `Database initialized` and `tebak_profesi.db` file created

**Step 3: Commit**

```bash
git add database.py
git commit -m "feat: add database CRUD functions"
```

---

## Task 3: Base Template & Static Files Setup

**Files:**
- Create: `templates/base.html`
- Create: `static/css/style.css`
- Create: `static/js/game.js`

**Step 1: Create base template**

```html
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Tebak Profesi{% endblock %}</title>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    {% block extra_head %}{% endblock %}
</head>
<body>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
    {% block scripts %}{% endblock %}
</body>
</html>
```

**Step 2: Create style.css with bright colors**

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Nunito', sans-serif;
    background: linear-gradient(135deg, #87CEEB 0%, #98D8C8 100%);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

h1, h2, h3 {
    font-family: 'Fredoka One', cursive;
    color: #1a1a2e;
}

.btn {
    font-family: 'Fredoka One', cursive;
    font-size: 1.5rem;
    padding: 15px 30px;
    border: none;
    border-radius: 50px;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
}

.btn:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
}

.btn-primary {
    background: #FFD700;
    color: #1a1a2e;
}

.btn-secondary {
    background: #FF6B35;
    color: white;
}

.btn-success {
    background: #32CD32;
    color: white;
}

.btn-danger {
    background: #FF69B4;
    color: white;
}
```

**Step 3: Create game.js skeleton**

```javascript
// Game interactions will be added here
console.log('Tebak Profesi game loaded!');
```

**Step 4: Commit**

```bash
git add templates/base.html static/css/style.css static/js/game.js
git commit -m "feat: add base template and static files"
```

---

## Task 4: Landing Page (index.html)

**Files:**
- Create: `templates/index.html`
- Modify: `app.py`

**Step 1: Create landing page template**

```html
{% extends "base.html" %}

{% block title %}Tebak Profesi - Home{% endblock %}

{% block content %}
<div class="landing">
    <h1 class="game-title">🎮 Tebak Profesi 🎮</h1>
    <p class="subtitle">Permainan tebak-tebakan profesi yang seru!</p>

    <div class="choice-container">
        <a href="{{ url_for('admin') }}" class="choice-card admin-card">
            <div class="choice-icon">👨‍👩‍👧</div>
            <h2>Mama Papa</h2>
            <p>Upload gambar profesi</p>
        </a>

        <a href="{{ url_for('play') }}" class="choice-card player-card">
            <div class="choice-icon">👧</div>
            <h2>Vanya</h2>
            <p>Main tebak profesi</p>
        </a>
    </div>
</div>
{% endblock %}
```

**Step 2: Add landing page styles to style.css**

```css
.landing {
    text-align: center;
}

.game-title {
    font-size: 3rem;
    margin-bottom: 10px;
    color: #FF6B35;
    text-shadow: 3px 3px 0 #FFD700;
}

.subtitle {
    font-size: 1.2rem;
    color: #1a1a2e;
    margin-bottom: 40px;
}

.choice-container {
    display: flex;
    gap: 30px;
    justify-content: center;
    flex-wrap: wrap;
}

.choice-card {
    background: white;
    border-radius: 30px;
    padding: 40px;
    min-width: 200px;
    text-decoration: none;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    transition: transform 0.3s;
}

.choice-card:hover {
    transform: translateY(-10px);
}

.choice-icon {
    font-size: 4rem;
    margin-bottom: 20px;
}

.choice-card h2 {
    font-size: 2rem;
    margin-bottom: 10px;
}

.choice-card p {
    color: #666;
}

.admin-card {
    border: 5px solid #FF69B4;
}

.player-card {
    border: 5px solid #32CD32;
}
```

**Step 3: Add admin route to app.py**

Add to `app.py`:
```python
@app.route('/admin')
def admin():
    professions = get_all_professions()
    return render_template('admin.html', professions=professions)

@app.route('/play')
def play():
    count = count_professions()
    return render_template('select_count.html', available_count=count)
```

**Step 4: Test the application**

Run: `python3 app.py`
Visit: `http://localhost:5000`
Expected: Landing page with "Mama Papa" and "Vanya" cards

**Step 5: Commit**

```bash
git add templates/index.html app.py static/css/style.css
git commit -m "feat: add landing page with role selection"
```

---

## Task 5: Admin Page & Image Upload

**Files:**
- Create: `templates/admin.html`
- Modify: `app.py`
- Modify: `static/css/style.css`

**Step 1: Create admin template**

```html
{% extends "base.html" %}

{% block title %}Admin - Upload Profesi{% endblock %}

{% block content %}
<div class="admin-page">
    <h1>👨‍👩‍👧 Mama Papa Admin</h1>

    <div class="upload-section">
        <h2>Upload Profesi Baru</h2>
        <form action="{{ url_for('upload') }}" method="post" enctype="multipart/form-data" class="upload-form">
            <div class="form-group">
                <label for="image">Gambar Profesi:</label>
                <input type="file" name="image" id="image" accept="image/png,image/jpeg,image/webp" required>
            </div>

            <div class="form-group">
                <label for="answer">Jawaban (Nama Profesi):</label>
                <input type="text" name="answer" id="answer" placeholder="Contoh: Dokter" required maxlength="50">
            </div>

            <button type="submit" class="btn btn-primary">Upload!</button>
        </form>
    </div>

    <div class="professions-list">
        <h2>Daftar Profesi ({{ professions|length }})</h2>
        {% if professions %}
        <div class="professions-grid">
            {% for prof in professions %}
            <div class="profession-item">
                <img src="{{ url_for('static', filename=prof.image_path.replace('static/', '')) }}" alt="{{ prof.answer }}">
                <p class="profession-name">{{ prof.answer }}</p>
                <form action="{{ url_for('delete_prof', id=prof.id) }}" method="post" class="delete-form">
                    <button type="submit" class="btn btn-danger btn-small">Hapus</button>
                </form>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <p class="empty-message">Belum ada profesi. Upload yuk!</p>
        {% endif %}
    </div>

    <a href="{{ url_for('index') }}" class="btn btn-secondary">Kembali ke Home</a>
</div>
{% endblock %}
```

**Step 2: Add admin styles to style.css**

```css
.admin-page {
    background: white;
    border-radius: 30px;
    padding: 30px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.upload-section {
    background: #FFF8E7;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 30px;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    font-weight: bold;
    margin-bottom: 8px;
    font-size: 1.1rem;
}

.form-group input[type="file"],
.form-group input[type="text"] {
    width: 100%;
    padding: 12px;
    border: 3px solid #FFD700;
    border-radius: 15px;
    font-size: 1rem;
    font-family: 'Nunito', sans-serif;
}

.professions-list {
    margin-bottom: 30px;
}

.professions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 15px;
}

.profession-item {
    background: #F0F0F0;
    border-radius: 15px;
    padding: 10px;
    text-align: center;
}

.profession-item img {
    width: 100%;
    height: 120px;
    object-fit: cover;
    border-radius: 10px;
    margin-bottom: 10px;
}

.profession-name {
    font-weight: bold;
    margin-bottom: 8px;
}

.btn-small {
    font-size: 1rem;
    padding: 8px 16px;
}

.empty-message {
    text-align: center;
    color: #999;
    font-size: 1.2rem;
}

.delete-form {
    display: inline;
}
```

**Step 3: Add upload and delete routes to app.py**

Add to `app.py`:
```python
import os
from flask import request, flash, jsonify
from werkzeug.utils import secure_filename
from database import add_profession, delete_profession, allowed_file

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
```

**Step 4: Add uuid import and flash template to base.html**

Add to app.py imports: `import uuid`

Add to base.html after content block:
```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        <div class="flash-messages">
        {% for category, message in messages %}
            <div class="flash flash-{{ category }}">{{ message }}</div>
        {% endfor %}
        </div>
    {% endif %}
{% endwith %}
```

Add flash styles to style.css:
```css
.flash-messages {
    margin-bottom: 20px;
}

.flash {
    padding: 15px 20px;
    border-radius: 15px;
    margin-bottom: 10px;
    font-weight: bold;
}

.flash-success {
    background: #32CD32;
    color: white;
}

.flash-error {
    background: #FF69B4;
    color: white;
}
```

**Step 5: Test image upload**

Run: `python3 app.py`
1. Visit `http://localhost:5000/admin`
2. Upload an image and enter a profession name
3. Verify image appears in list

**Step 6: Commit**

```bash
git add templates/admin.html app.py templates/base.html static/css/style.css
git commit -m "feat: add admin page with image upload"
```

---

## Task 6: Select Count Page

**Files:**
- Create: `templates/select_count.html`
- Modify: `app.py`
- Modify: `static/css/style.css`

**Step 1: Create select count template**

```html
{% extends "base.html" %}

{% block title %}Pilih Jumlah Soal{% endblock %}

{% block content %}
<div class="select-count-page">
    <h1>👧 Halo Vanya!</h1>
    <p class="subtitle">Berapa profesi yang ingin ditebak?</p>

    {% if available_count == 0 %}
    <div class="no-data">
        <p>😢 Maaf, belum ada profesi tersedia.</p>
        <p>Mama Papa harus upload dulu ya!</p>
        <a href="{{ url_for('index') }}" class="btn btn-primary">Kembali ke Home</a>
    </div>
    {% else %}
    <div class="count-buttons">
        {% for count in [5, 10, 15, 20] %}
            {% if count <= available_count %}
            <form action="{{ url_for('start_game') }}" method="post">
                <input type="hidden" name="count" value="{{ count }}">
                <button type="submit" class="btn btn-primary count-btn">{{ count }}</button>
            </form>
            {% endif %}
        {% endfor %}
    </div>

    <p class="available-info">Tersedia {{ available_count }} profesi</p>

    <a href="{{ url_for('index') }}" class="btn btn-secondary">Kembali</a>
    {% endif %}
</div>
{% endblock %}
```

**Step 2: Add select count styles**

```css
.select-count-page {
    background: white;
    border-radius: 30px;
    padding: 40px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.count-buttons {
    display: flex;
    gap: 20px;
    justify-content: center;
    flex-wrap: wrap;
    margin: 30px 0;
}

.count-btn {
    width: 80px;
    height: 80px;
    font-size: 2rem;
    border-radius: 50%;
}

.available-info {
    font-size: 1.1rem;
    color: #666;
}

.no-data {
    text-align: center;
}

.no-data p {
    font-size: 1.3rem;
    margin-bottom: 15px;
}
```

**Step 3: Add start_game route to app.py**

```python
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
```

**Step 4: Test count selection**

Run: `python3 app.py`
1. Visit `http://localhost:5000/play`
2. Click on a count button (5, 10, 15, or 20)
3. Verify session is created

**Step 5: Commit**

```bash
git add templates/select_count.html app.py static/css/style.css
git commit -m "feat: add question count selection page"
```

---

## Task 7: Game Page

**Files:**
- Create: `templates/game.html`
- Modify: `app.py`
- Modify: `static/js/game.js`
- Modify: `static/css/style.css`

**Step 1: Create game template**

```html
{% extends "base.html" %}

{% block title %}Tebak Profesi!{% endblock %}

{% block extra_head %}
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
{% endblock %}

{% block content %}
<div class="game-page">
    <div class="game-header">
        <h2 class="game-title-small">Tebak Profesi!</h2>
        <div class="score-display">
            <span class="score-label">Skor:</span>
            <span class="score-value" id="currentScore">0</span>
            <span class="score-divider">/</span>
            <span class="score-total" id="totalScore">5</span>
            <span class="stars" id="starsDisplay"></span>
        </div>
        <div class="question-number">
            Soal <span id="currentQuestion">1</span> dari <span id="totalQuestions">5</span>
        </div>
    </div>

    <div class="game-content">
        <div class="image-container" id="imageContainer">
            <img id="professionImage" src="" alt="Tebak profesi ini!">
        </div>

        <div class="answer-section">
            <input type="text" id="answerInput" placeholder="Jawaban..." autocomplete="off">
            <button id="submitBtn" class="btn btn-primary">Jawab!</button>
        </div>

        <div id="feedback" class="feedback hidden">
            <p id="feedbackText"></p>
        </div>
    </div>
</div>

<div id="loadingModal" class="modal">
    <div class="modal-content">
        <p>Memuat...</p>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
    // Game state from server
    const gameState = {
        total: {{ session.get('game', {}).get('total', 5) }}
    };
</script>
<script src="{{ url_for('static', filename='js/game.js') }}"></script>
{% endblock %}
```

**Step 2: Add game route to app.py**

```python
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
```

**Step 3: Add submit answer route to app.py**

```python
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
```

**Step 4: Add game page styles**

```css
.game-page {
    background: white;
    border-radius: 30px;
    padding: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.game-header {
    text-align: center;
    margin-bottom: 20px;
}

.game-title-small {
    font-size: 1.8rem;
    color: #FF6B35;
    margin-bottom: 10px;
}

.score-display {
    font-size: 1.5rem;
    font-family: 'Fredoka One', cursive;
    margin-bottom: 10px;
}

.score-label {
    color: #666;
}

.score-value {
    color: #32CD32;
    font-size: 2rem;
}

.score-divider {
    color: #999;
}

.score-total {
    color: #666;
}

.stars {
    font-size: 1.5rem;
}

.question-number {
    font-size: 1.1rem;
    color: #999;
}

.game-content {
    text-align: center;
}

.image-container {
    background: #FFF8E7;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 20px;
}

#professionImage {
    max-width: 100%;
    max-height: 350px;
    border-radius: 15px;
}

.answer-section {
    display: flex;
    gap: 10px;
    justify-content: center;
    margin-bottom: 20px;
}

#answerInput {
    flex: 1;
    max-width: 300px;
    padding: 15px 20px;
    font-size: 1.3rem;
    border: 3px solid #FFD700;
    border-radius: 50px;
    text-align: center;
    font-family: 'Nunito', sans-serif;
}

#answerInput:focus {
    outline: none;
    border-color: #FF6B35;
}

#submitBtn {
    padding: 15px 30px;
}

.feedback {
    padding: 20px;
    border-radius: 15px;
    font-size: 1.5rem;
    font-weight: bold;
    margin-top: 20px;
}

.feedback.correct {
    background: #32CD32;
    color: white;
}

.feedback.wrong {
    background: #FF69B4;
    color: white;
}

.feedback.hidden {
    display: none;
}

.modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    justify-content: center;
    align-items: center;
}

.modal.show {
    display: flex;
}

.modal-content {
    background: white;
    padding: 30px;
    border-radius: 20px;
    text-align: center;
}
```

**Step 5: Add game.js logic**

```javascript
let currentScore = 0;
let submitting = false;

document.addEventListener('DOMContentLoaded', function() {
    // Load current profession image
    const imgElement = document.getElementById('professionImage');
    const professionPath = "{{ profession.image_path.replace('static/', '') if profession else '' }}";
    imgElement.src = "{{ url_for('static', filename='') }}" + professionPath;

    // Update UI
    updateScoreDisplay({{ score }});
    document.getElementById('currentQuestion').textContent = {{ current }};
    document.getElementById('totalQuestions').textContent = {{ total }};

    // Auto focus input
    document.getElementById('answerInput').focus();

    // Submit on enter
    document.getElementById('answerInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            submitAnswer();
        }
    });

    // Submit button click
    document.getElementById('submitBtn').addEventListener('click', submitAnswer);
});

function updateScoreDisplay(score) {
    currentScore = score;
    document.getElementById('currentScore').textContent = score;

    // Update stars
    let stars = '';
    for (let i = 0; i < score; i++) {
        stars += '⭐';
    }
    document.getElementById('starsDisplay').textContent = stars;
}

function submitAnswer() {
    if (submitting) return;

    const input = document.getElementById('answerInput');
    const answer = input.value.trim();

    if (!answer) {
        alert('Jawaban tidak boleh kosong!');
        return;
    }

    submitting = true;
    document.getElementById('submitBtn').disabled = true;

    fetch('/game/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ answer: answer })
    })
    .then(response => response.json())
    .then(data => {
        showFeedback(data.correct, data.correct_answer, data.finished);

        if (data.correct) {
            updateScoreDisplay(data.score);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        submitting = false;
        document.getElementById('submitBtn').disabled = false;
    });
}

function showFeedback(isCorrect, correctAnswer, isFinished) {
    const feedback = document.getElementById('feedback');
    const feedbackText = document.getElementById('feedbackText');

    feedback.classList.remove('hidden', 'correct', 'wrong');

    if (isCorrect) {
        feedback.classList.add('correct');
        feedbackText.textContent = '🎉 Benar! Bagus sekali!';
        triggerConfetti();

        setTimeout(() => {
            goToNext(isFinished);
        }, 2000);
    } else {
        feedback.classList.add('wrong');
        feedbackText.textContent = `😅 Jawaban yang benar: ${correctAnswer}`;

        setTimeout(() => {
            goToNext(isFinished);
        }, 3000);
    }
}

function triggerConfetti() {
    confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
    });
}

function goToNext(isFinished) {
    if (isFinished) {
        window.location.href = '/result';
    } else {
        location.reload();
    }
}
```

**Step 6: Test game functionality**

Run: `python3 app.py`
1. Upload at least 5 profession images via admin
2. Start a game with 5 questions
3. Test correct and wrong answers
4. Verify confetti animation works

**Step 7: Commit**

```bash
git add templates/game.html app.py static/js/game.js static/css/style.css
git commit -m "feat: add game page with answer submission"
```

---

## Task 8: Result Page

**Files:**
- Create: `templates/result.html`
- Modify: `app.py`
- Modify: `static/css/style.css`

**Step 1: Create result template**

```html
{% extends "base.html" %}

{% block title %}Hasil Permainan{% endblock %}

{% block extra_head %}
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
{% endblock %}

{% block content %}
<div class="result-page">
    <div class="result-content">
        <h1 class="result-title">🎉 Selesai! 🎉</h1>

        <div class="congratulations">
            <p class="congrats-text">
                Vanya, kamu hebat!
            </p>
            <p class="score-text">
                Bisa menebak <span class="highlight">{{ score }}</span> profesi
                dari <span class="highlight">{{ total }}</span> profesi
            </p>
        </div>

        <div class="score-circle">
            <div class="score-number">{{ score }}/{{ total }}</div>
            <div class="score-label">Skor</div>
        </div>

        <div class="stars-display">
            {% for i in range(score) %}
            <span class="star">⭐</span>
            {% endfor %}
        </div>

        <div class="action-buttons">
            <a href="{{ url_for('play') }}" class="btn btn-primary">Main Lagi!</a>
            <a href="{{ url_for('index') }}" class="btn btn-secondary">Ke Home</a>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
    // Trigger celebration confetti
    setTimeout(function() {
        confetti({
            particleCount: 150,
            spread: 100,
            origin: { y: 0.6 }
        });

        setTimeout(function() {
            confetti({
                particleCount: 100,
                angle: 60,
                spread: 55,
                origin: { x: 0 }
            });
            confetti({
                particleCount: 100,
                angle: 120,
                spread: 55,
                origin: { x: 1 }
            });
        }, 500);
    }, 300);
</script>
{% endblock %}
```

**Step 2: Add result route to app.py**

```python
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
```

**Step 3: Add result page styles**

```css
.result-page {
    background: white;
    border-radius: 30px;
    padding: 40px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.result-title {
    font-size: 3rem;
    color: #FF6B35;
    margin-bottom: 30px;
}

.congratulations {
    margin-bottom: 30px;
}

.congrats-text {
    font-size: 1.8rem;
    font-weight: bold;
    color: #1a1a2e;
    margin-bottom: 15px;
}

.score-text {
    font-size: 1.3rem;
    color: #666;
}

.highlight {
    color: #FFD700;
    font-weight: bold;
    font-size: 1.5rem;
}

.score-circle {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
    margin: 0 auto 30px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: 0 10px 25px rgba(255, 215, 0, 0.4);
}

.score-number {
    font-size: 2.5rem;
    font-weight: bold;
    color: #1a1a2e;
}

.score-label {
    font-size: 1rem;
    color: #1a1a2e;
}

.stars-display {
    font-size: 2.5rem;
    margin-bottom: 30px;
}

.star {
    display: inline-block;
    animation: starPop 0.5s ease-out;
    animation-fill-mode: both;
}

@keyframes starPop {
    0% {
        transform: scale(0);
        opacity: 0;
    }
    50% {
        transform: scale(1.3);
    }
    100% {
        transform: scale(1);
        opacity: 1;
    }
}

.action-buttons {
    display: flex;
    gap: 15px;
    justify-content: center;
    flex-wrap: wrap;
}
```

**Step 4: Test result page**

Run: `python3 app.py`
1. Complete a full game
2. Verify result page shows correct score
3. Verify confetti animation plays
4. Test "Main Lagi!" and "Ke Home" buttons

**Step 5: Commit**

```bash
git add templates/result.html app.py static/css/style.css
git commit -m "feat: add result page with celebration"
```

---

## Task 9: Mobile Responsiveness

**Files:**
- Modify: `static/css/style.css`

**Step 1: Add media queries to style.css**

Add at the end of style.css:

```css
/* Mobile Responsiveness */
@media (max-width: 600px) {
    .game-title {
        font-size: 2rem;
    }

    .choice-container {
        flex-direction: column;
        align-items: center;
    }

    .choice-card {
        min-width: 100%;
        padding: 30px;
    }

    .admin-page,
    .select-count-page,
    .game-page,
    .result-page {
        padding: 20px;
    }

    .professions-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .count-buttons {
        flex-wrap: wrap;
    }

    .count-btn {
        width: 70px;
        height: 70px;
        font-size: 1.5rem;
    }

    .answer-section {
        flex-direction: column;
        align-items: center;
    }

    #answerInput {
        max-width: 100%;
        font-size: 1.1rem;
    }

    #professionImage {
        max-height: 250px;
    }

    .result-title {
        font-size: 2rem;
    }

    .score-circle {
        width: 120px;
        height: 120px;
    }

    .score-number {
        font-size: 2rem;
    }

    .action-buttons {
        flex-direction: column;
    }

    .action-buttons .btn {
        width: 100%;
    }
}
```

**Step 2: Test on mobile view**

1. Open browser DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Test various mobile screen sizes
4. Verify all elements are accessible

**Step 3: Commit**

```bash
git add static/css/style.css
git commit -m "feat: add mobile responsive design"
```

---

## Task 10: Final Testing & Polish

**Step 1: Complete end-to-end testing**

1. **Landing Page:**
   - [ ] Both "Mama Papa" and "Vanya" buttons work
   - [ ] Design looks bright and fun

2. **Admin Flow:**
   - [ ] Upload image with valid formats (jpg, png, webp)
   - [ ] Upload rejection for invalid formats
   - [ ] Empty answer validation
   - [ ] Image appears in list after upload
   - [ ] Delete removes both file and database entry

3. **Game Flow (No Data):**
   - [ ] Shows message when no professions available

4. **Game Flow (With Data):**
   - [ ] Count buttons only show available options
   - [ ] Game starts with selected count
   - [ ] Questions appear one by one
   - [ ] Correct answer shows confetti + "Benar!"
   - [ ] Wrong answer shows correct answer
   - [ ] Score updates correctly
   - [ ] All questions are asked before result

5. **Result Page:**
   - [ ] Shows correct score message
   - [ ] Celebration confetti plays
   - [ ] "Main Lagi!" starts new game
   - [ ] "Ke Home" returns to landing

6. **Mobile:**
   - [ ] All pages responsive
   - [ ] Touch targets large enough
   - [ ] Text is readable

**Step 2: Add sample data for testing**

Upload 5-10 sample profession images through admin page:
- Dokter (Doctor)
- Guru (Teacher)
- Polisi (Police)
- Petani (Farmer)
- Nelayan (Fisherman)
- Pilot
- Masinis (Train Driver)
- Koki (Chef)

**Step 3: Final commit**

```bash
git add -A
git commit -m "feat: complete Tebak Profesi game implementation"
```

---

## Summary

This implementation plan creates a complete educational game for 5-6 year olds with:

- ✅ Bright, colorful design
- ✅ Admin page for image upload
- ✅ Kid-friendly game interface
- ✅ Celebration animations (confetti)
- ✅ Score tracking and feedback
- ✅ Mobile responsive
- ✅ Indonesian language UI

**Total estimated tasks:** 10
**Estimated time:** 2-3 hours for full implementation
