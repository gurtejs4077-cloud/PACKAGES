/**
 * Global Audio Manager for Lumière Studio
 * Handles the welcome popup and persistent background music.
 */

const AudioManager = {
    audio: null,
    storageKeys: {
        accepted: 'lumiere_welcome_accepted',
        playing: 'lumiere_audio_playing',
        time: 'lumiere_audio_time'
    },

    init() {
        this.setupAudio();
        this.setupUI();
        
        // Listen for visibility changes to sync time
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.saveTime();
            }
        });

        // Save time periodically
        setInterval(() => {
            if (this.audio && !this.audio.paused) {
                this.saveTime();
            }
        }, 1000);

        // Check if we should show the popup
        if (!localStorage.getItem(this.storageKeys.accepted)) {
            setTimeout(() => this.showPopup(), 500);
        } else if (localStorage.getItem(this.storageKeys.playing) === 'true') {
            this.resumeAudio();
        }
    },

    setupAudio() {
        this.audio = new Audio('sound.mp3');
        this.audio.loop = true;
        this.audio.volume = 0.5; // Start at 50% volume for better UX
    },

    setupUI() {
        // Build Popup HTML
        const popupHTML = `
            <div id="welcome-popup-overlay">
                <div class="welcome-popup-card">
                    <span class="welcome-popup-logo">LUMIÈRE</span>
                    <h2 class="welcome-popup-title">Experience the<br><em>Art of Light</em></h2>
                    <p class="welcome-popup-text">
                        To fully immerse yourself in our studio's atmosphere, we recommend enabling our ambient soundscape.
                    </p>
                    <button id="continue-btn" class="welcome-popup-btn">Continue to Studio</button>
                    <div style="margin-top: 1.5rem; opacity: 0.5; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; color: #b8b0a2;">
                        sound.mp3 will play in background
                    </div>
                </div>
            </div>
            <div id="audio-control" title="Toggle Music">
                <div class="music-waves">
                    <div class="wave"></div>
                    <div class="wave"></div>
                    <div class="wave"></div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', popupHTML);

        // Event Listeners
        const continueBtn = document.getElementById('continue-btn');
        if (continueBtn) {
            continueBtn.addEventListener('click', () => this.handleContinue());
        }

        const audioCtrl = document.getElementById('audio-control');
        if (audioCtrl) {
            audioCtrl.addEventListener('click', () => this.toggleAudio());
        }
    },

    showPopup() {
        const overlay = document.getElementById('welcome-popup-overlay');
        if (overlay) overlay.classList.add('show');
    },

    hidePopup() {
        const overlay = document.getElementById('welcome-popup-overlay');
        if (overlay) overlay.classList.remove('show');
    },

    handleContinue() {
        localStorage.setItem(this.storageKeys.accepted, 'true');
        localStorage.setItem(this.storageKeys.playing, 'true');
        this.hidePopup();
        this.playAudio();
        this.showControl();
    },

    playAudio() {
        const savedTime = localStorage.getItem(this.storageKeys.time) || 0;
        this.audio.currentTime = parseFloat(savedTime);
        
        const playPromise = this.audio.play();
        if (playPromise !== undefined) {
            playPromise.then(() => {
                document.getElementById('audio-control')?.classList.remove('paused');
            }).catch(error => {
                console.log("Playback blocked by browser. User interaction required.");
                // If it fails (e.g. on subsequent pages without interaction), 
                // we keep the UI in a ready state.
                document.getElementById('audio-control')?.classList.add('paused');
            });
        }
    },

    resumeAudio() {
        this.showControl();
        // Browser might block autoplay even if previously accepted on a different page.
        // We try to play, but it might fail until they click somewhere.
        this.playAudio();
        
        // As a fallback, try to play on first click anywhere if it's supposed to be playing
        const startOnInteraction = () => {
            if (localStorage.getItem(this.storageKeys.playing) === 'true' && this.audio.paused) {
                this.playAudio();
            }
            document.removeEventListener('click', startOnInteraction);
        };
        document.addEventListener('click', startOnInteraction);
    },

    toggleAudio() {
        if (this.audio.paused) {
            this.audio.play();
            localStorage.setItem(this.storageKeys.playing, 'true');
            document.getElementById('audio-control')?.classList.remove('paused');
        } else {
            this.audio.pause();
            localStorage.setItem(this.storageKeys.playing, 'false');
            document.getElementById('audio-control')?.classList.add('paused');
        }
    },

    showControl() {
        document.getElementById('audio-control')?.classList.add('visible');
    },

    saveTime() {
        if (this.audio) {
            localStorage.setItem(this.storageKeys.time, this.audio.currentTime);
        }
    }
};

// Initialize on load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => AudioManager.init());
} else {
    AudioManager.init();
}
