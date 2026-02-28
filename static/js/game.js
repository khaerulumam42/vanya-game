let currentScore = 0;
let submitting = false;

document.addEventListener('DOMContentLoaded', function() {
    // Load current profession image
    const imgElement = document.getElementById('professionImage');
    imgElement.src = window.gameData.staticPath + window.gameData.professionPath;

    // Update UI
    updateScoreDisplay(window.gameData.score);
    document.getElementById('currentQuestion').textContent = window.gameData.current;
    document.getElementById('totalQuestions').textContent = window.gameData.total;

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
