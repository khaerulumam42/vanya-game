# Tebak Profesi

An educational web-based guessing game for 5-6 year old children. Kids guess profession names based on images, while parents can upload new profession images and answers through an admin interface.

## Project Summary

**Target Audience:** Children aged 5-6 years old
**Language:** Indonesian (Bahasa Indonesia)
**Framework:** Flask (Python) with SQLite3 database
**Architecture:** Simple MVC pattern with Jinja2 templating

### Features

- **Admin Interface (Mama Papa):** Upload profession images with correct answers
- **Game Interface (Vanya):** Kid-friendly guessing game with:
  - Question count selection (5, 10, 15, or 20 questions)
  - Real-time score tracking with stars
  - Instant feedback with confetti celebrations
  - Bright, colorful design optimized for children
- **Mobile Responsive:** Works on tablets and phones

---

## How to Run

### Prerequisites

- Python 3.8+
- Virtual environment (venv)

### Setup

1. **Navigate to the project directory:**
   ```bash
   cd /home/etc/claude-code/vanya-game/.worktrees/tebak-profesi
   ```

2. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies** (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Make sure the virtual environment is activated:**
   ```bash
   source venv/bin/activate
   ```

2. **Start the Flask server:**
   ```bash
   python3 app.py
   ```

3. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

4. **To stop the server:** Press `Ctrl+C` in the terminal

---

## How to Test

### Manual Testing Checklist

#### 1. Landing Page
- [ ] Page loads at `http://localhost:5000`
- [ ] Both "Mama Papa" and "Vanya" cards are visible
- [ ] Design looks bright and colorful
- [ ] Hover effects work on buttons

#### 2. Admin Flow (Mama Papa)
- [ ] Navigate to `/admin` or click "Mama Papa"
- [ ] Upload form displays correctly
- [ ] Can select image files (png, jpg, jpeg, webp)
- [ ] Can type profession name
- [ ] Upload button works
- [ ] Uploaded images appear in the list
- [ ] Delete button removes images
- [ ] Flash messages appear (success/error)

#### 3. Game Flow (Vanya - No Data)
- [ ] Navigate to `/play` or click "Vanya"
- [ ] Shows "no data available" message when database is empty
- [ ] Suggests parent should upload first

#### 4. Game Flow (Vanya - With Data)
- [ ] Count buttons (5, 10, 15, 20) appear based on available data
- [ ] Clicking a count button starts the game
- [ ] First profession image displays
- [ ] Answer input field accepts text
- [ ] Submit button works
- [ ] Correct answer triggers confetti + "Benar!" message
- [ ] Wrong answer shows correct answer
- [ ] Score updates correctly
- [ ] All questions are asked before showing results

#### 5. Result Page
- [ ] Shows correct score (e.g., "4 dari 5")
- [ ] Congratulation message appears
- [ ] Confetti celebration plays
- [ ] "Main Lagi!" button starts new game
- [ ] "Ke Home" button returns to landing page

#### 6. Mobile Responsiveness
- Open browser DevTools (F12) and toggle device toolbar
- [ ] Layout adapts to mobile screens
- [ ] Buttons are touch-friendly (large enough)
- [ ] Text remains readable
- [ ] Images scale properly

### Adding Test Data

Upload 5-10 sample profession images through the admin page:
- Dokter (Doctor)
- Guru (Teacher)
- Polisi (Police)
- Petani (Farmer)
- Nelayan (Fisherman)
- Pilot
- Masinis (Train Driver)
- Koki (Chef)

---

## Virtual Environment

**Location:** `venv/` in the project root

**Activation:**
```bash
source venv/bin/activate
```

**Deactivation:**
```bash
deactivate
```

**Installed Packages:**
- Flask==3.0.0
- Werkzeug==3.0.1

**Important:** Always activate the venv before running the application or running Python commands!

---

## Project Structure

```
tebak-profesi/
├── app.py                      # Main Flask application
├── database.py                 # SQLite database functions
├── requirements.txt            # Python dependencies
├── venv/                       # Virtual environment (DO NOT COMMIT)
├── tebak_profesi.db           # SQLite database (auto-created)
├── static/
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   ├── js/
│   │   └── game.js            # Game logic
│   └── images/
│       └── uploads/           # User-uploaded profession images
├── templates/
│   ├── base.html              # Base template
│   ├── index.html             # Landing page
│   ├── admin.html             # Admin upload page
│   ├── select_count.html      # Question count selection
│   ├── game.html              # Main game page
│   └── result.html            # Results page
└── docs/
    └── plans/                 # Design and implementation documents
```

---

## Development Notes

- **Secret Key:** Currently set to placeholder value - change for production
- **Debug Mode:** Enabled (`debug=True`) - disable for production
- **Upload Limit:** 5MB max file size
- **Allowed Formats:** PNG, JPG, JPEG, WebP
- **Database:** SQLite3 with single `professions` table

---

## Browser Compatibility

Tested on modern browsers:
- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

Minimum version: Any browser from 2018 onwards (for CSS flexbox and gradient support)
