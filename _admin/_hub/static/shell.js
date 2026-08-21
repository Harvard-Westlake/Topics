// Tab shell + helpers shared by every tab

window.Shell = (() => {
  const inited = {};

  function show(name) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.toggle('active', b.dataset.tab === name));
    document.querySelectorAll('section.tab').forEach(s => s.classList.toggle('active', s.id === 'tab-' + name));
    localStorage.setItem('hubTab', name);
    if (('#' + name) !== location.hash) history.replaceState(null, '', '#' + name);
    const ns = {courses: window.Courses, schedule: window.Schedule, planner: window.Planner, syllabus: window.Syllabus}[name];
    if (ns && !inited[name]) { inited[name] = true; ns.init(); }
  }

  function init() {
    document.querySelectorAll('.tab-btn').forEach(b => b.onclick = () => show(b.dataset.tab));
    const start = (location.hash || '').replace('#', '') || localStorage.getItem('hubTab') || 'courses';
    show(['courses', 'schedule', 'planner', 'syllabus'].includes(start) ? start : 'courses');
  }

  return {init, show};
})();

// ── Shared helpers ────────────────────────────────────────────────────────────

function esc(s) {
  return String(s == null ? '' : s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// Canvas is reached through hub.hw.com — a branded vanity domain for the
// school's real *.instructure.com backend. User-facing Canvas links should
// go through it; the hub's own API calls (server-side, BASE in server.py)
// are unaffected and keep hitting the backend domain directly.
const CANVAS_WEB = 'https://hub.hw.com';
function canvasCourseUrl(courseId, path) { return CANVAS_WEB + '/courses/' + courseId + (path || ''); }
function canvasLink(url) { return url ? url.replace(/^https?:\/\/[^/]*\.instructure\.com/, CANVAS_WEB) : url; }

function uid() { return 'b' + Date.now().toString(36) + Math.random().toString(36).slice(2, 7); }

function smartRound(n) {
  if (n >= 1000) return Math.round(n / 50) * 50;
  if (n >= 100)  return Math.round(n / 10) * 10;
  if (n >= 50)   return Math.round(n / 5)  * 5;
  return Math.round(n);
}

function fmtDayLabel(unitNum, a) {
  const dur = a.duration || 1;
  const base = unitNum + '.' + a.day;
  return dur > 1 ? base + ' · ' + dur + 'd' : base;
}

function timeAgo(ts) {
  if (!ts) return '';
  const s = Math.floor(Date.now() / 1000 - ts);
  if (s < 60)    return 'just now';
  if (s < 3600)  return Math.floor(s / 60) + 'm ago';
  if (s < 86400) return Math.floor(s / 3600) + 'h ago';
  return Math.floor(s / 86400) + 'd ago';
}

function fmtD(iso) {
  if (!iso) return '…';
  return new Date(iso + 'T12:00:00').toLocaleDateString('en-US', {weekday:'short', month:'short', day:'numeric'});
}

function fmtShort(iso) {
  if (!iso) return '…';
  return new Date(iso + 'T12:00:00').toLocaleDateString('en-US', {month:'short', day:'numeric'});
}

let __toastTimer = null;
function toast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.style.display = 'block';
  clearTimeout(__toastTimer);
  __toastTimer = setTimeout(() => t.style.display = 'none', 2200);
}
