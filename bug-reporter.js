(function () {
  if (window.__ahaBugReporter) return;
  window.__ahaBugReporter = true;

  var STORAGE_KEY = 'aha_bug_reports';

  function getGameName() {
    var path = (location.pathname || '').split('/').filter(Boolean).pop() || '';
    var file = path.replace(/\.html?$/i, '');
    if (file && file !== 'index') return file;
    var t = (document.title || '').trim();
    return t || file || 'unknown';
  }

  function getRound() {
    var candidates = ['currentRound', 'gameRound', 'round', 'roundNum', 'roundNumber', 'level', 'currentLevel'];
    for (var i = 0; i < candidates.length; i++) {
      var v = window[candidates[i]];
      if (typeof v === 'number' || typeof v === 'string') return v;
    }
    return null;
  }

  function loadReports() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return [];
      var parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed : [];
    } catch (e) { return []; }
  }

  function saveReport(report) {
    var all = loadReports();
    all.push(report);
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(all)); } catch (e) {}
  }

  var css = ''
    + '#ahaBugBtn{position:fixed;left:10px;bottom:10px;z-index:2147483600;width:34px;height:34px;border-radius:50%;border:none;'
    + 'background:rgba(0,0,0,0.55);color:#fff;font-size:16px;line-height:34px;text-align:center;cursor:pointer;padding:0;'
    + '-webkit-tap-highlight-color:transparent;backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);opacity:0.55;'
    + 'transition:opacity .15s,transform .15s;box-shadow:0 2px 6px rgba(0,0,0,0.3)}'
    + '#ahaBugBtn:hover,#ahaBugBtn:active{opacity:1;transform:scale(1.08)}'
    + '#ahaBugOverlay{position:fixed;inset:0;z-index:2147483601;background:rgba(0,0,0,0.75);display:none;'
    + 'align-items:center;justify-content:center;padding:20px;font-family:"Arial Rounded MT Bold","Nunito","Quicksand",system-ui,-apple-system,Arial,sans-serif}'
    + '#ahaBugOverlay.active{display:flex}'
    + '#ahaBugCard{background:#141833;color:#fff;border-radius:14px;padding:20px;width:100%;max-width:380px;'
    + 'box-shadow:0 10px 40px rgba(0,0,0,0.5);position:relative}'
    + '#ahaBugCard h3{margin:0 0 12px;font-size:17px;font-weight:700}'
    + '#ahaBugMeta{font-size:11px;color:#8a8fb5;margin-bottom:12px;line-height:1.4;word-break:break-word}'
    + '#ahaBugInput{width:100%;min-height:80px;padding:10px;border-radius:8px;border:1px solid #2a2f55;'
    + 'background:#0b0e24;color:#fff;font-family:inherit;font-size:14px;resize:vertical;box-sizing:border-box}'
    + '#ahaBugInput:focus{outline:none;border-color:#4a5bd6}'
    + '#ahaBugRow{display:flex;gap:8px;margin-top:12px}'
    + '#ahaBugSend{flex:1;background:#4a5bd6;color:#fff;border:none;border-radius:8px;padding:11px;font-size:14px;'
    + 'font-weight:700;cursor:pointer;font-family:inherit}'
    + '#ahaBugSend:active{background:#3a4ab0}'
    + '#ahaBugClose{position:absolute;top:8px;right:10px;background:none;border:none;color:#8a8fb5;font-size:22px;'
    + 'cursor:pointer;line-height:1;padding:4px 8px;font-family:inherit}'
    + '#ahaBugClose:hover{color:#fff}'
    + '#ahaBugToast{position:fixed;left:50%;bottom:80px;transform:translateX(-50%);z-index:2147483602;'
    + 'background:rgba(20,150,80,0.95);color:#fff;padding:10px 18px;border-radius:22px;font-size:14px;'
    + 'font-family:inherit;font-weight:700;opacity:0;transition:opacity .2s;pointer-events:none}'
    + '#ahaBugToast.show{opacity:1}';

  function inject() {
    var style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);

    var btn = document.createElement('button');
    btn.id = 'ahaBugBtn';
    btn.type = 'button';
    btn.setAttribute('aria-label', 'Report a bug');
    btn.textContent = '🐛';

    var overlay = document.createElement('div');
    overlay.id = 'ahaBugOverlay';
    overlay.innerHTML = ''
      + '<div id="ahaBugCard" role="dialog" aria-label="Report a bug">'
      + '  <button id="ahaBugClose" type="button" aria-label="Close">&times;</button>'
      + '  <h3>What went wrong?</h3>'
      + '  <div id="ahaBugMeta"></div>'
      + '  <textarea id="ahaBugInput" placeholder="Optional — describe what happened"></textarea>'
      + '  <div id="ahaBugRow"><button id="ahaBugSend" type="button">Send Report</button></div>'
      + '</div>';

    var toast = document.createElement('div');
    toast.id = 'ahaBugToast';
    toast.textContent = '✓ Logged!';

    document.body.appendChild(btn);
    document.body.appendChild(overlay);
    document.body.appendChild(toast);

    function show() {
      var game = getGameName();
      var round = getRound();
      var metaParts = ['Game: ' + game];
      if (round !== null) metaParts.push('Round: ' + round);
      document.getElementById('ahaBugMeta').textContent = metaParts.join(' · ');
      document.getElementById('ahaBugInput').value = '';
      overlay.classList.add('active');
      setTimeout(function () {
        var input = document.getElementById('ahaBugInput');
        if (input) try { input.focus(); } catch (e) {}
      }, 50);
    }
    function hide() { overlay.classList.remove('active'); }

    function showToast() {
      toast.classList.add('show');
      setTimeout(function () { toast.classList.remove('show'); }, 1400);
    }

    btn.addEventListener('click', show);
    document.getElementById('ahaBugClose').addEventListener('click', hide);
    overlay.addEventListener('click', function (e) { if (e.target === overlay) hide(); });

    document.getElementById('ahaBugSend').addEventListener('click', function () {
      var desc = document.getElementById('ahaBugInput').value.trim();
      var report = {
        game: getGameName(),
        url: location.href,
        round: getRound(),
        timestamp: new Date().toISOString(),
        description: desc,
        userAgent: navigator.userAgent
      };
      saveReport(report);
      hide();
      showToast();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inject);
  } else {
    inject();
  }
})();
