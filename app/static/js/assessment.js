document.addEventListener('DOMContentLoaded', () => {
    const optionCards = document.querySelectorAll('.option-card');
    const nextBtn = document.getElementById('next-btn');
    const submitBtn = document.getElementById('submit-btn');
    const timeTakenDisplay = document.getElementById('time-taken-display');
    const bottomTimeDisplay = document.getElementById('bottom-time-display');
    const timerText = document.getElementById('timer-text');
    const qId = document.getElementById('question-id')?.value;
    const qNum = document.getElementById('question-num')?.value;

    const QUESTION_TIME_LIMIT = 30;
    let selectedValue = null;
    let startTime = Date.now();
    let remainingSeconds = QUESTION_TIME_LIMIT;
    let timerInterval = null;

    function updateTimerDisplay(seconds) {
        if (timerText) {
            timerText.textContent = seconds;
            timerText.style.color = seconds <= 10 ? '#dc3545' : '#003366';
        }
    }

    function startQuestionTimer() {
        clearInterval(timerInterval);
        remainingSeconds = QUESTION_TIME_LIMIT;
        updateTimerDisplay(remainingSeconds);

        timerInterval = setInterval(() => {
            remainingSeconds -= 1;
            updateTimerDisplay(Math.max(0, remainingSeconds));

            if (remainingSeconds <= 0) {
                clearInterval(timerInterval);
                submitAnswer(true);
            }
        }, 1000);
    }

    function selectOption(card) {
        optionCards.forEach(c => c.classList.remove('selected'));
        card.classList.add('selected');
        selectedValue = card.getAttribute('data-value');

        const timeTakenSec = Math.round((Date.now() - startTime) / 1000);
        if (timeTakenDisplay) {
            timeTakenDisplay.textContent = `⏱ Attempted in ${timeTakenSec} seconds`;
            timeTakenDisplay.style.display = 'block';
        }
        if (bottomTimeDisplay) {
            bottomTimeDisplay.textContent = `⏱ ${timeTakenSec}s`;
        }

        if (submitBtn) submitBtn.disabled = false;
        if (nextBtn) nextBtn.disabled = false;
    }

    optionCards.forEach(card => {
        card.addEventListener('click', () => selectOption(card));
    });

    document.addEventListener('keydown', (e) => {
        const currentSelected = document.querySelector('.option-card.selected');
        const cards = Array.from(optionCards);
        let index = cards.indexOf(currentSelected);

        if (e.key === 'ArrowDown') {
            index = (index + 1) % cards.length;
            if (cards[index]) selectOption(cards[index]);
        } else if (e.key === 'ArrowUp') {
            index = (index - 1 + cards.length) % cards.length;
            if (cards[index]) selectOption(cards[index]);
        } else if (e.key === 'Enter' && selectedValue !== null) {
            submitAnswer(false);
        }
    });

    function getPayload(autoSubmitted = false) {
        const timeTaken = Math.round((Date.now() - startTime) / 1000);
        return {
            question_id: qId,
            selected_option: selectedValue,
            time_taken: timeTaken,
            auto_submitted: autoSubmitted && selectedValue === null
        };
    }

    async function saveResponse(autoSubmitted = false) {
        const payload = getPayload(autoSubmitted);
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        try {
            const response = await fetch(`/student/assessment/answer?q_num=${qNum}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(payload)
            });
            return await response.json();
        } catch (error) {
            console.error('Error saving response:', error);
            return null;
        }
    }

    window.goToQuestion = function (targetNum) {
        if (targetNum && targetNum > 0) {
            window.location.href = `/student/assessment/question/${targetNum}`;
        }
    };

    window.submitAnswer = async function (autoSubmitted = false) {
        clearInterval(timerInterval);
        const result = await saveResponse(autoSubmitted);

        if (result && result.success) {
            if (result.is_last) {
                await completeAssessment();
            } else {
                window.location.href = `/student/assessment/question/${result.next_question}`;
            }
        }
    };

    async function completeAssessment() {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        const response = await fetch('/student/assessment/complete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ total_time: Math.round((Date.now() - startTime) / 1000) })
        });
        const result = await response.json();
        if (result.success) {
            window.location.href = result.redirect;
        }
    }

    startQuestionTimer();
    if (submitBtn) submitBtn.disabled = false;
    if (nextBtn) nextBtn.disabled = false;
});


