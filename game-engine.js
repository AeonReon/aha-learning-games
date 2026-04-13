/**
 * Learning Games Engine v1.0
 * Shared components for educational games targeting ages 3-5
 * Inspired by: Endless Numbers, Khan Academy Kids, Starfall, Duolingo ABC, Sago Mini
 */

/* ═══════════════════════════════════════════
   CSS INJECTION — Common styles for all games
   ═══════════════════════════════════════════ */
(function injectCSS() {
  const style = document.createElement('style');
  style.textContent = `
    :root {
      --font-game: 'Comic Sans MS', 'Chalkboard SE', 'Marker Felt', 'Segoe Print', cursive;
      --tap-min: 80px;
      --radius-btn: 20px;
      --radius-card: 16px;
      --z-bg: 0;
      --z-game: 10;
      --z-ui: 20;
      --z-overlay: 50;
      --z-celebration: 100;
      --z-loading: 200;
      --transition-press: transform 0.1s ease;
      --shadow-soft: 0 4px 15px rgba(0,0,0,0.2);
      --shadow-glow: 0 0 20px rgba(255,255,255,0.3);
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      font-family: var(--font-game);
      overflow: hidden;
      height: 100vh; height: 100dvh;
      width: 100vw;
      touch-action: manipulation;
      -webkit-user-select: none;
      user-select: none;
      -webkit-tap-highlight-color: transparent;
    }

    /* ── Tappable element base ── */
    .tappable {
      min-width: var(--tap-min);
      min-height: var(--tap-min);
      cursor: pointer;
      transition: var(--transition-press);
      -webkit-tap-highlight-color: transparent;
    }
    .tappable:active { transform: scale(0.93); }

    /* ── Screen system ── */
    .game-screen {
      position: fixed;
      inset: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      transition: opacity 0.5s ease, visibility 0.5s ease;
      opacity: 0;
      visibility: hidden;
      pointer-events: none;
    }
    .game-screen.active {
      opacity: 1;
      visibility: visible;
      pointer-events: auto;
    }

    /* ── Loading screen ── */
    .screen-loading {
      z-index: var(--z-loading);
    }
    .loading-spinner {
      width: 60px; height: 60px;
      border: 6px solid rgba(255,255,255,0.2);
      border-top-color: #fff;
      border-radius: 50%;
      animation: ge-spin 0.8s linear infinite;
      margin: 20px auto;
    }
    .loading-title {
      font-size: clamp(28px, 7vw, 48px);
      color: #fff;
      text-shadow: 3px 3px 0 rgba(0,0,0,0.3);
      margin-bottom: 5px;
    }
    .loading-icon {
      font-size: clamp(80px, 20vw, 140px);
      margin-bottom: 15px;
      animation: ge-bounce 1.5s ease-in-out infinite;
    }

    /* ── Instructions screen ── */
    .screen-instructions {
      z-index: calc(var(--z-loading) - 1);
    }
    .instructions-demo {
      font-size: clamp(60px, 15vw, 100px);
      margin: 15px 0;
      animation: ge-bounce 2s ease-in-out infinite;
    }
    .instructions-text {
      font-size: clamp(16px, 4vw, 24px);
      color: rgba(255,255,255,0.9);
      max-width: 450px;
      padding: 0 25px;
      line-height: 1.5;
      margin-bottom: 20px;
    }

    /* ── Common button ── */
    .game-btn {
      min-width: var(--tap-min);
      min-height: calc(var(--tap-min) * 0.7);
      padding: 16px 45px;
      font-size: clamp(20px, 5vw, 30px);
      font-family: var(--font-game);
      color: #fff;
      border: none;
      border-radius: 35px;
      cursor: pointer;
      font-weight: bold;
      box-shadow: var(--shadow-soft);
      transition: var(--transition-press);
      -webkit-tap-highlight-color: transparent;
    }
    .game-btn:active { transform: scale(0.93); }

    /* ── Progress bar ── */
    .ge-progress-bar {
      position: fixed;
      bottom: 0; left: 0; right: 0;
      z-index: var(--z-ui);
      display: flex;
      justify-content: center;
      align-items: center;
      gap: clamp(3px, 1vw, 8px);
      padding: 10px 10px 12px;
      background: rgba(0,0,0,0.45);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
    }
    .ge-progress-item {
      width: clamp(32px, 7vw, 48px);
      height: clamp(32px, 7vw, 48px);
      border-radius: 50%;
      background: rgba(255,255,255,0.12);
      border: 2.5px solid rgba(255,255,255,0.25);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: clamp(11px, 2.5vw, 16px);
      font-weight: 900;
      color: rgba(255,255,255,0.35);
      font-family: var(--font-game);
      transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .ge-progress-item.complete {
      border-color: #fff;
      color: #fff;
      transform: scale(1.1);
    }

    /* ── Celebration screen ── */
    .screen-celebration {
      z-index: var(--z-celebration);
      background: rgba(0,0,0,0.75);
      backdrop-filter: blur(6px);
      -webkit-backdrop-filter: blur(6px);
    }
    .celebration-icon {
      font-size: clamp(80px, 20vw, 140px);
      animation: ge-dance 1s ease-in-out infinite;
    }
    .celebration-title {
      font-size: clamp(28px, 7vw, 50px);
      color: #ffe066;
      text-shadow: 3px 3px 0 rgba(0,0,0,0.4);
      margin: 10px 0;
      animation: ge-bounce 1.5s ease-in-out infinite;
    }
    .celebration-subtitle {
      font-size: clamp(16px, 4vw, 24px);
      color: rgba(255,255,255,0.9);
      margin: 5px 0 15px;
    }
    .celebration-stars {
      font-size: clamp(30px, 6vw, 50px);
      margin: 10px 0;
      letter-spacing: 5px;
    }

    /* ── Confetti ── */
    .ge-confetti {
      position: fixed;
      z-index: calc(var(--z-celebration) + 5);
      pointer-events: none;
      font-size: 22px;
      animation: ge-confetti-fall linear forwards;
    }

    /* ── Hint wiggle ── */
    .ge-hint-wiggle {
      animation: ge-wiggle 0.5s ease-in-out 3 !important;
    }
    .ge-hint-glow {
      box-shadow: 0 0 25px rgba(255,255,100,0.8), 0 0 50px rgba(255,255,100,0.4) !important;
    }

    /* ── Speech bubble ── */
    .ge-speech {
      position: absolute;
      background: rgba(255,255,255,0.95);
      padding: 10px 20px;
      border-radius: 22px;
      font-size: clamp(14px, 3vw, 20px);
      font-weight: bold;
      white-space: nowrap;
      box-shadow: 0 3px 15px rgba(0,0,0,0.15);
      opacity: 0;
      transition: opacity 0.25s ease;
      pointer-events: none;
      z-index: var(--z-ui);
      max-width: 90vw;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .ge-speech.visible { opacity: 1; }
    .ge-speech::after {
      content: '';
      position: absolute;
      bottom: -9px;
      left: 50%;
      transform: translateX(-50%);
      border-left: 9px solid transparent;
      border-right: 9px solid transparent;
      border-top: 10px solid rgba(255,255,255,0.95);
    }

    /* ── Star burst effect ── */
    .ge-star-burst {
      position: fixed;
      pointer-events: none;
      z-index: calc(var(--z-celebration) + 2);
      font-size: 28px;
      animation: ge-star-pop 0.7s ease-out forwards;
    }

    /* ── Keyframes ── */
    @keyframes ge-spin {
      to { transform: rotate(360deg); }
    }
    @keyframes ge-bounce {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-10px); }
    }
    @keyframes ge-dance {
      0%, 100% { transform: translateY(0) rotate(0deg) scale(1); }
      15% { transform: translateY(-18px) rotate(-8deg) scale(1.08); }
      30% { transform: translateY(0) rotate(8deg) scale(1); }
      45% { transform: translateY(-12px) rotate(-5deg) scale(1.05); }
      60% { transform: translateY(0) rotate(5deg) scale(1); }
      75% { transform: translateY(-8px) rotate(-3deg) scale(1.08); }
    }
    @keyframes ge-wiggle {
      0%, 100% { transform: rotate(0deg); }
      25% { transform: rotate(-6deg) scale(1.05); }
      75% { transform: rotate(6deg) scale(1.05); }
    }
    @keyframes ge-confetti-fall {
      0% { transform: translateY(-20px) rotate(0deg) scale(1); opacity: 1; }
      100% { transform: translateY(105vh) rotate(720deg) scale(0.5); opacity: 0.4; }
    }
    @keyframes ge-star-pop {
      0% { transform: scale(0) rotate(0deg); opacity: 1; }
      60% { transform: scale(1.4) rotate(200deg); opacity: 1; }
      100% { transform: scale(0) rotate(360deg); opacity: 0; }
    }
    @keyframes ge-pulse-glow {
      0%, 100% { filter: brightness(1); }
      50% { filter: brightness(1.25); }
    }
    @keyframes ge-float-in {
      0% { transform: translateY(25px) scale(0.9); opacity: 0; }
      100% { transform: translateY(0) scale(1); opacity: 1; }
    }
    @keyframes ge-number-appear {
      0% { transform: scale(0) rotate(-20deg); opacity: 0; }
      60% { transform: scale(1.2) rotate(5deg); opacity: 1; }
      100% { transform: scale(1) rotate(0deg); opacity: 1; }
    }
    @keyframes ge-chomp {
      0% { transform: scale(1) rotate(0deg); }
      20% { transform: scale(1.35) rotate(-6deg); }
      40% { transform: scale(1.4) rotate(6deg); }
      60% { transform: scale(1.3) rotate(-3deg); }
      100% { transform: scale(1) rotate(0deg); }
    }
    @keyframes ge-shake {
      0%, 100% { transform: translateX(0); }
      20% { transform: translateX(-12px) rotate(-4deg); }
      40% { transform: translateX(12px) rotate(4deg); }
      60% { transform: translateX(-8px) rotate(-2deg); }
      80% { transform: translateX(8px) rotate(2deg); }
    }
    @keyframes ge-idle-blink {
      0%, 96%, 100% { transform: scaleY(1); }
      98% { transform: scaleY(0.1); }
    }
  `;
  document.head.appendChild(style);
})();


/* ═══════════════════════════════════════════
   AUDIO MANAGER — Three-layer sound system
   ═══════════════════════════════════════════ */
class AudioManager {
  constructor() {
    this.ctx = null;
    this.musicGain = null;
    this.sfxGain = null;
    this.masterGain = null;
    this.musicVolume = 0.12;
    this.sfxVolume = 0.35;
    this.musicDuckedVolume = 0.04;
    this.isMusicPlaying = false;
    this.musicOscillators = [];
    this.voiceQueue = [];
    this.isSpeaking = false;
    this.sfxPlaying = false;
    this.voices = [];
    this.preferredVoice = null;
    this._initVoices();
  }

  _initAudio() {
    if (this.ctx) return;
    this.ctx = new (window.AudioContext || window.webkitAudioContext)();
    this.masterGain = this.ctx.createGain();
    this.masterGain.gain.value = 1;
    this.masterGain.connect(this.ctx.destination);
    this.musicGain = this.ctx.createGain();
    this.musicGain.gain.value = this.musicVolume;
    this.musicGain.connect(this.masterGain);
    this.sfxGain = this.ctx.createGain();
    this.sfxGain.gain.value = this.sfxVolume;
    this.sfxGain.connect(this.masterGain);
  }

  _initVoices() {
    const load = () => {
      this.voices = speechSynthesis.getVoices();
      if (!this.voices.length) return;
      const prefs = ['samantha','karen','victoria','fiona','moira','tessa','kate','google uk english female','microsoft zira'];
      for (const p of prefs) {
        const v = this.voices.find(v => v.name.toLowerCase().includes(p));
        if (v) { this.preferredVoice = v; return; }
      }
      const female = this.voices.find(v => /female/i.test(v.name));
      this.preferredVoice = female || this.voices[0] || null;
    };
    speechSynthesis.onvoiceschanged = load;
    load();
  }

  /** Ensure AudioContext is active — call on first user tap */
  unlock() {
    this._initAudio();
    if (this.ctx.state === 'suspended') this.ctx.resume();
  }

  /* ── MUSIC ── */
  /** Start a gentle pentatonic background loop */
  startMusic(key = 'C', mood = 'happy') {
    this._initAudio();
    if (this.isMusicPlaying) return;
    this.isMusicPlaying = true;

    // Pentatonic scale frequencies
    const scales = {
      'C':  [261.63, 293.66, 329.63, 392.00, 440.00],
      'G':  [196.00, 220.00, 246.94, 293.66, 329.63],
      'F':  [174.61, 196.00, 220.00, 261.63, 293.66],
      'D':  [146.83, 164.81, 196.00, 220.00, 261.63],
    };
    const notes = scales[key] || scales['C'];

    const playNote = () => {
      if (!this.isMusicPlaying) return;
      const freq = notes[Math.floor(Math.random() * notes.length)];
      const osc = this.ctx.createOscillator();
      const noteGain = this.ctx.createGain();

      osc.type = 'sine';
      osc.frequency.value = freq;
      noteGain.gain.setValueAtTime(0, this.ctx.currentTime);
      noteGain.gain.linearRampToValueAtTime(0.3, this.ctx.currentTime + 0.15);
      noteGain.gain.linearRampToValueAtTime(0, this.ctx.currentTime + 1.8);

      osc.connect(noteGain);
      noteGain.connect(this.musicGain);
      osc.start(this.ctx.currentTime);
      osc.stop(this.ctx.currentTime + 2);
      osc.onended = () => { osc.disconnect(); noteGain.disconnect(); };

      const next = 800 + Math.random() * 1400;
      this._musicTimer = setTimeout(playNote, next);
    };
    playNote();
  }

  stopMusic() {
    this.isMusicPlaying = false;
    if (this._musicTimer) clearTimeout(this._musicTimer);
  }

  _duckMusic() {
    if (!this.musicGain) return;
    this.musicGain.gain.linearRampToValueAtTime(this.musicDuckedVolume, this.ctx.currentTime + 0.15);
  }

  _unduckMusic() {
    if (!this.musicGain) return;
    this.musicGain.gain.linearRampToValueAtTime(this.musicVolume, this.ctx.currentTime + 0.3);
  }

  /* ── SFX ── */
  /** Play a short sound effect */
  playTone(type) {
    this._initAudio();
    const t = this.ctx.currentTime;

    const playOsc = (freq, startTime, duration, oscType = 'sine', vol = 0.5) => {
      const osc = this.ctx.createOscillator();
      const g = this.ctx.createGain();
      osc.type = oscType;
      osc.frequency.value = freq;
      g.gain.setValueAtTime(0, startTime);
      g.gain.linearRampToValueAtTime(vol, startTime + 0.02);
      g.gain.linearRampToValueAtTime(0, startTime + duration);
      osc.connect(g);
      g.connect(this.sfxGain);
      osc.start(startTime);
      osc.stop(startTime + duration + 0.01);
      osc.onended = () => { osc.disconnect(); g.disconnect(); };
    };

    switch(type) {
      case 'correct':
        // Rising two-note chime: C5 → E5
        playOsc(523.25, t, 0.18, 'sine', 0.5);
        playOsc(659.25, t + 0.15, 0.25, 'sine', 0.6);
        break;

      case 'wrong':
        // Gentle descending wobble — soft and friendly
        playOsc(350, t, 0.12, 'sine', 0.25);
        playOsc(300, t + 0.1, 0.12, 'sine', 0.2);
        playOsc(280, t + 0.2, 0.2, 'sine', 0.15);
        break;

      case 'celebration':
        // Ascending 5-note fanfare: C-E-G-E-C(high)
        playOsc(523.25, t, 0.15, 'sine', 0.4);
        playOsc(659.25, t + 0.13, 0.15, 'sine', 0.45);
        playOsc(783.99, t + 0.26, 0.18, 'sine', 0.5);
        playOsc(659.25, t + 0.42, 0.15, 'sine', 0.45);
        playOsc(1046.50, t + 0.55, 0.35, 'sine', 0.55);
        break;

      case 'appear':
        // Gentle pop sound
        playOsc(600, t, 0.08, 'sine', 0.2);
        playOsc(900, t + 0.04, 0.1, 'sine', 0.15);
        break;

      case 'tap':
        // Soft click
        playOsc(800, t, 0.04, 'sine', 0.15);
        break;

      case 'hint':
        // Gentle attention chime
        playOsc(440, t, 0.15, 'sine', 0.15);
        playOsc(550, t + 0.15, 0.2, 'sine', 0.12);
        break;

      case 'whoosh':
        // Quick whoosh for transitions
        const osc = this.ctx.createOscillator();
        const g = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(200, t);
        osc.frequency.exponentialRampToValueAtTime(800, t + 0.15);
        g.gain.setValueAtTime(0.15, t);
        g.gain.linearRampToValueAtTime(0, t + 0.2);
        osc.connect(g); g.connect(this.sfxGain);
        osc.start(t); osc.stop(t + 0.25);
        osc.onended = () => { osc.disconnect(); g.disconnect(); };
        break;
    }
  }

  /* ── VOICE ── */
  /** Speak text with ducking, returns a Promise */
  speak(text, rate = 0.85, pitch = 1.1) {
    return new Promise(resolve => {
      this.voiceQueue.push({ text, rate, pitch, resolve });
      this._processVoiceQueue();
    });
  }

  _processVoiceQueue() {
    if (this.isSpeaking || this.voiceQueue.length === 0) return;
    this.isSpeaking = true;
    const { text, rate, pitch, resolve } = this.voiceQueue.shift();

    speechSynthesis.cancel();
    this._duckMusic();

    const u = new SpeechSynthesisUtterance(text);
    if (this.preferredVoice) u.voice = this.preferredVoice;
    u.rate = rate;
    u.pitch = pitch;
    u.volume = 1;

    const done = () => {
      this.isSpeaking = false;
      this._unduckMusic();
      resolve();
      // Small gap between queued utterances
      setTimeout(() => this._processVoiceQueue(), 150);
    };
    u.onend = done;
    u.onerror = done;
    speechSynthesis.speak(u);
  }

  /** Clear the voice queue */
  clearVoiceQueue() {
    this.voiceQueue.forEach(q => q.resolve());
    this.voiceQueue = [];
    speechSynthesis.cancel();
    this.isSpeaking = false;
    this._unduckMusic();
  }
}


/* ═══════════════════════════════════════════
   CONFETTI — CSS particle celebration system
   ═══════════════════════════════════════════ */
class Confetti {
  static pieces = ['🎉','🎊','⭐','🌟','✨','💫','🎈','🎵','💜','💚','❤️','🧡','💛','💙'];

  /** Launch a burst of confetti */
  static burst(count = 45, extraPieces = []) {
    const all = [...Confetti.pieces, ...extraPieces];
    for (let i = 0; i < count; i++) {
      const el = document.createElement('div');
      el.className = 'ge-confetti';
      el.textContent = all[Math.floor(Math.random() * all.length)];
      el.style.left = (Math.random() * 100) + 'vw';
      el.style.top = '-30px';
      el.style.fontSize = (16 + Math.random() * 14) + 'px';
      el.style.animationDelay = (Math.random() * 1.8) + 's';
      el.style.animationDuration = (2.2 + Math.random() * 2.5) + 's';
      document.body.appendChild(el);
      setTimeout(() => el.remove(), 6000);
    }
  }

  /** Multiple waves of confetti */
  static celebrate(waves = 3, interval = 1800, extra = []) {
    for (let w = 0; w < waves; w++) {
      setTimeout(() => Confetti.burst(35, extra), w * interval);
    }
  }
}


/* ═══════════════════════════════════════════
   STAR BURST — sparkle effect on correct tap
   ═══════════════════════════════════════════ */
class StarBurst {
  static at(x, y, count = 7) {
    const chars = ['⭐','🌟','✨','💫','🎉'];
    for (let i = 0; i < count; i++) {
      const el = document.createElement('div');
      el.className = 'ge-star-burst';
      el.textContent = chars[Math.floor(Math.random() * chars.length)];
      el.style.left = (x + (Math.random() - 0.5) * 120) + 'px';
      el.style.top = (y + (Math.random() - 0.5) * 120) + 'px';
      el.style.animationDelay = (Math.random() * 0.2) + 's';
      document.body.appendChild(el);
      setTimeout(() => el.remove(), 900);
    }
  }

  static fromElement(el) {
    const r = el.getBoundingClientRect();
    StarBurst.at(r.left + r.width / 2, r.top + r.height / 2);
  }
}


/* ═══════════════════════════════════════════
   PROGRESS TRACKER — visual progress bar
   ═══════════════════════════════════════════ */
class ProgressTracker {
  /**
   * @param {HTMLElement} container — element to render into
   * @param {Array} items — array of {label, value} objects
   * @param {Object} opts — {completeColor, completeEmoji}
   */
  constructor(container, items, opts = {}) {
    this.container = container;
    this.items = items;
    this.completeColor = opts.completeColor || 'linear-gradient(135deg, #4CAF50, #8BC34A)';
    this.completeEmoji = opts.completeEmoji || null;
    this.completedSet = new Set();
    this.render();
  }

  render() {
    this.container.innerHTML = '';
    this.container.className = 'ge-progress-bar';
    this.itemEls = {};
    this.items.forEach(item => {
      const el = document.createElement('div');
      el.className = 'ge-progress-item';
      el.textContent = item.label;
      this.container.appendChild(el);
      this.itemEls[item.value] = el;
    });
  }

  complete(value) {
    if (this.completedSet.has(value)) return;
    this.completedSet.add(value);
    const el = this.itemEls[value];
    if (!el) return;
    el.classList.add('complete');
    el.style.background = this.completeColor;
    if (this.completeEmoji) el.textContent = this.completeEmoji;
  }

  get count() { return this.completedSet.size; }
  get total() { return this.items.length; }
  get isComplete() { return this.count >= this.total; }

  reset() {
    this.completedSet.clear();
    Object.values(this.itemEls).forEach(el => {
      el.classList.remove('complete');
      el.style.background = '';
    });
  }
}


/* ═══════════════════════════════════════════
   HINT SYSTEM — auto-hint after inactivity
   ═══════════════════════════════════════════ */
class HintSystem {
  /**
   * @param {AudioManager} audio
   * @param {Object} opts — {wiggleDelay, voiceDelay, voiceText, getTargets}
   */
  constructor(audio, opts = {}) {
    this.audio = audio;
    this.wiggleDelay = opts.wiggleDelay || 3000;
    this.voiceDelay = opts.voiceDelay || 6000;
    this.voiceText = opts.voiceText || "Can you find it?";
    this.getTargets = opts.getTargets || (() => []);
    this._wiggleTimer = null;
    this._voiceTimer = null;
    this._active = false;
  }

  /** Reset timers — call after any user interaction */
  reset() {
    this.stop();
    if (!this._active) return;
    this._wiggleTimer = setTimeout(() => this._doWiggle(), this.wiggleDelay);
    this._voiceTimer = setTimeout(() => this._doVoice(), this.voiceDelay);
  }

  start() {
    this._active = true;
    this.reset();
  }

  stop() {
    clearTimeout(this._wiggleTimer);
    clearTimeout(this._voiceTimer);
  }

  pause() {
    this._active = false;
    this.stop();
  }

  /** Update the voice hint text dynamically */
  setVoiceText(text) {
    this.voiceText = text;
  }

  _doWiggle() {
    const targets = this.getTargets();
    targets.forEach(el => {
      el.classList.add('ge-hint-wiggle', 'ge-hint-glow');
      setTimeout(() => el.classList.remove('ge-hint-wiggle', 'ge-hint-glow'), 1800);
    });
    this.audio.playTone('hint');
  }

  _doVoice() {
    if (this.voiceText) {
      this.audio.speak(this.voiceText, 0.85, 1.1);
    }
  }
}


/* ═══════════════════════════════════════════
   CELEBRATION SCREEN — end-of-game overlay
   ═══════════════════════════════════════════ */
class CelebrationScreen {
  /**
   * @param {Object} opts — {title, subtitle, icon, starsCount, bgColor, btnColor, btnText, extraConfetti}
   */
  constructor(opts = {}) {
    this.opts = Object.assign({
      title: '🎉 Amazing! 🎉',
      subtitle: 'You did it!',
      icon: '🌟',
      starsCount: 0,
      bgColor: 'rgba(0,0,0,0.75)',
      btnColor: 'linear-gradient(135deg, #4CAF50, #8BC34A)',
      btnText: 'Play Again! 🔄',
      extraConfetti: [],
    }, opts);

    this._build();
    this.onPlayAgain = null;
  }

  _build() {
    this.el = document.createElement('div');
    this.el.className = 'game-screen screen-celebration';
    this.el.style.background = this.opts.bgColor;

    this.el.innerHTML = `
      <div class="celebration-icon">${this.opts.icon}</div>
      <div class="celebration-title">${this.opts.title}</div>
      <div class="celebration-subtitle">${this.opts.subtitle}</div>
      <div class="celebration-stars"></div>
      <button class="game-btn tappable" style="background:${this.opts.btnColor};margin-top:20px;">${this.opts.btnText}</button>
    `;

    const btn = this.el.querySelector('.game-btn');
    btn.addEventListener('click', () => { if (this.onPlayAgain) this.onPlayAgain(); });

    document.body.appendChild(this.el);
  }

  show(starsCount) {
    const starsEl = this.el.querySelector('.celebration-stars');
    starsEl.textContent = '⭐'.repeat(starsCount || this.opts.starsCount || 5);
    this.el.classList.add('active');
    Confetti.celebrate(3, 1500, this.opts.extraConfetti);
  }

  hide() {
    this.el.classList.remove('active');
  }

  updateText(title, subtitle) {
    if (title) this.el.querySelector('.celebration-title').textContent = title;
    if (subtitle) this.el.querySelector('.celebration-subtitle').textContent = subtitle;
  }
}


/* ═══════════════════════════════════════════
   SCREEN MANAGER — transition between screens
   ═══════════════════════════════════════════ */
class ScreenManager {
  constructor() {
    this.screens = {};
    this.current = null;
  }

  register(name, element) {
    this.screens[name] = element;
    element.classList.remove('active');
  }

  show(name) {
    if (this.current && this.screens[this.current]) {
      this.screens[this.current].classList.remove('active');
    }
    this.current = name;
    if (this.screens[name]) {
      this.screens[name].classList.add('active');
    }
  }

  hide(name) {
    if (this.screens[name]) this.screens[name].classList.remove('active');
    if (this.current === name) this.current = null;
  }

  hideAll() {
    Object.values(this.screens).forEach(el => el.classList.remove('active'));
    this.current = null;
  }
}


/* ═══════════════════════════════════════════
   UTILITY HELPERS
   ═══════════════════════════════════════════ */

/** Promise-based delay */
function delay(ms) { return new Promise(r => setTimeout(r, ms)); }

/** Shuffle array in place */
function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

/** Random item from array */
function randomPick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }

/** Tens name lookup */
const TENS_NAMES = {
  10:'Ten', 20:'Twenty', 30:'Thirty', 40:'Forty', 50:'Fifty',
  60:'Sixty', 70:'Seventy', 80:'Eighty', 90:'Ninety', 100:'One Hundred'
};

/** Encouragement phrases */
const CHEERS = [
  "Amazing!", "Wonderful!", "Brilliant!", "Fantastic!", "You got it!",
  "Super!", "Awesome!", "Well done!", "Great job!", "Incredible!"
];

/** Gentle retry phrases */
const GENTLE_RETRY = [
  "Oops! Let's try again!", "Not quite! Try another one!",
  "Almost! Give it another go!", "Let's try again!",
  "Hmm, not that one! Try again!"
];

/** Make any element properly tappable (click + touch) */
function onTap(el, handler) {
  let tapped = false;
  el.addEventListener('touchstart', (e) => {
    e.preventDefault();
    if (tapped) return;
    tapped = true;
    handler(e);
    setTimeout(() => tapped = false, 300);
  }, { passive: false });
  el.addEventListener('click', (e) => {
    if (tapped) return;
    handler(e);
  });
}

// Export for games
window.GameEngine = {
  AudioManager,
  Confetti,
  StarBurst,
  ProgressTracker,
  HintSystem,
  CelebrationScreen,
  ScreenManager,
  delay,
  shuffle,
  randomPick,
  onTap,
  TENS_NAMES,
  CHEERS,
  GENTLE_RETRY,
};
