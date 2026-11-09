document.addEventListener('DOMContentLoaded', () => {
    // Initialize sequence from the script tag
    // Note: The variable 'sequence' is expected to be defined in the HTML via json_script, 
    // but here we grab it from the DOM element directly if needed, 
    // or rely on the global variable if defined before this script.
    // However, json_script creates a script tag with id="sequence-data".
    
    const sequenceDataElement = document.getElementById('sequence-data');
    if (sequenceDataElement) {
        window.sequence = JSON.parse(sequenceDataElement.textContent);
        updateCarousel();
    }
});

let currentIndex = 0;
let timeRemaining = 0;
let isRunning = false;
let interval = null;
let totalTimerInterval = null;
let totalSeconds = 0;
let jarvisVoice = null;

function initVoice() {
    const voices = window.speechSynthesis.getVoices();
    jarvisVoice = voices.find(v => v.lang.startsWith('fr') && v.name.includes('Google')) || 
                  voices.find(v => v.lang.startsWith('fr')) || 
                  voices[0];
}

if (speechSynthesis.onvoiceschanged !== undefined) {
    speechSynthesis.onvoiceschanged = initVoice;
}

function speak(text) {
    if (!text) return;
    const p = document.createElement('p');
    p.innerText = `> ${text}`;
    p.classList.add('animate-fade-in');
    const log = document.getElementById('ai-log');
    if (log) {
        log.prepend(p);
        if (log.children.length > 6) log.lastChild.remove();
    }

    const utterance = new SpeechSynthesisUtterance(text);
    if (jarvisVoice) utterance.voice = jarvisVoice;
    utterance.rate = 1.1; 
    utterance.pitch = 0.9;
    window.speechSynthesis.speak(utterance);
}

function formatTime(seconds) {
    const m = Math.floor(seconds / 60).toString().padStart(2, '0');
    const s = (seconds % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
}

function updateTotalTimer() {
    totalSeconds++;
    const totalTimer = document.getElementById('total-timer');
    if (totalTimer) totalTimer.innerText = formatTime(totalSeconds);
}

function updateCarousel() {
    const items = document.querySelectorAll('.carousel-item');
    items.forEach((item, idx) => {
        const offset = idx - currentIndex;
        
        if (offset === 0) {
            // Active
            item.style.transform = 'translateZ(0) scale(1)';
            item.style.opacity = '1';
            item.style.zIndex = '10';
            item.classList.add('border-energy', 'shadow-[0_0_40px_rgba(234,179,8,0.3)]');
            item.classList.remove('border-energy/30');
        } else if (offset === 1) {
            // Next
            item.style.transform = 'translateZ(-200px) translateX(60%) rotateY(-15deg)';
            item.style.opacity = '0.3';
            item.style.zIndex = '5';
            item.classList.remove('border-energy', 'shadow-[0_0_40px_rgba(234,179,8,0.3)]');
            item.classList.add('border-energy/30');
        } else if (offset === -1) {
            // Prev
            item.style.transform = 'translateZ(-200px) translateX(-60%) rotateY(15deg)';
            item.style.opacity = '0.3';
            item.style.zIndex = '5';
            item.classList.remove('border-energy', 'shadow-[0_0_40px_rgba(234,179,8,0.3)]');
            item.classList.add('border-energy/30');
        } else {
            // Hidden
            item.style.transform = 'translateZ(-500px) scale(0)';
            item.style.opacity = '0';
            item.style.zIndex = '0';
        }
    });
}

function startStep() {
    if (!window.sequence) return;
    const step = window.sequence[currentIndex];
    timeRemaining = step.duration;
    updateCarousel();
    
    let intro = step.name;
    // Use translated text from config if available
    if(step.type === 'rest' && window.workoutConfig && window.workoutConfig.textRest) {
        intro = window.workoutConfig.textRest;
    }
    speak(intro);
    
    clearInterval(interval);
    interval = setInterval(() => {
        if (!isRunning) return;
        
        timeRemaining--;
        const timerDisplay = document.getElementById(`timer-${currentIndex}`);
        if(timerDisplay) timerDisplay.innerText = timeRemaining;
        
        if (timeRemaining <= 3 && timeRemaining > 0) speak(timeRemaining);
        
        if (timeRemaining <= 0) {
            completeStep();
        }
    }, 1000);
}

function completeStep() {
    clearInterval(interval);
    if (window.workoutConfig && window.workoutConfig.textDone) {
        speak(window.workoutConfig.textDone);
    }
    
    currentIndex++;
    if (currentIndex < window.sequence.length) {
        setTimeout(startStep, 1000);
    } else {
        finishSession();
    }
}

function finishSession() {
    isRunning = false;
    clearInterval(totalTimerInterval);
    if (window.workoutConfig && window.workoutConfig.textSessionDone) {
        speak(window.workoutConfig.textSessionDone);
    }

    // Call Backend to record completion
    const csrfToken = window.workoutConfig ? window.workoutConfig.csrfToken : '';
    fetch(`/${document.documentElement.lang}/workout/complete/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        // We could display the energy gain here if we wanted to dynamically update the UI
    })
    .catch(error => console.error('Error recording workout:', error));
    
    // Show Report Modal
    const modal = document.getElementById('session-report');
    const card = document.getElementById('report-card');
    if (modal && card) {
        modal.classList.remove('hidden');
        // Small delay to allow display:block to apply before opacity transition
        setTimeout(() => {
            modal.classList.remove('opacity-0');
            card.classList.remove('scale-95');
            card.classList.add('scale-100');
        }, 50);
    }
}

function toggleSession() {
    isRunning = !isRunning;
    const iconPlay = document.getElementById('icon-play');
    const iconPause = document.getElementById('icon-pause');
    if(iconPlay) iconPlay.classList.toggle('hidden');
    if(iconPause) iconPause.classList.toggle('hidden');
    
    if (isRunning) {
        if (!totalTimerInterval) {
            totalTimerInterval = setInterval(updateTotalTimer, 1000);
        }
        if (timeRemaining === 0 && currentIndex === 0) {
            initVoice();
            if (window.workoutConfig && window.workoutConfig.textInit) {
                speak(window.workoutConfig.textInit);
            }
            startStep();
        } else {
            if (window.workoutConfig && window.workoutConfig.textResume) {
                speak(window.workoutConfig.textResume);
            }
        }
    } else {
        clearInterval(totalTimerInterval);
        totalTimerInterval = null;
        if (window.workoutConfig && window.workoutConfig.textPause) {
            speak(window.workoutConfig.textPause);
        }
    }
}

function skipStep() {
    if (window.workoutConfig && window.workoutConfig.textNext) {
        speak(window.workoutConfig.textNext);
    }
    completeStep();
}
