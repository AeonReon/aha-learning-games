# HANDOFF — Building games that don't suck

**Read this before writing a single line of code. Seriously.**

This document exists because every new session I (Claude) have regresses on hard-won lessons. The games that ship well versus the ones that crash have nothing to do with talent — it's about following specific rules that aren't obvious until you've broken them. This is the brief I wish I'd had on day one.

---

## 1. Orient yourself first (5 minutes)

```
learning-games/
├── index.html                  ← Main hub (category browser)
├── audio/
│   ├── letters/                ← a.mp3..z.mp3 (letter names) + a_sound.mp3..z_sound.mp3 (phonics)
│   ├── numbers/                ← 0.mp3..100.mp3
│   ├── voice-a/                ← en-US-AnaNeural (numbers games — cute, energetic)
│   │   └── {greetings,correct,wrong,thinking,round-complete,game-complete}/*.mp3
│   ├── voice-b/                ← en-GB-SoniaNeural (letters games — warm British)
│   │   └── {greetings,correct,wrong,thinking,round-complete,game-complete}/*.mp3
│   ├── fun-zone/               ← Character voice packs (dragon, trex, monster, etc)
│   ├── phrases/                ← Legacy flat phrase clips
│   └── phrases.json            ← Manifest of voice-a/voice-b clips
├── ARCHITECTURE.md             ← Reference doc — READ THIS TOO
├── QUALITY_STANDARDS.md        ← Pre-ship checklist
├── HANDOFF.md                  ← You're reading it
├── GAME_TEMPLATE.html          ← Working skeleton with all patterns
└── v2/
    ├── 0-5/                    ← Princess & Friends (numbers 0-5)
    ├── 6-10/                   ← Spooky Halloween (numbers 6-10) ← GOLD STANDARD
    ├── 11-15/                  ← Ocean Adventure
    ├── 16-20/                  ← Space Explorer
    ├── 10-50/                  ← Jungle Safari
    ├── 60-100/                 ← Dragon Lair
    ├── a-e/                    ← Castle Kingdom (letters A-E)
    ├── f-j/                    ← Fairy Forest
    ├── k-o/                    ← Magic Mountain
    ├── p-t/                    ← Pirate Cove
    ├── u-z/                    ← Unicorn Rainbow
    ├── number-carnival/        ← Bonus multi-mini-game
    ├── alphabet-arcade/        ← Bonus multi-mini-game
    └── fun-zone/               ← 5 pure-fun games (Tickle T-Rex, Feed Dragon, etc)
```

**Each theme folder contains exactly 5 files:** `card-match.html`, `pairs.html`, `bubble-pop.html`, `sequence.html`, `tracing.html` — plus an `index.html` sub-hub.

**Audio path rule:** From any game file, audio is at `../../audio/`. This is NON-NEGOTIABLE. Breaking it silently kills all sound. Don't change it.

**Deployment:** Single repo, pushed to `AeonReon/aha-learning-games` on GitHub, auto-deploys to `https://learning-games-one.vercel.app/`. No build step — pure vanilla HTML/CSS/JS.

---

## 2. The Golden Rules (from user feedback — non-negotiable)

These came from watching real 3-5 year olds play. Violate them and the game feels broken.

### RULE 1: The numeral is ALWAYS visible and is the HERO
Every card, every target, every option that shows a number **must show the digit prominently**. Not "small digit with big emoji" — the **digit fills the card**, everything else is decoration.

**VIOLATIONS I made that were caught and had to be fixed:**
- Pairs game showing "sixty" word as big text with tiny "60" — WRONG
- Card showing 🐘🌿🌿 with small "20" underneath — WRONG  
- Emoji pattern as the target card with no numeral visible — WRONG

**CORRECT:** `<div class="card-numeral">60</div>` at `clamp(54px, 14vw, 86px)`, with tiny corner emoji decoration at `opacity: 0.4`, max 18px.

### RULE 2: Speak the number/letter ONCE per interaction
Never double-speak. I made this mistake early — `await speakNumber(n); await delay(140); await speakNumber(n);` — user called it out as "frustratingly slow."

**CORRECT pattern:**
```javascript
audio.play('correct');       // random cheer (no repeat)
await delay(280);
audio.speakNumber(currentTarget);   // once
await delay(120);
// that's it — don't repeat
```

### RULE 3: Never block with `await` on voice clips during gameplay
This is the #1 cause of "the game feels glitchy" and "it froze."

**iOS Safari WebAudio has a known issue where `src.onended` sometimes never fires.** If you `await audio.play(...)`, the entire game state machine freezes. The more audio nodes active (e.g. monster with many features, dragon full), the higher the chance.

**ANTI-PATTERNS that cause freezes:**
```javascript
// NEVER DO THIS in a gameplay path:
await audio.play('correct');
await audio.speakNumber(n);
await audio.dragonSay('yummy');

// NEVER DO THIS either — Promise.resolve adopts inner promise state!
await Promise.race([
  Promise.resolve(audio.play('x')),    // BROKEN — still awaits the hung promise
  new Promise(r => setTimeout(r, 700))
]);
```

**CORRECT patterns:**
```javascript
// Fire and forget
audio.play('correct');
audio.speakNumber(n);

// If you really need a delay after triggering audio, use setTimeout:
audio.speakNumber(n);
setTimeout(() => advanceGame(), 400);

// If you NEED a proper timeout race, actually wrap it:
await Promise.race([
  new Promise(resolve => { audio.play('x').then(resolve, resolve); }),
  new Promise(resolve => setTimeout(resolve, 700))
]);
```

**Best of all: don't await anything. Use fire-and-forget + `setTimeout` for timing.**

### RULE 4: Snappy pacing — never block the child from advancing
User feedback: *"It's very stuck where you press one button and then you have to wait while nothing happens in between."*

- Post-correct delay: **max 450ms** before child can tap the next thing
- Round transitions: **~3 seconds total** — NOT 8 seconds (which is what happens if you await voice clips)
- Wrong answer: child can retry **immediately** — do not lock the board for a punishment beat
- Voice clips for `round-complete` / `greetings` on round banners: show banner THEN fire voice NON-BLOCKING

**Pattern for round transitions:**
```javascript
// BAD — waits for voice clip (which is 2-3 seconds)
$('roundBanner').classList.add('show');
await audio.play('round-complete');    // blocks 2-3s
await delay(1500);
$('roundBanner').classList.remove('show');

// GOOD — banner visible immediately, voice plays in background
$('roundBanner').classList.add('show');
audio.play('round-complete');          // fire-and-forget
await delay(1400);                      // total 1.4s, voice catches up
$('roundBanner').classList.remove('show');
await delay(180);
```

### RULE 5: Bouncy spring easing everywhere
User praised Tickle-T-Rex as "fun, the way it bounces." That feel comes from ONE thing:

```css
cubic-bezier(0.34, 1.56, 0.64, 1)
```

Use it on every transform, scale, flight animation. Not `ease-out`, not `ease-in-out` — this specific spring curve. It's why correct-answer feedback feels SATISFYING.

```css
.num-node {
  transition: transform 0.15s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.card-flying {
  animation: flyToTarget 350ms cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

### RULE 6: No floating UI over the play area
User feedback: *"In the card match when you are in there where it shows the number you're supposed to select it's hidden by a strange box."*

**What happened:** I put an "Animal Sanctuary" achievement visual in the top-right that covered the target card on small screens.

**RULE:** Achievement visuals go in the HUD as a small counter ("🦴 3/20") OR appear ONLY on the celebration screen. Never a floating sidebar, never in a corner during gameplay.

### RULE 7: Soft tone — never "wrong"
User feedback: *"When I got it wrong, it said 'no that is wrong,' instead of something just like try again."*

- No "wrong" or "no" in voice clips or text
- No crying faces (😿) or sad emoji reactions
- Wrong answer = gentle shake + voice like "Try again!" or "Almost!" + encouraging character face
- The character stays supportive, never judgmental

### RULE 8: iPhone notch — use safe-area-inset
User feedback: *"You can't see the number or letter at the top. It's in behind the notch."*

**Every top-fixed element MUST use:**
```css
.hud, .back-btn, .target-display {
  top: max(12px, env(safe-area-inset-top, 12px) + 8px);
}
```

Also add to viewport meta:
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no, viewport-fit=cover">
```

### RULE 9: Always-reachable back button (and have TWO)
User reported being stuck inside games multiple times.

**Minimum required in every game:**
```html
<!-- Primary — top-left, OUTSIDE all screen containers -->
<a href="../../" class="back-home-btn">← Home</a>

<!-- Failsafe — floating home bubble during gameplay -->
<a href="../../" id="homeBubble" class="home-bubble">🏠</a>
```

**Critical CSS:**
```css
.back-home-btn, .home-bubble {
  position: fixed;
  z-index: 9999;  /* above EVERYTHING else */
}
```

These are plain `<a>` tags. They work even if **all JavaScript crashes**. That's the point.

### RULE 10: Screens controlled by `.active` class — and ONLY by `.active`
A bug I made that broke Cat Café: I had `#scrTitle { display: flex; }` as a base style AND `.screen.active { display: flex; }`. **ID selector specificity beats class specificity** — so the title screen never hid. Every tap re-triggered the start handler. The game just meowed infinitely.

**CORRECT pattern:**
```css
.screen {
  position: fixed; inset: 0;
  display: none;       /* base: hidden */
  flex-direction: column;
  z-index: 200;
}
.screen.active { display: flex; }   /* only way to show */

/* DO NOT add #scrTitle { display: flex; } anywhere */
/* DO NOT add #scrCeleb { display: block; } anywhere */
```

---

## 3. Gold Standard Reference Files

When building a new game, **read the equivalent 6-10 game first**. These are the gold standard:

| Game type | Read this first |
|-----------|----------------|
| Card Match | `v2/6-10/card-match.html` |
| Pairs | `v2/6-10/pairs.html` |
| Bubble Pop | `v2/6-10/bubble-pop.html` |
| Sequence | `v2/6-10/sequence.html` |
| Tracing | `v2/6-10/tracing.html` |
| Fun/bouncy feel | `v2/fun-zone/tickle-trex.html` |
| Recap/mini-game pack | `v2/number-carnival/index.html` |

The 6-10 folder is the standard because it was rebuilt AFTER the first round of user feedback. Its patterns are battle-tested. The 0-5 folder is older and may have stale patterns — don't use as reference.

---

## 4. What actually makes these games good

### The animation feel
- **Every tap over-reacts.** Tapping a correct answer triggers: starBurst (8 emoji sparkles radiating outward), a scale-bounce on the tapped element (`transform: scale(0.93)` on `:active`, spring back), a voice cheer, a character jump, a progress dot filling with a scale-up bloom.
- **Idle motion keeps the world alive.** Background particles drift. Characters bob gently. The start button glows/brightens. Nothing is static.
- **Character reactions are instant.** Character's speech bubble appears within 50ms of a tap. The character jumps/dances immediately. Don't queue these behind voice clips.

### How audio integrates
The sequence for a correct answer:
1. `audio.tone('correct')` — instant 3-note chime (C-E-G) from Web Audio oscillators, ZERO latency
2. `starBurst(element)` — visual burst at tap location
3. `jumpChar()` — character hop
4. `showCharBubble(pick(BUBBLE_CORRECT))` — text bubble
5. `audio.speakNumber(n)` — fire-and-forget, number voice
6. `audio.play('correct')` — fire-and-forget, random cheer phrase from pool
7. `markProg(index)` — progress dot fills with bloom animation
8. Wait `~450ms` then move to next question

**Why this order:** The tone + starBurst + character reaction all fire INSTANTLY (synthesized tones have no load time). The longer voice clips come after but don't block gameplay.

### The 4-round progression
**The round count is EXACTLY 4.** Not 3, not 5. HUD shows "1/4" — kids need a clear endpoint.

Difficulty escalates through **scaffolding removal**, not raw speed:
- Round 1: All scaffolds on. Target shows numeral + word + dots. Strong hint pulse on next correct answer.
- Round 2: Word removed from target. No hint pulse.
- Round 3: Numeral removed from target — only dots/emoji pattern shown (but option cards still show numeral + word).
- Round 4: Mixed representations — some cards show numeral only, some words, some emoji. Requires cross-representation understanding.

**What this actually looks like per game:**

#### Card Match
- R1: 2 choices. Target + cards show numeral + emoji + word.
- R2: 3 choices. Target shows numeral + emoji. Cards show numeral + word.
- R3: 4 choices. Target shows emoji pattern (+ small numeral still visible). Cards show numeral + word.
- R4: 4 choices. Target shows word (+ small numeral). Cards show numeral only.

#### Pairs
- R1: 3 pairs (6 cards). 1.5s peek at start. Cross-rep: numeral ↔ dot-pattern.
- R2: 4 pairs. No peek. Same cross-rep.
- R3: 5 pairs. Numeral ↔ word cross-rep. (Or keep numeral-only with different decoration — per user preference, avoid "tiny numeral / big decoration".)
- R4: 6 pairs. Mixed representations.

#### Bubble Pop (rising mechanic)
- R1: Big numeral + small word on bubbles. Slow rise (~15s to cross). Target big in HUD.
- R2: Numeral only. Faster (~12s).
- R3: Dot pattern + small numeral always visible. Slower (~15s).
- R4: Mixed representations. Fast (~10s).

#### Sequence (drop-into-container)
- R1: 5 bottles scattered, next-to-tap pulses as hint.
- R2: Same, no hint pulse.
- R3: Bottles show dots/emoji pattern + small numeral always visible.
- R4: Smaller bottles, gentle background color shift timer (no failure).

#### Tracing (canvas)
- L1: Full-opacity outline + animated sparkle guide traces the path first (2s).
- L2: Full-opacity outline, no guide.
- L3: 50% opacity outline.
- L4: 15% opacity outline (nearly from memory).

### What the narrative does
It's not decoration — it's what makes kids care.

- **Luna the witch** (spooky theme) doesn't just exist — she reacts: jumps when you match a card, says "Splendid, absolutely splendid!" via Voice B. Her book (spell book in card-match) visibly gains pages. At game complete, Luna dances.
- **Every game has a narrative payoff:** Card Match seals spell cards into a book. Pairs rebuilds a haunted house. Sequence brews a potion that hatches into a baby dragon. This isn't "gets more points" — it's a VISIBLE story arc.
- **The achievement must be visible on the celebration screen** — not during gameplay. A "spell book filling up" would be a floating UI distraction. But showing the full book with all 20 matched pages on the celebration screen = magical payoff.

---

## 5. Audio system — complete picture

### GameAudio class
Every game copies the same class. Do NOT simplify it — every feature is needed:

```javascript
class GameAudio {
  constructor() {
    this.ctx = null;
    this.musicGain = null;
    this.sfxGain = null;
    this.musicVol = 0.08;        // DO NOT DROP BELOW 0.05 — becomes inaudible
    this.sfxVol = 0.3;
    this.musicDucked = 0.025;    // while voice plays
    this.playing = false;
    this.voiceQueue = [];
    this.speaking = false;
    this._lastPlayed = {};
  }

  _init() {
    if (this.ctx) return;
    this.ctx = new (window.AudioContext || window.webkitAudioContext)();
    const master = this.ctx.createGain();
    master.gain.value = 1;
    master.connect(this.ctx.destination);
    this.musicGain = this.ctx.createGain();
    this.musicGain.gain.value = this.musicVol;
    this.musicGain.connect(master);
    this.sfxGain = this.ctx.createGain();
    this.sfxGain.gain.value = this.sfxVol;
    this.sfxGain.connect(master);
  }

  unlock() {
    // DO NOT make this async — see RULE 3
    this._init();
    if (this.ctx.state === 'suspended') this.ctx.resume().catch(() => {});
  }

  // ... startMusic(), stopMusic(), _duck(), _unduck(), tone(), speak()
  // See GAME_TEMPLATE.html for complete implementation

  _playFile(path) {
    // iOS FIX — route through AudioContext, not new Audio()
    const htmlFallback = () => new Promise(resolve => {
      const a = new window.Audio(path);
      a.onended = resolve;
      a.onerror = () => resolve();
      a.play().catch(() => resolve());
    });
    if (this.ctx && this.ctx.state !== 'closed') {
      return fetch(path)
        .then(r => { if (!r.ok) throw 0; return r.arrayBuffer(); })
        .then(buf => this.ctx.decodeAudioData(buf))
        .then(decoded => new Promise(resolve => {
          const src = this.ctx.createBufferSource();
          src.buffer = decoded;
          src.connect(this.ctx.destination);
          src.onended = resolve;
          src.start();
        }))
        .catch(() => htmlFallback());
    }
    return htmlFallback();
  }

  speakNumber(n) { return this.speak(`${AUDIO_BASE}/numbers/${n}.mp3`); }
  speakLetter(l) { return this.speak(`${AUDIO_BASE}/letters/${l}.mp3`); }
  speakPhrase(name) { return this.speak(`${AUDIO_BASE}/phrases/${name}.mp3`); }

  clearQueue() {
    this.voiceQueue.forEach(q => q.resolve());
    this.voiceQueue = [];
  }

  // CRITICAL for games with changing targets — flush old announcements
  // before announcing a new one, so voice doesn't lag behind gameplay
}
```

### Voice A vs Voice B
| Voice | Edge TTS ID | Character | Use for |
|-------|-------------|-----------|---------|
| Voice A | `en-US-AnaNeural` | Cute, energetic, American | **Numbers games** |
| Voice B | `en-GB-SoniaNeural` | Warm, nurturing, British teacher | **Letters games** |

This convention is FIXED. Don't mix them. Fun Zone games can use custom character voices (dragon, t-rex, etc) per game theme.

### The phrase pools pattern
Every game inlines its own pool object:
```javascript
const VOICE_A = {
  greetings: [
    'voice-a/greetings/here-we-go.mp3',
    'voice-a/greetings/lets-go.mp3',
    // ... 5-7 variations
  ],
  correct: [/* 13 variations */],
  wrong: [/* 6 variations */],
  thinking: [/* 5 variations */],
  'round-complete': [/* 4 variations */],
  'game-complete': [/* 5 variations */],
};
```

Add a `play(category)` method to GameAudio that picks a random clip, never repeating the same one twice in a row:
```javascript
play(category) {
  const pool = VOICE_A[category];
  if (!pool || !pool.length) return Promise.resolve();
  const last = this._lastPlayed[category];
  const candidates = pool.length > 1 ? pool.filter(f => f !== last) : pool;
  const file = candidates[Math.floor(Math.random() * candidates.length)];
  this._lastPlayed[category] = file;
  return this.speak(`${AUDIO_BASE}/${file}`);
}
```

### audio.unlock() on button tap — iOS requirement
iOS Safari suspends AudioContext until a user gesture. **Must unlock INSIDE the btnStart handler, BEFORE any async operations:**

```javascript
onTap($('btnStart'), () => {
  audio.unlock();        // FIRST — synchronous
  audio.tone('whoosh');  // optional opening SFX
  startGame();           // may be async after this
});
```

If you call `audio.unlock()` inside `async function startGame()` after any `await`, iOS treats it as detached from the user gesture. No audio plays for the entire game. This is a common silent failure.

### Debugging audio
- **No sound on iOS at all?** → `audio.unlock()` isn't in the btnStart handler or is after an `await`
- **Music too quiet?** → `musicVol` below 0.05. Set to 0.08.
- **Voice cuts off another voice?** → Multiple `speakX()` calls without awaiting. Either queue them properly (`await speak1; await speak2`) OR use `clearQueue()` before the new one.
- **Voice lags behind gameplay?** → You're speaking old state. Call `audio.clearQueue()` before each new target announcement.
- **File plays on dev but not production?** → `AUDIO_BASE` wrong, or the file doesn't exist. Check the path in DevTools network tab.

---

## 6. Tracing games — the checkpoint system

This is a common area where new sessions regress. I've seen it built wrong multiple times.

### WRONG: Pixel-perfect path tracking
Trying to match the exact pixels of a number outline. Fragile, impossible to perfect, frustrating for kids.

### RIGHT: Invisible checkpoint sequence
Define ~5-10 checkpoint coordinates along the number's path (normalized 0-1). The child must hit them in order within a generous radius (~15% of canvas width).

```javascript
const CHECKPOINTS = {
  6: [
    {x:0.55,y:0.12}, {x:0.30,y:0.15}, {x:0.20,y:0.42},
    {x:0.22,y:0.68}, {x:0.45,y:0.85}, {x:0.72,y:0.80},
    {x:0.78,y:0.60}, {x:0.55,y:0.48}, {x:0.28,y:0.50}
  ],
  // etc
};
```

Pointer movement enters checkpoint radius → mark hit → advance. When all hit in sequence → trace complete.

### Multi-digit numbers (like 10, 20, 100)
Split into parts. Each part is a separate checkpoint array. Show "10: part 1/2" in HUD as child traces first digit, then "10: part 2/2".

```javascript
const CHECKPOINTS = {
  '10_first':  [/* the "1" */],
  '10_second': [/* the "0" */],
  '100_first': [/* the "1" */],
  '100_second': [/* middle "0" */],
  '100_third': [/* right "0" */],
};
```

Canvas for 3-digit numbers needs wider aspect ratio (1.4:1 or 1.6:1).

### Rendering the outline
- Draw the letter/number outline on canvas before gameplay — this is the visual target
- Tracing line renders on top as the finger moves
- 3-layer stroke for visibility: outer glow color, middle color, white core

### Touch handling
```javascript
canvas.addEventListener('touchmove', (e) => {
  e.preventDefault();                    // stops page scroll
  const rect = canvas.getBoundingClientRect();
  const touch = e.touches[0];
  const x = (touch.clientX - rect.left) / rect.width;   // normalized 0-1
  const y = (touch.clientY - rect.top) / rect.height;
  // check against next checkpoint
}, { passive: false });
```

**`touch-action: none`** on the canvas (not `manipulation`) — tracing needs to capture all pointer movement without the browser hijacking it for scroll/zoom.

---

## 7. The specific failure modes (what NOT to do)

### 🚫 Don't await voice clips in gameplay
See RULE 3. I've burned hours on this. Every single freeze bug I've shipped had `await audio.X()` in the hot path.

### 🚫 Don't use `Promise.resolve(pendingPromise)` to "wrap" for timeout races
It adopts the inner promise's state. Race is non-functional. Use this instead:
```javascript
Promise.race([
  new Promise(resolve => { audio.play(...).then(resolve, resolve); }),
  new Promise(resolve => setTimeout(resolve, 700))
]);
```

### 🚫 Don't put `#screenID { display: flex }` base styles
Breaks `.active` class pattern. Use ONLY `.screen{display:none}` and `.screen.active{display:flex}`. No ID-level display rules.

### 🚫 Don't use ease-in-out or ease for feedback animations
Feels limp. Use `cubic-bezier(0.34, 1.56, 0.64, 1)` for anything that should feel SATISFYING.

### 🚫 Don't put achievement visuals floating over the play area
They cover the target card on small screens. Put in HUD or celebration screen only.

### 🚫 Don't use "wrong" or "no" messaging
User specifically called this out. Kids feel judged. Use "Try again!" or "Almost!"

### 🚫 Don't show tiny numeral with big decoration
Violates Rule 1. Numeral is the HERO. Decoration is corner accent.

### 🚫 Don't double-speak numbers
Was a common pattern: `speakNumber(n); delay(140); speakNumber(n)`. User called this out as "frustratingly slow." Speak ONCE per event.

### 🚫 Don't `await audio.play('greetings')` between rounds
That's 2-3 seconds of dead air. Show the banner, fire the voice NON-BLOCKING, use `await delay(1400)` to time it.

### 🚫 Don't forget the notch
Every top-fixed element uses `env(safe-area-inset-top)`. Including the back button.

### 🚫 Don't rely on `new Audio().play()` alone for voice on iOS
After any `await`, the user-gesture context is lost and `new Audio().play()` silently fails. Use the AudioContext path in `_playFile()` as primary, HTML Audio as fallback.

### 🚫 Don't skip the progress tracking snippet
Every game file needs the tracking IIFE at the end:
```javascript
/* ═══ AHA! PROGRESS TRACKING ═══ */
(function(){
  function getKey(){ var parts=location.pathname.split('/').filter(Boolean);
    var last=parts[parts.length-1]||'index.html'; var game=last.replace('.html','');
    var theme=parts[parts.length-2]||'root'; if(game==='') game='index';
    return theme+'/'+game; }
  function load(){ try{return JSON.parse(localStorage.getItem('aha_progress')||'{}')}catch(e){return{}} }
  function save(p){ try{localStorage.setItem('aha_progress', JSON.stringify(p))}catch(e){} }
  function markAttempt(){ var p=load(), k=getKey();
    if(!p[k]) p[k]={attempted:true, attemptedAt:Date.now()}; save(p); }
  function markComplete(){ var p=load(), k=getKey();
    if(!p[k]) p[k]={}; p[k].completed=true; p[k].completedAt=Date.now();
    p[k].plays=(p[k].plays||0)+1; save(p); }
  var celeb = document.getElementById('scrCeleb');
  if (celeb){ var obs = new MutationObserver(function(){
    if(celeb.classList.contains('active')) markComplete(); });
    obs.observe(celeb, { attributes:true, attributeFilter:['class'] }); }
  setTimeout(markAttempt, 3000);
})();
```

The celebration screen element **must be `id="scrCeleb"`** — the MutationObserver watches that specific ID. If you name it `celebration` or `scrEnd`, the main hub's progress badges won't work.

### 🚫 Don't skip the `#scrCeleb` → `.active` transition
Some games fail to add `.active` to the celebration screen. Progress tracking never fires. Fix: always use `showScreen('scrCeleb')` which adds `.active`.

---

## 8. The complete checklist before you ship

**Read this top-to-bottom before saying "done."**

### Audio
- [ ] `const AUDIO_BASE = '../../audio';` (two levels up, exactly)
- [ ] GameAudio class copied in full — no simplifications
- [ ] `audio.unlock()` called in `onTap($('btnStart'), ...)` BEFORE anything else
- [ ] `audio.unlock()` NOT inside `async function startGame()` after any await
- [ ] Music starts in `startGame()` via `audio.startMusic()`
- [ ] `musicVol = 0.08` (not lower, not higher)
- [ ] Every `audio.play(...)` call in gameplay is fire-and-forget (no `await`)
- [ ] Wrong answer plays `audio.tone('wrong')` + `audio.play('wrong')` + re-speaks target after delay
- [ ] Correct answer plays `audio.tone('correct')` + `audio.play('correct')` + speaks number once
- [ ] Round complete plays `audio.tone('roundDone')` + `audio.play('round-complete')` NON-BLOCKING
- [ ] Final celebration plays TWO different game-complete phrases
- [ ] `audio.clearQueue()` called before new targets in bubble-pop-style games

### Visual
- [ ] Every numeral display is large (`clamp(54px, 14vw, 86px)` or larger)
- [ ] Every card/target shows the NUMERAL (decoration secondary)
- [ ] Background has animated particles (bats, stars, sparkles — not static)
- [ ] Character bobs/wiggles in idle
- [ ] Start button has `animation: glow 2.4s ease-in-out infinite`
- [ ] Confetti on round complete (~30 pieces)
- [ ] Confetti on game complete (60 pieces + second wave 35 after 2s)
- [ ] starBurst on every correct tap (7-8 sparkles from tap location)
- [ ] Wrong answer: `wrongShake` animation + shake class removed after 500ms
- [ ] Spring easing `cubic-bezier(0.34, 1.56, 0.64, 1)` on all feedback

### Layout
- [ ] Font: `'Arial Rounded MT Bold','Nunito','Quicksand',system-ui` (NOT Comic Sans)
- [ ] `overflow: hidden` on body
- [ ] `height: 100vh; height: 100dvh;` (both, in that order)
- [ ] `touch-action: manipulation` on body (NOT `none` unless canvas tracing)
- [ ] All tap targets ≥ 80px (`min-width: clamp(70px, 16vw, 90px)`)
- [ ] Viewport meta: `width=device-width, initial-scale=1.0, user-scalable=no, viewport-fit=cover`
- [ ] All top-fixed elements use `env(safe-area-inset-top)` for notch

### Game flow
- [ ] Title screen with Start button (glowing)
- [ ] Round 1 banner (non-blocking voice)
- [ ] 4 rounds played through
- [ ] Round-complete banners between (non-blocking voice)
- [ ] Celebration screen `#scrCeleb` with `.active` toggle
- [ ] "Play Again" button on celebration that resets and restarts
- [ ] HUD shows `1/4` round format
- [ ] Progress bar fills as items in round are completed
- [ ] Hint system: wiggle element at 4s inactivity, voice hint at 7s

### Navigation
- [ ] `<a href="../../" class="back-home-btn">← Home</a>` at `z-index: 9999` OUTSIDE all screens
- [ ] Floating `🏠` home bubble at bottom-right, `z-index: 9999`, shown during gameplay
- [ ] Both back buttons are plain `<a>` tags (work without JavaScript)

### Progress tracking
- [ ] Celebration screen element has `id="scrCeleb"` (exactly — not "scrEnd" or "celebration")
- [ ] `.active` class added when celebration shows
- [ ] Progress tracking IIFE snippet at the end of the script block
- [ ] File saves to `localStorage['aha_progress']` — a 3-second attempt + celebration-triggered completion

### Testing
- [ ] Game parses cleanly: `node -e "const fs=require('fs'); const html=fs.readFileSync('FILE.html','utf8'); const scripts=[...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(m=>m[1]).join('\n'); try{new Function(scripts); console.log('✓')}catch(e){console.log('✗ '+e.message)}"`
- [ ] Open in Chrome/Safari, tap Start, confirm first round plays
- [ ] Tap Back button at various points — always works
- [ ] Complete all 4 rounds — celebration fires, progress saved to localStorage
- [ ] Check `localStorage.getItem('aha_progress')` — contains completion record

---

## 9. How rounds actually escalate — detailed

### Card Match rounds
```javascript
const ROUNDS = [
  { choices: 2, display: 'full',    hintMode: 'strong' },
  // Target card and all option cards: NUMERAL + emoji + word
  // 2 option cards. Hint wiggles correct answer at 4s inactivity.
  
  { choices: 3, display: 'numeral', hintMode: 'subtle' },
  // Target: numeral + emoji only. Cards: numeral + word.
  // 3 options. Hint is a soft pulse rather than full wiggle.
  
  { choices: 4, display: 'dots',    hintMode: 'none' },
  // Target: emoji-pattern (6 = 🕷️🕷️🕷️🕷️🕷️🕷️) + SMALL numeral still visible.
  // Cards: numeral + word. No hints. Child must count.
  
  { choices: 4, display: 'word',    hintMode: 'none', timer: true },
  // Target: word + small numeral. Cards: numeral only.
  // Gentle background color shift suggests urgency (NO failure state).
];
```

### Pairs rounds
```javascript
const ROUNDS = [
  { pairs: 3, peek: 1500, pairType: 'numeral-dots' },
  // 6 cards, 3 pairs. 1.5s peek before flipping. Pair = numeral ↔ dot-pattern
  // (both cards show the NUMERAL — dot pattern is decoration on one card)
  
  { pairs: 4, peek: 0,    pairType: 'numeral-dots' },
  // 8 cards, no peek. Still numeral ↔ numeral-with-pattern.
  
  { pairs: 5, peek: 0,    pairType: 'numeral-word' },
  // 10 cards. Pair = numeral ↔ word. But WORD CARD STILL SHOWS NUMERAL smaller.
  
  { pairs: 6, peek: 0,    pairType: 'mixed' },
  // 12 cards. Mix of pair types. All cards show numeral somewhere.
];
```

**Cross-representation rule:** Both cards of a pair must show the SAME numeral prominently. If card A shows "60" with emoji and card B shows "60" in a different color with different decoration, that's fine. If card A shows "60" and card B shows the word "sixty" with tiny "60", that VIOLATES rule 1 — the numeral on card B is too small.

### Bubble Pop rounds
```javascript
const ROUNDS = [
  { display: 'numeral-word', speed: 0.85, spawnMs: 900,  announce: true,  targetCount: 3 },
  { display: 'numeral',      speed: 1.10, spawnMs: 750,  announce: false, targetCount: 4 },
  { display: 'dots+num',     speed: 0.85, spawnMs: 900,  announce: true,  targetCount: 3 },
  { display: 'mixed',        speed: 1.25, spawnMs: 700,  announce: false, targetCount: 4 },
];
```

**Bubble rise speed units:** px per frame at 60fps. 0.85 = ~50px/sec = ~12-15s to traverse a phone screen. Anything above 1.5 is too fast for 3-year-olds. Anything below 0.35 feels slow.

### Sequence rounds
All 4 rounds use the same 5 numbers in order (0→5, or 6→10, or 10→50). Escalation is about scaffolding:

```javascript
const ROUNDS = [
  { label: 'Round 1', display: 'full',    hintMode: 'strong' },  // next-to-tap pulses brightly
  { label: 'Round 2', display: 'full',    hintMode: 'none' },    // same display, no pulse
  { label: 'Round 3', display: 'dots',    hintMode: 'none' },    // dot patterns + small numeral
  { label: 'Round 4', display: 'mixed',   hintMode: 'none', timer: true },  // smaller, timer bg shift
];
```

### Tracing levels
```javascript
const LEVELS = [
  { opacity: 1.0, guide: true },   // animated sparkle traces path first
  { opacity: 1.0, guide: false },  // full outline, no guide
  { opacity: 0.5, guide: false },  // faded outline (partial memory)
  { opacity: 0.15, guide: false }, // barely visible (nearly from memory)
];
```

---

## 10. Things I tried that DIDN'T work

Documenting my failures so future sessions don't repeat them.

### ❌ "I'll await voice clips between rounds for cleaner timing"
Result: 8-second dead air between every round. User: "frustratingly slow."
Fix: Fire-and-forget voice, use `await delay(1400)` for banner duration.

### ❌ "I'll add `Promise.race` with timeout to prevent audio hangs"
```javascript
await Promise.race([
  Promise.resolve(audio.play('x')),
  new Promise(r => setTimeout(r, 700))
]);
```
Result: Game still froze. `Promise.resolve()` adopts the inner promise's state, so the race was racing itself.
Fix: Don't await audio at all. Use setTimeout for timing.

### ❌ "I'll put a nice sanctuary achievement in the top-right corner"
Result: Covered the target card on small screens.
Fix: Achievement = small HUD counter OR only on celebration screen.

### ❌ "I'll make the tracing game use pixel-perfect path detection"
Result: Impossible for kids. Too tight. Would only register perfect strokes.
Fix: Invisible checkpoint system with 15% canvas-width hit radius.

### ❌ "I'll have the cat say 'no that is wrong!' when it's incorrect"
Result: User said it felt "aggressive."
Fix: "Try again! Meow! 💛"

### ❌ "I'll add a grumpy cat character for variety"
Result: User said it felt "aggressive, grouchy face."
Fix: Replaced with Happy Kitty 😻.

### ❌ "I'll use `await audio.unlock()` in the start handler for safety"
Result: On iOS, if unlock takes >0.5s the tap gesture context is lost, no audio ever plays.
Fix: `audio.unlock()` is synchronous — don't await it.

### ❌ "I'll make the ice cream conveyor fast and exciting"
Result: Too fast to tap. User: "impossible even on iPhone."
Fix: Conveyor speed based on viewport width — aim for 6-13 seconds to traverse.

### ❌ "I'll use a 300ms shake animation for wrong feedback"
Result: Too fast, feels like a glitch.
Fix: 500ms shake with `cubic-bezier(0.34, 1.56, 0.64, 1)`.

### ❌ "I'll use written word cards in pairs for educational variety"
Result: User: "it has a lot of written words and not the numbers which we requested."
Fix: Same-numeral pairs with different decoration styles, NO word-only cards.

### ❌ "I'll use conic-gradient for the wheel and have it spin fast for excitement"
Result: User: "I didn't know what I was supposed to do."
Fix: Slow rotation (14s/revolution), big visible target in HUD, clear intro overlay with voice explanation.

---

## 11. Reading ARCHITECTURE.md — what actually matters

Sections that you MUST read and understand:
- **§5 Audio System — Complete Reference** — the full GameAudio class with iOS fixes
- **§5a-ii Audio path & iOS playback rules** — why AudioContext-first matters
- **§7 Visual Feedback System** — confetti, starBurst, hint system
- **§8 Number and Letter Representation** — the visual-first number rule
- **§17 Before-You-Build Checklist** — the same checklist I include above

Sections that are helpful but not critical:
- §1-4 (layout, design philosophy — good context)
- §10 (character system — applies less to v2 games which use emoji)
- §14-16 (HUD layout, interaction, app.json — mostly for older games/v1)

---

## 12. When the user says something doesn't work

Watch for these specific symptoms in their feedback — each maps to a known bug class:

| User says | Probable cause |
|-----------|----------------|
| "It froze" / "stuck" / "can't get out" | Awaited audio that hung. See RULE 3. Add back button. |
| "Nothing happens when I tap" | audio.unlock() not in gesture, or `#gameArea.active` not toggling, or JS parse error killed listeners |
| "It's too fast" | Animation durations < 300ms, or conveyor/bubble speed too high |
| "Too slow" / "nothing happens between" | Awaited voice clips. Remove awaits. |
| "It's glitchy" | Usually a CSS specificity bug or a state machine race |
| "It's behind the notch" | Missing `env(safe-area-inset-top)` |
| "Feels aggressive" | Too-stern wrong-answer messaging, or a grumpy character face |
| "Can't see the number" | Numeral too small (rule 1 violation) or hidden behind a floating UI |
| "Number says itself twice" | Double speak. See RULE 2. |

When fixing: **find the specific root cause before patching.** The user will tell you if it's still broken. They're a patient tester but they'll notice.

---

## 13. The deployment flow

1. Build or edit files locally
2. Test the JS parses: `node -e "..."` (see checklist)
3. `git add <files>`
4. `git commit -m "short descriptive message"`
5. `git push origin main`
6. Vercel auto-deploys to `https://learning-games-one.vercel.app/` (~60s)
7. Hard refresh on tablet (⌘⇧R) or close/reopen PWA

**Commit message style:** lead with what + why. Include root cause for bug fixes. Example:

> Fix Monster Mixer freeze at horns step
> 
> Root cause: Promise.race([Promise.resolve(pending), timeout]) was
> non-functional — Promise.resolve adopts the inner promise's state.
> Race was racing the hung promise against itself.
> 
> Fix: eliminated all async/await in game flow; added 2500ms safety
> net that force-shows celebration; celebrationShown flag prevents
> double-fire.

---

## 14. The user

The user is patient, detail-oriented, and tests on real devices (iPhone + tablet PWA). They pay attention to:
- Whether the game feels fun (not just educational)
- Whether a 3-5yo could actually play it
- Whether gameplay flows without dead air
- Whether things visibly respond
- The soft stuff: tone, character reactions, supportiveness

They do NOT care about:
- Complex educational theory
- Being "strict" with correct/wrong
- Perfect visuals (they'll accept emoji instead of custom SVGs)

**When they give feedback, believe them.** They play the games with kids. Their "too fast" or "too aggressive" is real.

---

## 15. Before you write ANY code

1. Read `ARCHITECTURE.md` — or at least §5, §7, §8, §17
2. Read the relevant v2/6-10 game — it's the gold standard
3. Read `GAME_TEMPLATE.html` — shows every pattern correctly
4. Read this file top-to-bottom

Then build. You will save yourself hours of debugging.

Good luck. Make it bouncy. Make it kind. Make it work on iOS.

— Claude, writing to Claude

---

*Last updated: the end of a long session where we built 75+ games, made and fixed every mistake in this document, and shipped a PWA the kids actually play.*
