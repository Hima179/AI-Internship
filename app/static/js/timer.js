class AssessmentTimer {
    constructor(totalSeconds, svgRingId, countdownId, onComplete) {
        this.duration = totalSeconds;
        this.remaining = totalSeconds;
        this.ring = document.getElementById(svgRingId);
        this.display = document.getElementById(countdownId);
        this.onComplete = onComplete;
        this.interval = null;
        
        // Circumference for r=26
        this.circumference = 2 * Math.PI * 26;
        if (this.ring) {
            this.ring.style.strokeDasharray = `${this.circumference} ${this.circumference}`;
        }
    }

    start() {
        this.update();
        this.interval = setInterval(() => {
            this.remaining--;
            this.update();
            
            if (this.remaining <= 0) {
                this.stop();
                if (this.onComplete) this.onComplete();
            }
        }, 1000);
    }

    stop() {
        if (this.interval) {
            clearInterval(this.interval);
            this.interval = null;
        }
    }

    reset(newSeconds) {
        this.stop();
        this.duration = newSeconds || this.duration;
        this.remaining = this.duration;
        this.update();
        this.start();
    }

    update() {
        if (this.display) this.display.innerText = this.remaining;
        
        if (this.ring) {
            const offset = this.circumference - (this.remaining / this.duration) * this.circumference;
            this.ring.style.strokeDashoffset = offset;
            
            // Color logic
            this.ring.classList.remove('warning', 'danger');
            if (this.remaining <= 3) {
                this.ring.classList.add('danger');
            } else if (this.remaining <= 6) {
                this.ring.classList.add('warning');
            }
        }
    }
}
