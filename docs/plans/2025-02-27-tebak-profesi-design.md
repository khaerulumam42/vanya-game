# Tebak Profesi - Design Document

**Date:** 2025-02-27
**Target Audience:** Kids aged 5-6 years old
**Framework:** Flask + SQLite3 + Vanilla JavaScript

---

## Overview

"Tebak Profesi" (Guess the Profession) is a web-based educational game where children guess professions based on images. Parents (Mama Papa) can upload profession images and answers, while kids (Vanya) play the guessing game.

---

## Architecture

### Project Structure

```
vanya-game/
├── app.py                      # Main Flask application
├── database.py                 # SQLite3 database functions
├── static/
│   ├── css/
│   │   └── style.css          # Bright, fun styling
│   ├── js/
│   │   └── game.js            # Game logic & animations
│   ├── images/                # Profession images (uploaded)
│   │   └── uploads/           # User uploaded profession photos
│   └── confetti/
│       └── confetti.js        # Celebration animation library
└── templates/
    ├── base.html              # Base template with shared layout
    ├── index.html             # Landing page (Mama Papa / Vanya)
    ├── admin.html             # Admin upload form
    ├── select_count.html      # Choose number of questions
    ├── game.html              # Main game page
    └── result.html            # Final score & congratulations
```

### Technology Stack
- **Flask** - Python web framework
- **SQLite3** - Database storage
- **Jinja2** - HTML templating
- **Vanilla JavaScript** - Frontend logic
- **canvas-confetti** - Celebration animations

---

## Database Schema

```sql
CREATE TABLE professions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_path TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Game Flow

```
Landing Page (Choose Mama Papa or Vanya)
│
├─ Mama Papa (Admin)
│  └─ Upload form: [Image] + [Answer]
│     └─ List of uploaded items (delete option)
│
└─ Vanya (Player)
   └─ Select count: [5] [10] [15] [20]
      └─ Game: Show image → Type answer → Submit
         └─ Result: "Vanya, kamu hebat! Bisa menebak X profesi dari Y profesi"
```

---

## Color Scheme (Bright & Kid-Friendly)

| Element | Color | Hex |
|---------|-------|-----|
| Primary (buttons) | Bright Yellow | `#FFD700` |
| Background | Sky Blue | `#87CEEB` |
| Accents | Orange, Pink, Green | `#FF6B35`, `#FF69B4`, `#32CD32` |
| Text | Dark Navy | `#1a1a2e` |

---

## Backend Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Landing page |
| `/admin` | GET | Admin upload page |
| `/admin/upload` | POST | Upload image + save profession |
| `/admin/delete/<id>` | POST | Delete profession |
| `/play` | GET | Select question count |
| `/play/start` | POST | Start game session |
| `/game` | GET | Game page |
| `/game/submit` | POST | Submit answer (JSON response) |
| `/result` | GET | Final score page |

---

## Session Data

```python
session['game'] = {
    'profession_ids': [1, 5, 8, 12, 3],   # Randomly selected
    'current_index': 0,                   # Current question
    'score': 0,                           # Correct answers
    'total': 5,                           # Total questions
    'answers': [...]                      # Answer history
}
```

---

## Game Mechanics

### Answer Validation
- **Exact match** required (case-insensitive, trimmed)
- **Instant feedback** on each answer
- **Correct:** Green flash, confetti, "Benar!", 2s delay → next
- **Wrong:** Red flash, sad face, show correct answer, 3s delay → next

### Celebration Animations
- Correct answer: Confetti burst from center
- Game completion: Full-screen confetti + stars

---

## Error Handling

| Scenario | Handling |
|----------|----------|
| No professions available | "Data belum tersedia. Mama Papa harus upload dulu!" |
| Requested count > available | Cap at available count |
| Invalid image type | Accept only jpg, jpeg, png, webp |
| Image > 5MB | Show error message |
| Empty answer | "Jawaban tidak boleh kosong!" |

---

## Testing Checklist

- [ ] Landing page displays both options
- [ ] Admin upload works correctly
- [ ] Delete removes both DB entry and file
- [ ] Game starts with selected count
- [ ] Questions are randomized
- [ ] Correct/wrong answers handled properly
- [ ] Result page shows correct message
- [ ] Mobile responsive
