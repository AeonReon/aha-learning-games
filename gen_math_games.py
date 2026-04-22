#!/usr/bin/env python3
"""Generate the remaining 7 math-zone games from a shared template.
Each game has: theme color palette, hero emoji, celebration emoji, scene
renderer (HTML chunk + JS chunk), PROBLEMS array, background particles.
"""
from pathlib import Path

BASE = Path(__file__).parent / "v2" / "math-zone"

TEMPLATE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<meta name="theme-color" content="{theme_color}">
<title>{title} · aha!</title>
<style>
:root{{--spring:cubic-bezier(0.34,1.56,0.64,1)}}
*{{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent;user-select:none;-webkit-user-select:none}}
html,body{{width:100%;height:100vh;height:100dvh;overflow:hidden;font-family:'Arial Rounded MT Bold','Nunito','Quicksand',system-ui,Arial,sans-serif;
  background:{body_grad};color:{text_color};touch-action:manipulation;position:fixed;inset:0}}
.back-home-btn{{position:fixed;top:max(12px,env(safe-area-inset-top,12px) + 6px);left:14px;z-index:9999;background:#fff;color:{text_color};border:4px solid {accent};border-radius:999px;padding:10px 18px;font-size:16px;font-weight:900;text-decoration:none;box-shadow:0 4px 0 {text_color},0 6px 12px rgba(0,0,0,0.2)}}
.home-bubble{{position:fixed;bottom:18px;right:18px;z-index:9999;width:56px;height:56px;border-radius:50%;background:#fff;border:4px solid {accent};display:none;align-items:center;justify-content:center;font-size:28px;text-decoration:none;box-shadow:0 4px 12px rgba(0,0,0,0.3)}}
.home-bubble.show{{display:flex}}
.bg-part{{position:absolute;font-size:22px;animation:bgPartAnim linear infinite;pointer-events:none;opacity:0.55}}
@keyframes bgPartAnim{{from{{transform:translateY(110vh) rotate(0)}}to{{transform:translateY(-10vh) rotate(360deg)}}}}
.screen{{position:fixed;inset:0;display:none;flex-direction:column;align-items:center;justify-content:center;padding:16px;overflow:hidden;z-index:200}}
.screen.active{{display:flex}}
.title-emoji{{font-size:clamp(140px,32vw,240px);animation:heroBob 2.4s var(--spring) infinite;filter:drop-shadow(0 10px 20px rgba(0,0,0,0.3))}}
@keyframes heroBob{{0%,100%{{transform:translateY(0) rotate(-6deg)}}50%{{transform:translateY(-14px) rotate(6deg)}}}}
.title-big{{font-size:clamp(40px,10vw,70px);color:#fff;-webkit-text-stroke:3px {text_color};text-align:center;text-shadow:4px 6px 0 {title_shadow},0 8px 14px rgba(0,0,0,0.3);line-height:1.05;margin:10px 0}}
.title-sub{{font-size:clamp(18px,4.2vw,24px);color:#fff;font-weight:900;margin-bottom:26px;text-shadow:2px 2px 0 {text_color}}}
.start-btn{{background:linear-gradient(180deg,#fbbf24,#d97706);color:#7c2d12;border:5px solid #fff;border-radius:999px;padding:20px 50px;font-size:clamp(22px,5.5vw,30px);font-weight:900;box-shadow:0 6px 0 #7c2d12,0 10px 20px rgba(0,0,0,0.3);cursor:pointer;animation:glow 2.4s ease-in-out infinite}}
@keyframes glow{{0%,100%{{box-shadow:0 6px 0 #7c2d12,0 10px 20px rgba(0,0,0,0.3),0 0 20px rgba(251,191,36,0.5)}}50%{{box-shadow:0 6px 0 #7c2d12,0 10px 20px rgba(0,0,0,0.3),0 0 44px rgba(251,191,36,0.95)}}}}
.start-btn:active{{transform:translateY(3px) scale(0.97)}}
.hud{{position:fixed;top:max(12px,env(safe-area-inset-top,12px) + 6px);left:50%;transform:translateX(-50%);z-index:50;background:rgba(0,0,0,0.5);color:#fff;border-radius:22px;padding:7px 20px;font-weight:900;font-size:15px;border:2px solid rgba(255,255,255,0.4)}}

{scene_css}

.equation{{font-size:clamp(38px,9vw,54px);font-weight:900;text-align:center;margin:14px 0;color:#fff;text-shadow:3px 3px 0 {text_color},0 6px 14px rgba(0,0,0,0.3)}}
.equation .q{{display:inline-block;background:#fff;color:#dc2626;border-radius:14px;padding:2px 18px;min-width:68px;box-shadow:inset 0 4px 0 rgba(0,0,0,0.15);animation:qPulse 0.9s ease-in-out infinite;-webkit-text-stroke:0}}
@keyframes qPulse{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.1)}}}}
.choices{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;width:100%;max-width:420px;padding:0 4px;margin-bottom:24px}}
.choice{{font-size:clamp(44px,11vw,60px);font-weight:900;padding:14px 0;border-radius:22px;border:5px solid #fff;background:#fef3c7;color:#7c2d12;box-shadow:0 6px 0 #7c2d12,0 10px 16px rgba(0,0,0,0.25);cursor:pointer;transition:transform 0.18s var(--spring);min-height:clamp(70px,16vw,90px);touch-action:manipulation}}
.choice:active{{transform:translateY(3px) scale(0.95)}}
.choice.correct{{background:#86EFAC;color:#14532D;animation:pop 0.5s var(--spring)}}
.choice.wrong{{animation:shake 0.5s ease}}
@keyframes pop{{0%{{transform:scale(1)}}50%{{transform:scale(1.2)}}100%{{transform:scale(1)}}}}
@keyframes shake{{0%,100%{{transform:translateX(0)}}25%{{transform:translateX(-10px)}}50%{{transform:translateX(10px)}}75%{{transform:translateX(-6px)}}}}
.celeb-emoji{{font-size:clamp(140px,34vw,240px);animation:celebSpin 1.4s var(--spring) infinite;filter:drop-shadow(0 10px 24px rgba(0,0,0,0.4))}}
@keyframes celebSpin{{0%,100%{{transform:translateY(0) rotate(-10deg) scale(1)}}50%{{transform:translateY(-24px) rotate(10deg) scale(1.12)}}}}
.celeb-title{{font-size:clamp(34px,8vw,56px);color:#fff;-webkit-text-stroke:3px {text_color};text-shadow:3px 4px 0 {title_shadow};text-align:center;margin-bottom:10px}}
.celeb-stars{{font-size:clamp(44px,11vw,64px);margin-bottom:22px}}
.celeb-btns{{display:flex;gap:12px;flex-wrap:wrap;justify-content:center}}
.btn-celeb{{font-size:clamp(16px,4.2vw,20px);font-weight:900;padding:16px 28px;border-radius:28px;border:4px solid #fff;cursor:pointer;box-shadow:0 6px 0 rgba(0,0,0,0.35),0 10px 16px rgba(0,0,0,0.3);text-decoration:none;display:inline-flex;align-items:center;gap:4px}}
.btn-play{{background:#fbbf24;color:#7c2d12}}
.btn-home{{background:#fff;color:{text_color}}}
.star{{position:fixed;pointer-events:none;font-size:24px;z-index:900;animation:starFly 0.9s var(--spring) forwards}}
@keyframes starFly{{0%{{transform:translate(0,0) scale(0.3);opacity:1}}100%{{transform:translate(var(--dx),var(--dy)) scale(1.5);opacity:0}}}}
.fx-canvas{{position:fixed;inset:0;pointer-events:none;z-index:800}}
</style>
</head>
<body>
<a href="../../" class="back-home-btn">← Home</a>
<a href="../../" id="homeBubble" class="home-bubble">🏠</a>
<canvas class="fx-canvas" id="fxCanvas"></canvas>

<div class="screen active" id="scrTitle">
  <div class="title-emoji">{title_emoji}</div>
  <h1 class="title-big">{title_upper}</h1>
  <div class="title-sub">{subtitle}</div>
  <button class="start-btn" id="btnStart">▶ PLAY</button>
</div>

<div class="screen" id="scrGame">
  <div class="hud">{title_emoji} Problem <span id="hudNum">1</span>/5</div>
  {scene_html}
  <div class="equation" id="equation"></div>
  <div class="choices" id="choices"></div>
</div>

<div class="screen" id="scrCeleb">
  <div class="celeb-emoji">{celeb_emoji}</div>
  <div class="celeb-title">{celeb_title}</div>
  <div class="celeb-stars">⭐⭐⭐⭐⭐</div>
  <div class="celeb-btns">
    <button class="btn-celeb btn-play" id="btnPlay">Play Again</button>
    <a class="btn-celeb btn-home" href="../../">🏠 Home</a>
  </div>
</div>

<script>
const AUDIO_BASE='../../audio',GAUDIO='audio/{slug}/';
const PROBLEMS={problems};
class GameAudio{{constructor(){{this.ctx=null;this.musicGain=null;this.sfxGain=null;this.musicVol=0.08;this.sfxVol=0.3;this.musicDucked=0.025;this.voiceQueue=[];this.speaking=false;this._lastPlayed={{}};this.musicOn=true;this.musicScheduler=null}}
_init(){{if(this.ctx)return;this.ctx=new(window.AudioContext||window.webkitAudioContext)();this.musicGain=this.ctx.createGain();this.musicGain.gain.value=0;this.musicGain.connect(this.ctx.destination);this.sfxGain=this.ctx.createGain();this.sfxGain.gain.value=this.sfxVol;this.sfxGain.connect(this.ctx.destination)}}
unlock(){{this._init();if(this.ctx.state==='suspended')this.ctx.resume().catch(()=>{{}})}}
_duck(){{if(!this.musicGain)return;const n=this.ctx.currentTime;this.musicGain.gain.cancelScheduledValues(n);this.musicGain.gain.setValueAtTime(this.musicGain.gain.value,n);this.musicGain.gain.linearRampToValueAtTime(this.musicDucked,n+0.2)}}
_unduck(){{if(!this.musicGain)return;const n=this.ctx.currentTime;this.musicGain.gain.cancelScheduledValues(n);this.musicGain.gain.setValueAtTime(this.musicGain.gain.value,n);this.musicGain.gain.linearRampToValueAtTime(this.musicOn?this.musicVol:0,n+0.3)}}
tone(k){{if(!this.ctx)return;const c=this.ctx,n=c.currentTime;let f=[440],t='sine',d=0.18;
  if(k==='correct'){{f=[523.25,659.25,783.99];d=0.22;t='triangle'}}else if(k==='wrong'){{f=[392,329.63];d=0.3;t='sine'}}else if(k==='roundDone'){{f=[523.25,659.25,783.99,1046.5];d=0.18;t='triangle'}}else if(k==='whoosh'){{f=[880];d=0.18;t='triangle'}}
  f.forEach((fr,i)=>{{const o=c.createOscillator(),g=c.createGain();o.type=t;o.frequency.value=fr;g.gain.setValueAtTime(0.0001,n+i*0.06);g.gain.exponentialRampToValueAtTime(0.24,n+i*0.06+0.02);g.gain.exponentialRampToValueAtTime(0.0001,n+i*0.06+d);o.connect(g).connect(this.sfxGain||c.destination);o.start(n+i*0.06);o.stop(n+i*0.06+d+0.05)}})}}
_playFile(p){{const fb=()=>new Promise(r=>{{const a=new Audio(p);a.onended=r;a.onerror=()=>r();a.play().catch(()=>r())}});
  if(this.ctx&&this.ctx.state!=='closed')return fetch(p).then(r=>{{if(!r.ok)throw 0;return r.arrayBuffer()}}).then(b=>this.ctx.decodeAudioData(b)).then(buf=>new Promise(res=>{{const s=this.ctx.createBufferSource();s.buffer=buf;s.connect(this.ctx.destination);s.onended=res;s.start()}})).catch(()=>fb());
  return fb()}}
speak(p){{return new Promise(r=>{{this.voiceQueue.push({{path:p,resolve:r}});this._pump()}})}}
_pump(){{if(this.speaking||!this.voiceQueue.length)return;this.speaking=true;const{{path,resolve}}=this.voiceQueue.shift();this._duck();this._playFile(path).then(()=>{{this.speaking=false;if(!this.voiceQueue.length)this._unduck();resolve();this._pump()}})}}
clearQueue(){{this.voiceQueue.forEach(q=>q.resolve());this.voiceQueue=[]}}
speakNumber(n){{return this.speak(`${{AUDIO_BASE}}/numbers/${{n}}.mp3`)}}
speakOp(op){{const f=op==='+'?'plus':op==='-'?'minus':'equals';return this.speak(`${{GAUDIO}}${{f}}.mp3`)}}
speakGame(name){{return this.speak(`${{GAUDIO}}${{name}}.mp3`)}}
play(name){{const pool=name==='correct'?['correct1','correct2','correct3']:name==='wrong'?['wrong1','wrong2']:[name];let c=pool[Math.floor(Math.random()*pool.length)];if(pool.length>1&&c===this._lastPlayed[name])c=pool.find(x=>x!==this._lastPlayed[name])||c;this._lastPlayed[name]=c;return this.speak(`${{GAUDIO}}${{c}}.mp3`)}}
startMusic(){{if(!this.ctx||this.musicScheduler)return;this.musicOn=true;const n=this.ctx.currentTime;this.musicGain.gain.cancelScheduledValues(n);this.musicGain.gain.linearRampToValueAtTime(this.musicVol,n+1);const SCALE=[523.25,587.33,659.25,783.99,880,1046.5];let next=this.ctx.currentTime+0.1;
  this.musicScheduler=setInterval(()=>{{while(next<this.ctx.currentTime+0.3){{const f=SCALE[Math.floor(Math.random()*SCALE.length)];const o=this.ctx.createOscillator(),g=this.ctx.createGain();o.type='triangle';o.frequency.value=f;g.gain.setValueAtTime(0.0001,next);g.gain.exponentialRampToValueAtTime(0.55,next+0.05);g.gain.exponentialRampToValueAtTime(0.0001,next+0.5);o.connect(g).connect(this.musicGain);o.start(next);o.stop(next+0.55);next+=0.48}}}},60)}}}}
const audio=new GameAudio();
const $=id=>document.getElementById(id);
function onTap(el,fn){{let f=false;const h=e=>{{if(f)return;f=true;setTimeout(()=>f=false,300);e.preventDefault();e.stopPropagation();fn(e)}};el.addEventListener('click',h);el.addEventListener('touchend',h,{{passive:false}})}}
function showScreen(id){{document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));$(id).classList.add('active');$('homeBubble').classList.toggle('show',id==='scrGame')}}
function starBurst(x,y){{const em=['⭐','✨','💫','🌟'];for(let i=0;i<8;i++){{const s=document.createElement('div');s.className='star';s.textContent=em[i%4];s.style.left=(x-12)+'px';s.style.top=(y-12)+'px';const a=(i/8)*Math.PI*2;s.style.setProperty('--dx',Math.cos(a)*90+'px');s.style.setProperty('--dy',Math.sin(a)*90+'px');document.body.appendChild(s);setTimeout(()=>s.remove(),900)}}}}
function burstConfetti(n=30){{const c=$('fxCanvas'),ctx=c.getContext('2d');c.width=innerWidth;c.height=innerHeight;const parts=[];
  for(let i=0;i<n;i++)parts.push({{x:innerWidth/2,y:innerHeight/3,vx:(Math.random()-0.5)*12,vy:Math.random()*-16-3,color:['#fbbf24','#dc2626','#fcd34d','#86efac','#f87171','#a3e635'][i%6],size:Math.random()*9+5,rot:Math.random()*Math.PI,vr:(Math.random()-0.5)*0.3,life:1}});
  (function loop(){{ctx.clearRect(0,0,c.width,c.height);let al=0;for(const p of parts){{if(p.life<=0)continue;al++;p.x+=p.vx;p.y+=p.vy;p.vy+=0.4;p.vx*=0.99;p.rot+=p.vr;p.life-=0.012;ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.rot);ctx.globalAlpha=Math.max(0,p.life);ctx.fillStyle=p.color;ctx.fillRect(-p.size/2,-p.size/4,p.size,p.size/2);ctx.restore()}}if(al>0)requestAnimationFrame(loop);else ctx.clearRect(0,0,c.width,c.height)}})()}}

{scene_js}

let pi=0;
function renderEquation(p){{$('equation').innerHTML=`${{p.a}} ${{p.op}} ${{p.b}} = <span class="q">?</span>`}}
function renderChoices(p){{const box=$('choices');box.innerHTML='';const set=new Set([p.answer]);const offs=[1,-1,2,-2];
  while(set.size<3){{const v=p.answer+offs[Math.floor(Math.random()*offs.length)];if(v>=0&&v<=12)set.add(v)}}
  [...set].sort(()=>Math.random()-0.5).forEach(v=>{{const b=document.createElement('button');b.className='choice';b.textContent=v;onTap(b,()=>handleChoice(b,v,p));box.appendChild(b)}})}}
function nextProblem(){{if(pi>=PROBLEMS.length){{finish();return}}const p=PROBLEMS[pi];$('hudNum').textContent=pi+1;renderScene(p);renderEquation(p);renderChoices(p);
  setTimeout(()=>{{audio.clearQueue();audio.speakNumber(p.a);audio.speakOp(p.op);audio.speakNumber(p.b);audio.speakOp('=')}},350)}}
function handleChoice(btn,v,p){{const r=btn.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2;
  if(v===p.answer){{audio.tone('correct');btn.classList.add('correct');starBurst(cx,cy);audio.clearQueue();audio.speakNumber(p.answer);audio.play('correct');pi++;setTimeout(nextProblem,900)}}
  else{{audio.tone('wrong');btn.classList.add('wrong');audio.play('wrong');setTimeout(()=>btn.classList.remove('wrong'),520)}}}}
function finish(){{showScreen('scrCeleb');burstConfetti(60);audio.tone('roundDone');setTimeout(()=>burstConfetti(40),800);setTimeout(()=>audio.speakGame('complete'),500)}}
function startGame(){{pi=0;showScreen('scrGame');audio.startMusic();setTimeout(()=>audio.speakGame('start'),400);setTimeout(nextProblem,2400)}}
onTap($('btnStart'),()=>{{audio.unlock();audio.tone('whoosh');startGame()}});
onTap($('btnPlay'),()=>{{showScreen('scrTitle')}});

(function(){{for(let i=0;i<{bg_count};i++){{const l=document.createElement('div');l.className='bg-part';l.textContent={bg_emojis}[i%{bg_emoji_count}];l.style.left=Math.random()*100+'vw';l.style.animationDuration=(10+Math.random()*8)+'s';l.style.animationDelay=(Math.random()*10)+'s';document.body.appendChild(l)}}}})();

(function(){{function getKey(){{var parts=location.pathname.split('/').filter(Boolean);var last=parts[parts.length-1]||'index.html';var game=last.replace('.html','');var theme=parts[parts.length-2]||'root';if(game==='')game='index';return theme+'/'+game}}
function load(){{try{{return JSON.parse(localStorage.getItem('aha_progress')||'{{}}')}}catch(e){{return{{}}}}}}function save(p){{try{{localStorage.setItem('aha_progress',JSON.stringify(p))}}catch(e){{}}}}
function markAttempt(){{var p=load(),k=getKey();if(!p[k])p[k]={{attempted:true,attemptedAt:Date.now()}};save(p)}}
function markComplete(){{var p=load(),k=getKey();if(!p[k])p[k]={{}};p[k].completed=true;p[k].completedAt=Date.now();p[k].plays=(p[k].plays||0)+1;save(p)}}
var celeb=document.getElementById('scrCeleb');if(celeb){{var obs=new MutationObserver(function(){{if(celeb.classList.contains('active'))markComplete()}});obs.observe(celeb,{{attributes:true,attributeFilter:['class']}})}}
setTimeout(markAttempt,3000)}})();
</script>
</body>
</html>
'''

GAMES = [
    # ── counting-sheep (addition) ──────────────────────────────────────
    {
        "slug":"counting-sheep","title":"Counting Sheep","title_upper":"COUNTING SHEEP","title_emoji":"🐑",
        "subtitle":"Count all the sheep that jumped!","celeb_emoji":"😴","celeb_title":"SLEEPY WINNER!",
        "theme_color":"#7c3aed","body_grad":"linear-gradient(180deg,#e9d5ff 0%,#a78bfa 55%,#4c1d95 100%)",
        "text_color":"#4c1d95","title_shadow":"#ec4899","accent":"#c4b5fd",
        "problems":"[{a:1,b:2,op:'+',answer:3},{a:2,b:3,op:'+',answer:5},{a:3,b:4,op:'+',answer:7},{a:4,b:3,op:'+',answer:7},{a:5,b:4,op:'+',answer:9}]",
        "bg_count":12,"bg_emojis":"['🌙','⭐','☁️']","bg_emoji_count":3,
        "scene_css":""".pasture{position:relative;width:min(92vw,460px);height:min(34vh,220px);margin-top:64px;display:flex;align-items:flex-end;justify-content:center;gap:12px}
.flock{display:flex;flex-wrap:wrap;justify-content:center;align-items:flex-end;gap:4px;max-width:42%}
.sheep{font-size:clamp(30px,7vw,46px);animation:sheepJump 1.6s ease-in-out infinite;filter:drop-shadow(0 3px 4px rgba(0,0,0,0.3))}
@keyframes sheepJump{0%,80%,100%{transform:translateY(0)}40%{transform:translateY(-14px)}}
.fence{width:8px;height:90px;background:linear-gradient(180deg,#a16207,#713f12);border-radius:3px;box-shadow:0 4px 0 rgba(0,0,0,0.25)}
.fence::after{content:'';display:block;width:8px;height:12px;background:#713f12;border-radius:2px;margin-top:2px}""",
        "scene_html":"""<div class="pasture">
    <div class="flock" id="flockL"></div>
    <div class="fence"></div>
    <div class="flock" id="flockR"></div>
  </div>""",
        "scene_js":"""function renderScene(p){
  const L=$('flockL'),R=$('flockR');L.innerHTML='';R.innerHTML='';
  for(let i=0;i<p.a;i++){const s=document.createElement('span');s.className='sheep';s.textContent='🐑';s.style.animationDelay=(i*0.15)+'s';L.appendChild(s)}
  for(let i=0;i<p.b;i++){const s=document.createElement('span');s.className='sheep';s.textContent='🐑';s.style.animationDelay=(i*0.15+0.3)+'s';R.appendChild(s)}
}""",
    },
    # ── piggy-bank (addition) ─────────────────────────────────────────
    {
        "slug":"piggy-bank","title":"Piggy Bank","title_upper":"PIGGY BANK","title_emoji":"🐷",
        "subtitle":"Count all the coins in the bank!","celeb_emoji":"🐽","celeb_title":"PIGGY WINNER!",
        "theme_color":"#db2777","body_grad":"linear-gradient(180deg,#fbcfe8 0%,#ec4899 55%,#831843 100%)",
        "text_color":"#831843","title_shadow":"#fbbf24","accent":"#f9a8d4",
        "problems":"[{a:1,b:2,op:'+',answer:3},{a:2,b:3,op:'+',answer:5},{a:3,b:4,op:'+',answer:7},{a:4,b:5,op:'+',answer:9},{a:5,b:5,op:'+',answer:10}]",
        "bg_count":12,"bg_emojis":"['🪙','💰','💎']","bg_emoji_count":3,
        "scene_css":""".bank-wrap{position:relative;width:min(88vw,400px);height:min(38vh,250px);margin-top:62px;display:flex;align-items:flex-end;justify-content:center;gap:14px}
.coin-pile{display:flex;flex-direction:column-reverse;align-items:center;gap:3px;flex:0 0 30%}
.coin-pile.right{flex-direction:column-reverse}
.coin-label{font-size:32px;color:#fff;font-weight:900;text-shadow:2px 2px 0 #831843}
.coin{font-size:clamp(26px,6.5vw,38px);animation:coinDrop 0.5s var(--spring);filter:drop-shadow(0 3px 4px rgba(0,0,0,0.4))}
@keyframes coinDrop{from{transform:translateY(-30px) rotate(-180deg);opacity:0}to{transform:translateY(0) rotate(0);opacity:1}}
.piggy{font-size:clamp(90px,22vw,140px);animation:piggyWiggle 2.2s ease-in-out infinite;filter:drop-shadow(0 6px 10px rgba(0,0,0,0.4))}
@keyframes piggyWiggle{0%,100%{transform:rotate(-3deg) scale(1)}50%{transform:rotate(3deg) scale(1.05)}}""",
        "scene_html":"""<div class="bank-wrap">
    <div class="coin-pile" id="pileL"></div>
    <div class="piggy">🐷</div>
    <div class="coin-pile" id="pileR"></div>
  </div>""",
        "scene_js":"""function renderScene(p){
  const L=$('pileL'),R=$('pileR');L.innerHTML='';R.innerHTML='';
  for(let i=0;i<p.a;i++){const c=document.createElement('span');c.className='coin';c.textContent='🪙';c.style.animationDelay=(i*0.1)+'s';L.appendChild(c)}
  for(let i=0;i<p.b;i++){const c=document.createElement('span');c.className='coin';c.textContent='🪙';c.style.animationDelay=(i*0.1+0.3)+'s';R.appendChild(c)}
}""",
    },
    # ── fish-tank (subtraction) ────────────────────────────────────────
    {
        "slug":"fish-tank","title":"Fish Tank","title_upper":"FISH TANK","title_emoji":"🐠",
        "subtitle":"Some fish swim away — how many stay?","celeb_emoji":"🐟","celeb_title":"SPLASHY WINNER!",
        "theme_color":"#0891b2","body_grad":"linear-gradient(180deg,#cffafe 0%,#06b6d4 55%,#155e75 100%)",
        "text_color":"#155e75","title_shadow":"#0369a1","accent":"#67e8f9",
        "problems":"[{a:3,b:1,op:'-',answer:2},{a:5,b:2,op:'-',answer:3},{a:6,b:3,op:'-',answer:3},{a:8,b:3,op:'-',answer:5},{a:10,b:4,op:'-',answer:6}]",
        "bg_count":12,"bg_emojis":"['🫧','💧','🐚']","bg_emoji_count":3,
        "scene_css":""".tank{position:relative;width:min(92vw,440px);height:min(40vh,260px);margin-top:62px;background:linear-gradient(180deg,rgba(255,255,255,0.25),rgba(255,255,255,0.08));border:6px solid #fff;border-radius:20px;box-shadow:inset 0 -8px 20px rgba(0,0,0,0.15),0 10px 20px rgba(0,0,0,0.3);display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:10px;padding:14px;overflow:hidden}
.fish{font-size:clamp(36px,9vw,50px);animation:fishSwim 2.2s ease-in-out infinite;filter:drop-shadow(0 3px 4px rgba(0,0,0,0.3));transition:transform 0.8s}
.fish.gone{animation:fishLeave 0.8s ease forwards}
@keyframes fishSwim{0%,100%{transform:translateX(0) rotate(0)}50%{transform:translateX(12px) rotate(8deg)}}
@keyframes fishLeave{0%{transform:translateX(0);opacity:1}100%{transform:translateX(200px) rotate(30deg);opacity:0}}""",
        "scene_html":"""<div class="tank" id="tank"></div>""",
        "scene_js":"""function renderScene(p){
  const t=$('tank');t.innerHTML='';
  for(let i=0;i<p.a;i++){const f=document.createElement('span');f.className='fish';f.textContent=['🐠','🐟','🐡'][i%3];f.style.animationDelay=(i*0.15)+'s';t.appendChild(f)}
  setTimeout(()=>{const fish=[...t.querySelectorAll('.fish')];for(let k=0;k<p.b;k++){const idx=fish.length-1-k;if(fish[idx])setTimeout(()=>fish[idx].classList.add('gone'),k*300+500)}},900);
}""",
    },
    # ── frog-hop (addition, number line) ───────────────────────────────
    {
        "slug":"frog-hop","title":"Frog Hop","title_upper":"FROG HOP","title_emoji":"🐸",
        "subtitle":"How far does Froggy hop?","celeb_emoji":"🐸","celeb_title":"HOP CHAMP!",
        "theme_color":"#65a30d","body_grad":"linear-gradient(180deg,#d9f99d 0%,#84cc16 55%,#365314 100%)",
        "text_color":"#365314","title_shadow":"#16a34a","accent":"#bef264",
        "problems":"[{a:1,b:1,op:'+',answer:2},{a:2,b:2,op:'+',answer:4},{a:3,b:2,op:'+',answer:5},{a:4,b:3,op:'+',answer:7},{a:5,b:3,op:'+',answer:8}]",
        "bg_count":10,"bg_emojis":"['🍀','🌿','🦋']","bg_emoji_count":3,
        "scene_css":""".numline-wrap{position:relative;width:min(92vw,460px);margin-top:64px;height:min(34vh,200px);display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:8px}
.frog{font-size:clamp(46px,11vw,58px);filter:drop-shadow(0 3px 6px rgba(0,0,0,0.4));position:relative;z-index:2;transition:transform 1.2s cubic-bezier(0.4,1.6,0.6,1)}
.numline{display:flex;align-items:flex-end;gap:4px;width:100%;justify-content:center;padding-bottom:6px}
.pad{width:30px;height:30px;background:radial-gradient(circle,#86efac,#16a34a);border-radius:50% 50% 45% 45%;display:flex;align-items:center;justify-content:center;font-size:13px;color:#fff;font-weight:900;box-shadow:0 3px 5px rgba(0,0,0,0.3);flex:0 0 auto;border:2px solid #fff}
.pad.active{background:radial-gradient(circle,#fbbf24,#d97706);transform:scale(1.15)}""",
        "scene_html":"""<div class="numline-wrap">
    <div class="frog" id="frog">🐸</div>
    <div class="numline" id="numline"></div>
  </div>""",
        "scene_js":"""function renderScene(p){
  const nl=$('numline');nl.innerHTML='';
  for(let i=0;i<=10;i++){const d=document.createElement('div');d.className='pad';d.textContent=i;d.id='pad'+i;nl.appendChild(d)}
  const frog=$('frog');frog.style.transform='translateX(0)';
  setTimeout(()=>{const padA=document.getElementById('pad'+p.a);if(padA){padA.classList.add('active');
    const lineRect=nl.getBoundingClientRect(),padRect=padA.getBoundingClientRect();
    const offset=padRect.left+padRect.width/2-(lineRect.left+lineRect.width/2);
    frog.style.transform='translateX('+offset+'px)';}},600);
  setTimeout(()=>{const padB=document.getElementById('pad'+(p.a+p.b));if(padB){padB.classList.add('active');
    const lineRect=nl.getBoundingClientRect(),padRect=padB.getBoundingClientRect();
    const offset=padRect.left+padRect.width/2-(lineRect.left+lineRect.width/2);
    frog.style.transform='translateX('+offset+'px)';}},1800);
}""",
    },
    # ── rocket-fuel (subtraction) ──────────────────────────────────────
    {
        "slug":"rocket-fuel","title":"Rocket Fuel","title_upper":"ROCKET FUEL","title_emoji":"🚀",
        "subtitle":"Count the fuel that is left!","celeb_emoji":"🛸","celeb_title":"BLAST OFF!",
        "theme_color":"#4338ca","body_grad":"linear-gradient(180deg,#312e81 0%,#1e1b4b 55%,#020617 100%)",
        "text_color":"#e0e7ff","title_shadow":"#f59e0b","accent":"#a5b4fc",
        "problems":"[{a:4,b:1,op:'-',answer:3},{a:5,b:2,op:'-',answer:3},{a:7,b:3,op:'-',answer:4},{a:8,b:4,op:'-',answer:4},{a:9,b:5,op:'-',answer:4}]",
        "bg_count":24,"bg_emojis":"['⭐','✨','💫','🌟']","bg_emoji_count":4,
        "scene_css":""".launch-pad{position:relative;width:min(88vw,400px);height:min(42vh,280px);margin-top:62px;display:flex;align-items:center;justify-content:center;gap:20px}
.rocket{font-size:clamp(90px,22vw,140px);animation:rocketHover 2s ease-in-out infinite;filter:drop-shadow(0 6px 10px rgba(251,191,36,0.5))}
@keyframes rocketHover{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
.fuel-bar{display:flex;flex-direction:column-reverse;gap:6px}
.fuel-cell{width:36px;height:20px;background:linear-gradient(90deg,#fbbf24,#dc2626);border:3px solid #fff;border-radius:6px;box-shadow:0 3px 5px rgba(0,0,0,0.5),inset 0 0 8px rgba(255,255,255,0.3);transition:opacity 0.5s,transform 0.5s}
.fuel-cell.burned{animation:fuelBurn 0.6s ease forwards}
@keyframes fuelBurn{0%{transform:scale(1)}40%{transform:scale(1.3) translateX(20px);opacity:0.7;filter:brightness(2)}100%{transform:scale(0) translateX(40px);opacity:0}}""",
        "scene_html":"""<div class="launch-pad">
    <div class="rocket">🚀</div>
    <div class="fuel-bar" id="fuelBar"></div>
  </div>""",
        "scene_js":"""function renderScene(p){
  const bar=$('fuelBar');bar.innerHTML='';
  for(let i=0;i<p.a;i++){const c=document.createElement('div');c.className='fuel-cell';bar.appendChild(c)}
  setTimeout(()=>{const cells=[...bar.querySelectorAll('.fuel-cell')];for(let k=0;k<p.b;k++){const idx=cells.length-1-k;if(cells[idx])setTimeout(()=>cells[idx].classList.add('burned'),k*280+400)}},900);
}""",
    },
    # ── snack-bar (mixed add/sub) ──────────────────────────────────────
    {
        "slug":"snack-bar","title":"Snack Bar","title_upper":"SNACK BAR","title_emoji":"🍕",
        "subtitle":"Yummy math — plus and minus!","celeb_emoji":"🍩","celeb_title":"YUM CHAMP!",
        "theme_color":"#ea580c","body_grad":"linear-gradient(180deg,#fed7aa 0%,#f97316 55%,#7c2d12 100%)",
        "text_color":"#7c2d12","title_shadow":"#c2410c","accent":"#fdba74",
        "problems":"[{a:2,b:1,op:'+',answer:3,emo:'🍕'},{a:5,b:2,op:'-',answer:3,emo:'🍩'},{a:3,b:2,op:'+',answer:5,emo:'🍪'},{a:6,b:3,op:'-',answer:3,emo:'🧁'},{a:4,b:3,op:'+',answer:7,emo:'🍓'}]",
        "bg_count":14,"bg_emojis":"['🍕','🍩','🧁','🍪','🍓']","bg_emoji_count":5,
        "scene_css":""".plate{position:relative;width:min(84vw,360px);height:min(36vh,230px);margin-top:62px;background:radial-gradient(circle,#fff,#fcd34d 70%,#d97706 100%);border:6px solid #fff;border-radius:50%;box-shadow:inset 0 -8px 20px rgba(0,0,0,0.2),0 12px 24px rgba(0,0,0,0.3);display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:8px;padding:18px}
.snack{font-size:clamp(34px,8vw,46px);animation:snackPop 0.5s var(--spring);filter:drop-shadow(0 3px 4px rgba(0,0,0,0.4))}
.snack.eaten{animation:snackEat 0.5s ease forwards}
@keyframes snackPop{from{transform:scale(0) rotate(-180deg)}to{transform:scale(1) rotate(0)}}
@keyframes snackEat{0%{transform:scale(1)}50%{transform:scale(1.3) rotate(30deg);opacity:0.6}100%{transform:scale(0) rotate(60deg);opacity:0}}
.snack.added{animation:snackAdd 0.5s var(--spring)}
@keyframes snackAdd{from{transform:translateY(-40px) scale(0)}to{transform:translateY(0) scale(1)}}""",
        "scene_html":"""<div class="plate" id="plate"></div>""",
        "scene_js":"""function renderScene(p){
  const pl=$('plate');pl.innerHTML='';const emo=p.emo||'🍕';
  for(let i=0;i<p.a;i++){const s=document.createElement('span');s.className='snack';s.textContent=emo;s.style.animationDelay=(i*0.07)+'s';pl.appendChild(s)}
  setTimeout(()=>{
    if(p.op==='+'){for(let k=0;k<p.b;k++){setTimeout(()=>{const s=document.createElement('span');s.className='snack added';s.textContent=emo;pl.appendChild(s)},k*280+500)}}
    else{const snacks=[...pl.querySelectorAll('.snack')];for(let k=0;k<p.b;k++){const idx=snacks.length-1-k;if(snacks[idx])setTimeout(()=>snacks[idx].classList.add('eaten'),k*280+500)}}
  },900);
}""",
    },
]

for g in GAMES:
    out = BASE / f"{g['slug']}.html"
    html = TEMPLATE.format(**g)
    out.write_text(html)
    print(f"Wrote {out}")
