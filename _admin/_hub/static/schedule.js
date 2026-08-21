// Year Schedule tab — per-teacher drag-and-drop year plans (_admin/_schedules/<name>.json)

window.Schedule = (() => {

let schedName = null;        // active schedule file (one per teacher)
let schedList = [];
let schedule = null;         // editable model
let resolved = null;         // last server resolution (dates, expanded lessons)
let calendar = null;         // imported .ics class calendar bound to this schedule
let calName = null;
let savedModules = [], topicList = [], finalsInfo = {available: false, finals: []};
let topicLessons = {};       // topic name -> lessons (palette expansion)
let expandedBlocks = new Set();
let expandedTopics = new Set();
let courses = null, favoriteIds = new Set();
let saveTimer = null;
let editingFinal = null;
let syncBlockId = null;
let dndAttached = false;

const DOW = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
const DAY_TYPES = [
  {kind: 'test',   title: 'Test Day',   cls: 'kb-test'},
  {kind: 'review', title: 'Review Day', cls: 'kb-review'},
  {kind: 'flex',   title: 'Flex Day',   cls: 'kb-flex'},
  {kind: 'custom', title: 'Custom Day', cls: 'kb-custom'},
];

function drag(payload) { return 'draggable="true" data-drag="' + encodeURIComponent(JSON.stringify(payload)) + '"'; }

function setPill(state) {
  const labels = {saved: 'Saved', saving: 'Saving…', error: 'Save failed'};
  const pill = document.getElementById('savePill');
  pill.className = 'status-pill ' + state;
  pill.innerHTML = '<div class="dot"></div>' + labels[state];
}

function blockById(id)   { return schedule.sequence.find(b => b.id === id); }
function resolvedById(id){ return ((resolved && resolved.blocks) || []).find(b => b.id === id); }

// ── Load / save ───────────────────────────────────────────────────────────────

async function init() {
  attachDnd();
  const d = await fetch('/api/schedules').then(r => r.json());
  schedList = d.schedules || [];
  const last = localStorage.getItem('schedName');
  schedName = schedList.some(s => s.name === last) ? last
            : (schedList[0] ? schedList[0].name : null);
  renderSchedPicker();
  if (schedName) await loadSchedule(schedName);
  else {
    document.getElementById('board').innerHTML =
      '<div class="board-empty">No schedules yet — click “+ New” above to create yours<br>(one schedule file per teacher).</div>';
  }
  loadPalette();
}

function renderSchedPicker() {
  const sel = document.getElementById('schedPick');
  sel.innerHTML = '';
  schedList.forEach(s => {
    const o = document.createElement('option');
    o.value = s.name;
    o.textContent = s.name + (s.year ? ' (' + s.year + ')' : '');
    if (s.name === schedName) o.selected = true;
    sel.appendChild(o);
  });
}

async function loadSchedule(name) {
  schedName = name;
  localStorage.setItem('schedName', name);
  const d = await fetch('/api/schedules/' + encodeURIComponent(name)).then(r => r.json());
  schedule = d.schedule;
  resolved = d.resolved;
  schedule.sequence.forEach(b => { if (!b.id) b.id = uid(); });
  await loadCalendar();
  renderSettings();
  renderNoSchool();
  renderBoard();
  renderSummary();
  renderWarnings();
  renderCalInfo();
  setPill('saved');
}

async function loadCalendar() {
  calName = schedule.calendar || schedName;
  calendar = null;
  if (!calName) return;
  const d = await fetch('/api/calendars/' + encodeURIComponent(calName))
    .then(r => r.ok ? r.json() : null).catch(() => null);
  if (d && d.calendar) calendar = d.calendar;
}

function pickSchedule(name) {
  if (name) loadSchedule(name);
}

async function newSchedule() {
  const name = prompt('Schedule name — e.g. your last name, or lastname-2027-28 for a new year:');
  if (!name) return;
  if (!/^[A-Za-z0-9][A-Za-z0-9 _\-]*$/.test(name)) { toast('Letters, numbers, - and _ only'); return; }
  if (schedList.some(s => s.name === name)) { toast('A schedule named “' + name + '” already exists'); return; }
  let body = {
    year: '2026-27',
    start_date: '2026-08-26',
    end_date: '2027-06-04',
    meeting_days: [0, 1, 2, 3, 4],
    no_school: [],
    sequence: [],
  };
  // Year rollover: the plan (sequence) is date-free, so copying it into a new
  // schedule and setting the new year's calendar re-dates the whole year.
  const blocks = schedule ? (schedule.sequence || []).length : 0;
  if (blocks && confirm('Copy the current plan from “' + schedName + '” (' + blocks +
      ' block' + (blocks !== 1 ? 's' : '') + ') into “' + name + '”?\n\n' +
      'OK = carry the plan over (then just set the new year’s dates and no-school days).\n' +
      'Cancel = start “' + name + '” empty.')) {
    body = JSON.parse(JSON.stringify(schedule));
  }
  await fetch('/api/schedules/' + encodeURIComponent(name), {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(body),
  });
  const d = await fetch('/api/schedules').then(r => r.json());
  schedList = d.schedules || [];
  schedName = name;
  renderSchedPicker();
  await loadSchedule(name);
}

function markDirty() {
  renderBoard();
  setPill('saving');
  clearTimeout(saveTimer);
  saveTimer = setTimeout(doSave, 400);
}

async function doSave() {
  if (!schedName) return;
  try {
    const d = await fetch('/api/schedules/' + encodeURIComponent(schedName), {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(schedule),
    }).then(r => r.json());
    if (d.error) throw new Error(d.error);
    resolved = d.resolved;
    setPill('saved');
    renderBoard();
    renderSummary();
    renderWarnings();
    renderCalInfo();
  } catch (e) {
    setPill('error');
  }
}

// ── Settings ──────────────────────────────────────────────────────────────────

function renderSettings() {
  document.getElementById('setYear').value  = schedule.year || '';
  document.getElementById('setStart').value = schedule.start_date || '';
  document.getElementById('setEnd').value   = schedule.end_date || '';
  document.getElementById('setYear').onchange  = e => { schedule.year = e.target.value; markDirty(); };
  document.getElementById('setStart').onchange = e => { schedule.start_date = e.target.value; markDirty(); };
  document.getElementById('setEnd').onchange   = e => { schedule.end_date = e.target.value; markDirty(); };
  const g = document.getElementById('dowGroup');
  g.innerHTML = [0,1,2,3,4].map(d =>
    '<button class="dow-btn' + ((schedule.meeting_days || []).includes(d) ? ' active' : '') + '"' +
    ' onclick="Schedule.toggleDow(' + d + ')">' + DOW[d] + '</button>').join('');
  renderCalClassPicker();
}

// ── Class calendar (imported .ics) ────────────────────────────────────────────
// The calendar is the compressed copy of a Didax teacher-schedule export.
// Binding a class replaces the weekday grid with the class's real meeting
// dates; the grid controls hide because they no longer apply.

function classLabel(c) {
  if (c.block && c.course) return 'Block ' + c.block + ' — ' + c.course;
  if (c.block) return 'Block ' + c.block + ' (free block)';
  return c.course || c.id;
}

function renderCalClassPicker() {
  const sel = document.getElementById('calClass');
  const bound = !!(schedule.calendar_class && calendar &&
                   calendar.classes.some(c => c.id === schedule.calendar_class));
  let opts = '<option value="">' +
    (calendar ? 'Manual (weekday grid)' : 'Manual — import an .ics for real dates') +
    '</option>';
  if (calendar) {
    opts += calendar.classes.map(c =>
      '<option value="' + esc(c.id) + '"' +
      (schedule.calendar_class === c.id ? ' selected' : '') + '>' +
      esc(classLabel(c)) + '</option>').join('');
  }
  sel.innerHTML = opts;
  sel.disabled = !calendar;
  document.getElementById('dowLabel').style.display = bound ? 'none' : '';
  document.getElementById('dowGroup').style.display = bound ? 'none' : '';
}

function pickCalClass(id) {
  if (!id) {
    delete schedule.calendar_class;
  } else {
    const cls = calendar.classes.find(c => c.id === id);
    schedule.calendar = calName;
    schedule.calendar_class = id;
    // Cover the class's whole span; narrow First/Last day to start a plan
    // at any later meeting instead.
    if (cls && cls.meetings.length) {
      schedule.start_date = cls.meetings[0][0];
      schedule.end_date = cls.meetings[cls.meetings.length - 1][0];
    }
  }
  renderSettings();
  markDirty();
}

async function importIcs(input) {
  const file = input.files && input.files[0];
  input.value = '';
  if (!file || !schedName) return;
  const text = await file.text();
  // One calendar per schedule name: a new year's schedule gets its own
  // calendar file, so re-importing never re-dates an older year's plan.
  const name = schedName;
  const d = await fetch('/api/calendars/' + encodeURIComponent(name) +
      '/import?filename=' + encodeURIComponent(file.name), {
    method: 'POST', headers: {'Content-Type': 'text/calendar'}, body: text,
  }).then(r => r.json()).catch(e => ({error: String(e)}));
  if (d.error) { toast(d.error); return; }
  calendar = d.calendar;
  calName = name;
  schedule.calendar = name;
  const withCourse = calendar.classes.filter(c => c.course).length;
  toast('Imported ' + calendar.classes.length + ' class slots (' + withCourse +
        ' with courses) — pick your class');
  renderSettings();
  renderCalInfo();
  markDirty();
}

function renderCalInfo() {
  const el = document.getElementById('calInfo');
  const cls = resolved && resolved.calendar && resolved.calendar.class;
  if (cls) {
    el.style.display = '';
    el.innerHTML = 'Dates from imported calendar: <b style="color:var(--text)">' +
      esc(classLabel(cls)) + '</b>' +
      (cls.location ? ' &middot; ' + esc(cls.location) : '') +
      ' &middot; ' + cls.meetings + ' meetings ' + fmtShort(cls.first) + ' &ndash; ' +
      fmtShort(cls.last) +
      ' &middot; Canvas sync unlocks at class start; homework due 11:59 PM before the next class';
  } else if (calendar) {
    el.style.display = '';
    el.innerHTML = 'Calendar &ldquo;' + esc(calName) + '&rdquo; imported (' +
      calendar.classes.length + ' class slots) — pick a class above to use real meeting dates.';
  } else {
    el.style.display = 'none';
  }
}

function toggleDow(d) {
  const days = new Set(schedule.meeting_days || []);
  if (days.has(d)) days.delete(d); else days.add(d);
  schedule.meeting_days = [...days].sort();
  renderSettings();
  markDirty();
}

function toggleNoSchool() {
  document.getElementById('nsRow').classList.toggle('open');
}

function renderNoSchool() {
  const list = schedule.no_school || [];
  document.getElementById('nsToggle').textContent = 'No-school days (' + list.length + ')';
  document.getElementById('nsChips').innerHTML = list.map((n, i) => {
    const d = typeof n === 'string' ? {date: n} : n;
    return '<span class="ns-chip">' + fmtShort(d.date) +
      (d.label ? ' <span style="color:var(--muted)">— ' + esc(d.label) + '</span>' : '') +
      '<span class="x" onclick="Schedule.removeNoSchool(' + i + ')">&#x2715;</span></span>';
  }).join('');
}

function addNoSchool() {
  const date = document.getElementById('nsDate').value;
  if (!date) return;
  const label = document.getElementById('nsLabel').value.trim();
  schedule.no_school = schedule.no_school || [];
  schedule.no_school.push(label ? {date, label} : {date});
  schedule.no_school.sort((a, b) => (a.date || a) < (b.date || b) ? -1 : 1);
  document.getElementById('nsDate').value = '';
  document.getElementById('nsLabel').value = '';
  renderNoSchool();
  markDirty();
}

function removeNoSchool(i) {
  schedule.no_school.splice(i, 1);
  renderNoSchool();
  markDirty();
}

function renderSummary() {
  const c = resolved && resolved.calendar;
  if (!c) { document.getElementById('summary').innerHTML = ''; return; }
  const free = c.remaining;
  document.getElementById('summary').innerHTML =
    '<b>' + c.total + '</b> class days &middot; <b>' + c.used + '</b> scheduled &middot; ' +
    (free < 0 ? '<span class="over">' + (-free) + ' over!</span>'
              : '<b>' + free + '</b> free');
}

function renderWarnings() {
  const w = (resolved && resolved.warnings) || [];
  document.getElementById('warnings').innerHTML =
    w.map(x => '<div class="warn">&#9888; ' + esc(x) + '</div>').join('');
}

// ── Palette ───────────────────────────────────────────────────────────────────

async function loadPalette() {
  const [saved, topics, finals] = await Promise.all([
    fetch('/api/github/saved-modules').then(r => r.json()).catch(() => ({modules: []})),
    fetch('/api/github/modules').then(r => r.json()).catch(() => ({modules: []})),
    fetch('/api/finals').then(r => r.json()).catch(() => ({available: false, finals: []})),
  ]);
  savedModules = saved.modules || [];
  topicList    = topics.modules || [];
  finalsInfo   = finals;
  topicLessons = {};
  renderPalette();
  // A module already placed on the board may have changed since this schedule
  // was loaded (e.g. edited in the Planner tab) — re-resolve it too, not just
  // the drag-source list, so the board's dates/points/lesson counts catch up.
  if (schedName) {
    const d = await fetch('/api/schedules/' + encodeURIComponent(schedName)).then(r => r.json());
    resolved = d.resolved;
    renderBoard();
    renderSummary();
    renderWarnings();
  }
}

function renderPalette() {
  document.getElementById('palSaved').innerHTML = savedModules.length ? savedModules.map(m =>
    '<div class="pal-item" ' + drag({src:'palette', kind:'saved', slug:m.slug}) + '>' +
      '<span class="grip">&#x2630;</span>' +
      '<span class="name">' + esc(m.name) + '</span>' +
      '<span class="meta">' + m.days + 'd</span>' +
    '</div>').join('')
    : '<div class="pal-note">None yet — build one in the Module Planner tab</div>';

  document.getElementById('palTopics').innerHTML = topicList.map(name =>
    '<div>' +
      '<div class="pal-item" ' + drag({src:'palette', kind:'topic', name}) + '>' +
        '<span class="caret' + (expandedTopics.has(name) ? ' open' : '') + '" onclick="Schedule.toggleTopic(event, \'' + name + '\')">&#9656;</span>' +
        '<span class="name">' + esc(name) + '</span>' +
      '</div>' +
      (expandedTopics.has(name) ? '<div class="pal-sub" id="tsub_' + name + '">' + topicSubHtml(name) + '</div>' : '') +
    '</div>').join('');

  const finalsEl = document.getElementById('palFinals');
  document.getElementById('palFinalsNew').style.display = finalsInfo.available ? 'inline' : 'none';
  if (!finalsInfo.available) {
    finalsEl.innerHTML = '<div class="pal-note">Private Admin repo not found — clone it as a sibling ' +
      'of this repo (or set FINALS_DIR in .env) to manage finals.</div>';
  } else {
    finalsEl.innerHTML = (finalsInfo.finals.length ? finalsInfo.finals.map(f =>
      '<div class="pal-item" ' + drag({src:'palette', kind:'final', file:f.file, name:f.name, title:f.title}) + '>' +
        '<span class="grip">&#x2630;</span>' +
        '<span class="kb kb-final">Final</span>' +
        '<span class="name" title="' + esc(f.title) + '">' + esc(f.name) + '</span>' +
        '<span class="edit-btn" style="margin-left:auto" onclick="Schedule.openFinalEditor(event, \'' + esc(f.name) + '\')">&#9998;</span>' +
      '</div>').join('')
      : '<div class="pal-note">No finals yet — click “+ new”</div>');
  }

  document.getElementById('palDays').innerHTML = DAY_TYPES.map(t =>
    '<div class="pal-item" ' + drag({src:'palette', kind:t.kind}) + '>' +
      '<span class="grip">&#x2630;</span>' +
      '<span class="kb ' + t.cls + '">' + t.kind + '</span>' +
      '<span class="name">' + t.title + '</span>' +
    '</div>').join('');
}

function topicSubHtml(name) {
  const lessons = topicLessons[name];
  if (!lessons) return '<div class="pal-note" style="font-size:11px">Loading…</div>';
  return lessons.map(a =>
    '<div class="pal-item" ' + drag({src:'palette', kind:'lesson', module:name, path:a.path, title:a.title}) + '>' +
      '<span class="day">' + a.day + (a.duration > 1 ? '–' + (a.day + a.duration - 1) : '') + '</span>' +
      '<span class="name" title="' + esc(a.title) + '">' + esc(a.title) + '</span>' +
    '</div>').join('');
}

async function toggleTopic(e, name) {
  e.stopPropagation();
  if (expandedTopics.has(name)) expandedTopics.delete(name);
  else expandedTopics.add(name);
  renderPalette();
  if (expandedTopics.has(name) && !topicLessons[name]) {
    const d = await fetch('/api/github/modules/' + encodeURIComponent(name)).then(r => r.json());
    topicLessons[name] = d.assignments || [];
    const sub = document.getElementById('tsub_' + name);
    if (sub) sub.innerHTML = topicSubHtml(name);
  }
}

// ── Board ─────────────────────────────────────────────────────────────────────

function renderBoard() {
  const board = document.getElementById('board');
  if (!schedule) return;
  if (!schedule.sequence.length) {
    board.innerHTML = dz(0) +
      '<div class="board-empty">Drag saved modules, topics, finals, and day types here to build the year.<br>' +
      'Drop items <i>inside</i> an expanded module to add test days or extra lessons mid-unit.</div>';
    return;
  }
  let html = dz(0), unit = 0;
  schedule.sequence.forEach((blk, i) => {
    if (blk.type === 'module') { html += moduleCard(blk, unit); unit++; }
    else html += standaloneCard(blk);
    html += dz(i + 1);
  });
  board.innerHTML = html;
}

function dz(i) {
  return '<div class="dz" data-dz="' + i + '"><div class="line"></div></div>';
}

function idz(blockId, afterDay, insId) {
  return '<div class="idz" data-block="' + blockId + '" data-after="' + afterDay + '"' +
         (insId ? ' data-ins="' + insId + '"' : '') + '><div class="line"></div></div>';
}

function moduleCard(blk, unit) {
  const r = resolvedById(blk.id);
  const open = expandedBlocks.has(blk.id);
  const name = r ? r.name : blk.ref;
  const dates = r && r.start ? fmtShort(r.start) + ' – ' + fmtShort(r.end) + ' &middot; ' + r.days + 'd'
              : (r && r.days === 0 && r.missing ? '' : '…');
  let html =
    '<div class="block b-module" id="blk_' + blk.id + '">' +
      '<div class="block-head" ' + drag({src:'board', id:blk.id}) + '>' +
        '<span class="grip">&#x2630;</span>' +
        '<span class="caret' + (open ? ' open' : '') + '" onclick="Schedule.toggleBlock(\'' + blk.id + '\')">&#9656;</span>' +
        '<span class="block-title"><span class="unit">Unit ' + unit + ':</span> ' + esc(name) + '</span>' +
        '<span class="src-badge">' + (blk.source === 'topic' ? 'topic' : 'saved') + '</span>' +
        '<span class="block-dates">' + dates + '</span>' +
        '<span class="block-actions">' +
          (r && !r.missing ? '<button class="mini-btn sync" onclick="Schedule.openSync(\'' + blk.id + '\')">Sync</button>' : '') +
          '<button class="x-btn" onclick="Schedule.removeBlock(\'' + blk.id + '\')">&#x2715;</button>' +
        '</span>' +
      '</div>';
  if (r && r.missing) {
    html += '<div class="missing-note">&#9888; “' + esc(blk.ref) + '” no longer exists in the repo.</div>';
  } else if (open) {
    html += '<div class="block-body">' + moduleRows(blk, r) + '</div>';
  }
  return html + '</div>';
}

function moduleRows(blk, r) {
  if (!r) return '<div style="padding:10px 16px;color:var(--muted);font-size:12px">Resolving…</div>';
  let html = idz(blk.id, 0, null);
  const seenParts = {};
  r.slots.forEach((s, i) => {
    html += slotRow(blk, s, s.day_num || i + 1);
    const next = r.slots[i + 1];
    if (next && next.co_day) return;   // more lessons share this class day — zone after the last one
    if (s.insert_id) {
      // zone only after the last day of a multi-day insert
      seenParts[s.insert_id] = (seenParts[s.insert_id] || 0) + 1;
      if (seenParts[s.insert_id] === s.parts) html += idz(blk.id, findAfterDay(r, i), s.insert_id);
    } else {
      html += idz(blk.id, s.module_day || 0, null);
    }
  });
  return html;
}

function findAfterDay(r, i) {
  // module_day of the nearest lesson/gap slot at or before index i (0 if none)
  for (let k = i; k >= 0; k--) {
    if (r.slots[k].module_day) return r.slots[k].module_day;
  }
  return 0;
}

function slotRow(blk, s, num) {
  const isInsert = !!s.insert_id;
  const later = (s.part || 1) > 1;
  let controls = '';
  if (isInsert && !later) {
    const ins = (blk.inserts || []).find(x => x.id === s.insert_id) || {};
    controls =
      '<span class="stepper"><button onclick="Schedule.stepInsert(\'' + blk.id + '\',\'' + s.insert_id + '\',-1)">&minus;</button>' +
      '<span class="n">' + (ins.days || 1) + 'd</span>' +
      '<button onclick="Schedule.stepInsert(\'' + blk.id + '\',\'' + s.insert_id + '\',1)">+</button></span>' +
      (s.kind === 'test' || s.kind === 'final'
        ? '<input class="pts-input" type="number" value="' + (ins.points || 100) + '" title="Points"' +
          ' onchange="Schedule.setInsertPoints(\'' + blk.id + '\',\'' + s.insert_id + '\',this.value)">'
        : '') +
      '<span class="grip" ' + drag({src:'insert', blockId:blk.id, insertId:s.insert_id}) + '>&#x2630;</span>' +
      '<button class="x-btn" onclick="Schedule.removeInsert(\'' + blk.id + '\',\'' + s.insert_id + '\')">&#x2715;</button>';
  }
  const badge = s.kind === 'lesson' && !isInsert ? ''
    : '<span class="kb kb-' + s.kind + '">' + s.kind + '</span>';
  const titleAttr = isInsert && !later && s.kind !== 'lesson'
    ? ' class="slot-title editable" onclick="Schedule.editInsertTitle(this,\'' + blk.id + '\',\'' + s.insert_id + '\')"'
    : ' class="slot-title' + (s.kind === 'gap' ? ' gap' : '') + '"';
  const from = s.lesson && s.lesson._module ? ' <span class="from">' + esc(s.lesson._module) + '/' + esc(s.lesson.path || '') + '</span>'
    : (s.lesson_ref ? ' <span class="from">' + esc(s.lesson_ref.module) + '/' + esc(s.lesson_ref.path) + '</span>' : '');
  const timeTip = s.time
    ? ' title="Class ' + s.time.start + '–' + s.time.end +
      (s.next_date ? ' · HW due 11:59 PM the night before ' + fmtShort(s.next_date) : '') + '"'
    : '';
  return '<div class="slot-row' + (isInsert ? ' ins' : '') + '">' +
    '<span class="slot-date"' + timeTip + '>' + fmtD(s.date) + '</span>' +
    '<span class="slot-num">' + num + '</span>' +
    '<span>' + badge + '</span>' +
    '<span' + titleAttr + '>' + esc(s.title) + from + '</span>' +
    '<span class="slot-controls">' + controls + '</span>' +
  '</div>';
}

function standaloneCard(blk) {
  const r = resolvedById(blk.id);
  const kind = blk.type;
  const title = (r && r.slots && r.slots[0] && r.slots[0].base_title) || blk.title || kind;
  const dates = r && r.start
    ? (r.days > 1 ? fmtShort(r.start) + ' – ' + fmtShort(r.end) + ' &middot; ' + r.days + 'd' : fmtD(r.start))
    : '…';
  const editable = kind !== 'lesson';
  const syncable = kind === 'test' || kind === 'final' || kind === 'lesson';
  return '<div class="block b-' + kind + '" id="blk_' + blk.id + '">' +
    '<div class="block-head" ' + drag({src:'board', id:blk.id}) + '>' +
      '<span class="grip">&#x2630;</span>' +
      '<span class="kb kb-' + kind + '">' + kind + '</span>' +
      '<span class="block-title' + (editable ? ' editable" onclick="Schedule.editBlockTitle(this,\'' + blk.id + '\')"' : '"') + '>' + esc(title) + '</span>' +
      (kind === 'final' && blk.file ? '<span class="src-badge">' + esc(blk.file) + '</span>' : '') +
      (blk.module ? '<span class="src-badge">' + esc(blk.module) + '/' + esc(blk.path) + '</span>' : '') +
      '<span class="block-dates">' + dates + '</span>' +
      '<span class="block-actions">' +
        '<span class="stepper"><button onclick="Schedule.stepBlock(\'' + blk.id + '\',-1)">&minus;</button>' +
        '<span class="n">' + (blk.days || 1) + 'd</span>' +
        '<button onclick="Schedule.stepBlock(\'' + blk.id + '\',1)">+</button></span>' +
        (kind === 'test' || kind === 'final'
          ? '<input class="pts-input" type="number" value="' + (blk.points || 100) + '" title="Points"' +
            ' onchange="Schedule.setBlockPoints(\'' + blk.id + '\',this.value)">'
          : '') +
        (syncable ? '<button class="mini-btn sync" onclick="Schedule.openSync(\'' + blk.id + '\')">Sync</button>' : '') +
        '<button class="x-btn" onclick="Schedule.removeBlock(\'' + blk.id + '\')">&#x2715;</button>' +
      '</span>' +
    '</div>' +
  '</div>';
}

function toggleBlock(id) {
  if (expandedBlocks.has(id)) expandedBlocks.delete(id);
  else expandedBlocks.add(id);
  renderBoard();
}

// ── Mutations ─────────────────────────────────────────────────────────────────

function removeBlock(id) {
  const blk = blockById(id);
  if (!blk) return;
  if (blk.type === 'module' && !confirm('Remove this module from the schedule? (The repo content is untouched.)')) return;
  schedule.sequence = schedule.sequence.filter(b => b.id !== id);
  markDirty();
}

function stepBlock(id, delta) {
  const blk = blockById(id);
  blk.days = Math.max(1, (blk.days || 1) + delta);
  markDirty();
}

function setBlockPoints(id, v) {
  blockById(id).points = parseInt(v) || 0;
  markDirty();
}

function removeInsert(blockId, insId) {
  const blk = blockById(blockId);
  blk.inserts = (blk.inserts || []).filter(x => x.id !== insId);
  markDirty();
}

function stepInsert(blockId, insId, delta) {
  const ins = (blockById(blockId).inserts || []).find(x => x.id === insId);
  if (!ins) return;
  ins.days = Math.max(1, (ins.days || 1) + delta);
  markDirty();
}

function setInsertPoints(blockId, insId, v) {
  const ins = (blockById(blockId).inserts || []).find(x => x.id === insId);
  if (ins) { ins.points = parseInt(v) || 0; markDirty(); }
}

function editBlockTitle(el, id) {
  swapToInput(el, blockById(id).title || '', v => { blockById(id).title = v; });
}

function editInsertTitle(el, blockId, insId) {
  const ins = (blockById(blockId).inserts || []).find(x => x.id === insId);
  if (!ins) return;
  swapToInput(el, ins.title || '', v => { ins.title = v; });
}

function swapToInput(el, current, commit) {
  const input = document.createElement('input');
  input.className = 'edit-input';
  input.value = current;
  el.replaceWith(input);
  input.focus();
  input.select();
  let done = false;
  const finish = ok => {
    if (done) return;
    done = true;
    if (ok && input.value.trim()) commit(input.value.trim());
    markDirty();
  };
  input.onkeydown = e => {
    if (e.key === 'Enter') finish(true);
    if (e.key === 'Escape') finish(false);
  };
  input.onblur = () => finish(true);
}

// ── Drag & drop ───────────────────────────────────────────────────────────────

let hoverZone = null;

function zoneAt(e) {
  // A drop anywhere on the board lands in the nearest zone — the thin lines are
  // the visual cue, not the only target a human has to hit.
  const direct = e.target.closest && e.target.closest('.dz, .idz');
  if (direct) return direct;
  const board = e.target.closest && e.target.closest('.board');
  if (!board) return null;
  // inside an expanded module's rows → nearest insert zone in that module;
  // anywhere else on the board → nearest between-block zone
  const body = e.target.closest('.block-body');
  const pool = body ? body.querySelectorAll('.idz') : board.querySelectorAll('.dz');
  let best = null, bestDist = Infinity;
  for (const z of pool) {
    const r = z.getBoundingClientRect();
    const d = Math.abs(e.clientY - (r.top + r.height / 2));
    if (d < bestDist) { bestDist = d; best = z; }
  }
  return best;
}

function clearHover() {
  if (hoverZone) { hoverZone.classList.remove('over'); hoverZone = null; }
}

function attachDnd() {
  if (dndAttached) return;
  dndAttached = true;

  document.addEventListener('dragstart', e => {
    const el = e.target.closest && e.target.closest('[data-drag]');
    if (!el) return;
    e.dataTransfer.setData('text/plain', el.dataset.drag);
    e.dataTransfer.effectAllowed = 'move';
  });

  document.addEventListener('dragover', e => {
    const z = zoneAt(e);
    if (!z) { clearHover(); return; }
    e.preventDefault();
    if (hoverZone !== z) {
      clearHover();
      hoverZone = z;
      z.classList.add('over');
    }
  });

  document.addEventListener('dragend', clearHover);

  document.addEventListener('drop', e => {
    const z = zoneAt(e);
    clearHover();
    if (!z) return;
    e.preventDefault();
    let p;
    try { p = JSON.parse(decodeURIComponent(e.dataTransfer.getData('text/plain'))); }
    catch { return; }
    if (z.classList.contains('dz')) dropAtBoard(parseInt(z.dataset.dz), p);
    else dropAtInsert(z.dataset.block, parseInt(z.dataset.after), z.dataset.ins || null, p);
  });
}

function newBlockFromPalette(p) {
  switch (p.kind) {
    case 'saved':  return {id: uid(), type: 'module', source: 'saved', ref: p.slug, inserts: []};
    case 'topic':  return {id: uid(), type: 'module', source: 'topic', ref: p.name, inserts: []};
    case 'lesson': return {id: uid(), type: 'lesson', module: p.module, path: p.path, title: p.title, days: 1, points: 10};
    case 'final':  return {id: uid(), type: 'final', file: p.file, title: p.title || (p.name + ' Final'), days: 1, points: 100};
    case 'test':   return {id: uid(), type: 'test', title: 'Test', days: 1, points: 100};
    case 'review': return {id: uid(), type: 'review', title: 'Review Day', days: 1};
    case 'flex':   return {id: uid(), type: 'flex', title: 'Flex Day', days: 1};
    default:       return {id: uid(), type: 'custom', title: 'Custom Day', days: 1};
  }
}

function newInsertFromPalette(p) {
  switch (p.kind) {
    case 'lesson': return {id: uid(), type: 'lesson', module: p.module, path: p.path, title: p.title, days: 1};
    case 'final':  return {id: uid(), type: 'final', file: p.file, title: p.title || (p.name + ' Final'), days: 1, points: 100};
    case 'test':   return {id: uid(), type: 'test', title: 'Test', days: 1, points: 100};
    case 'review': return {id: uid(), type: 'review', title: 'Review Day', days: 1};
    case 'flex':   return {id: uid(), type: 'flex', title: 'Flex Day', days: 1};
    case 'custom': return {id: uid(), type: 'custom', title: 'Custom Day', days: 1};
    default:       return null;
  }
}

function dropAtBoard(i, p) {
  if (!schedule) return;
  if (p.src === 'board') {
    const j = schedule.sequence.findIndex(b => b.id === p.id);
    if (j < 0) return;
    const [blk] = schedule.sequence.splice(j, 1);
    if (j < i) i--;
    schedule.sequence.splice(i, 0, blk);
  } else if (p.src === 'insert') {
    const origin = blockById(p.blockId);
    if (!origin) return;
    const k = (origin.inserts || []).findIndex(x => x.id === p.insertId);
    if (k < 0) return;
    const [ins] = origin.inserts.splice(k, 1);
    const blk = {id: ins.id, type: ins.type, title: ins.title, days: ins.days || 1};
    if (ins.points != null) blk.points = ins.points;
    if (ins.file) blk.file = ins.file;
    if (ins.module) { blk.module = ins.module; blk.path = ins.path; }
    schedule.sequence.splice(i, 0, blk);
  } else {
    const blk = newBlockFromPalette(p);
    schedule.sequence.splice(i, 0, blk);
    if (blk.type === 'module') expandedBlocks.add(blk.id);
  }
  markDirty();
}

function dropAtInsert(blockId, afterDay, afterInsId, p) {
  const blk = blockById(blockId);
  if (!blk) return;
  let item = null;
  if (p.src === 'palette') {
    item = newInsertFromPalette(p);
    if (!item) { toast('Modules can’t be nested inside another module'); return; }
  } else if (p.src === 'board') {
    const moving = blockById(p.id);
    if (!moving) return;
    if (moving.type === 'module') { toast('Modules can’t be nested inside another module'); return; }
    schedule.sequence = schedule.sequence.filter(b => b.id !== p.id);
    item = {id: moving.id, type: moving.type, title: moving.title, days: moving.days || 1};
    if (moving.points != null) item.points = moving.points;
    if (moving.file) item.file = moving.file;
    if (moving.module) { item.module = moving.module; item.path = moving.path; }
  } else if (p.src === 'insert') {
    const origin = blockById(p.blockId);
    if (!origin) return;
    const k = (origin.inserts || []).findIndex(x => x.id === p.insertId);
    if (k < 0) return;
    [item] = origin.inserts.splice(k, 1);
    if (afterInsId === item.id) afterInsId = null;
  }
  blk.inserts = blk.inserts || [];
  if (afterInsId) {
    const idx = blk.inserts.findIndex(x => x.id === afterInsId);
    item.after_day = idx >= 0 ? (blk.inserts[idx].after_day || 0) : afterDay;
    blk.inserts.splice(idx + 1, 0, item);
  } else {
    item.after_day = afterDay;
    let idx = blk.inserts.findIndex(x => (x.after_day || 0) >= afterDay);
    if (idx < 0) idx = blk.inserts.length;
    blk.inserts.splice(idx, 0, item);
  }
  blk.inserts.sort((a, b) => (a.after_day || 0) - (b.after_day || 0));
  expandedBlocks.add(blockId);
  markDirty();
}

// ── Sync to Canvas ────────────────────────────────────────────────────────────

async function loadCourses() {
  if (courses) return;
  const [cRes, fRes] = await Promise.all([
    fetch('/api/courses').then(r => r.json()),
    fetch('/api/favorites').then(r => r.json()),
  ]);
  if (cRes.error && !cRes.courses) throw new Error(cRes.error);
  courses = cRes.courses || [];
  favoriteIds = new Set(fRes.favorite_ids || []);
}

async function openSync(blockId) {
  syncBlockId = blockId;
  const r = resolvedById(blockId);
  if (!r) return;
  document.getElementById('syncOverlay').style.display = 'block';
  document.getElementById('syncModal').style.display = 'flex';
  document.getElementById('syncResult').style.display = 'none';
  document.getElementById('syncResult').innerHTML = '';
  document.getElementById('syncBtn').disabled = false;
  document.getElementById('syncBtn').textContent = 'Sync';

  const isModule = r.type === 'module';
  document.getElementById('syncTitle').textContent = isModule
    ? 'Sync Unit ' + r.unit_number + ' — ' + r.name : 'Sync — ' + (r.title || r.type);

  const counts = {};
  (r.slots || []).forEach(s => { if ((s.part || 1) === 1) counts[s.kind] = (counts[s.kind] || 0) + 1; });
  let lines = [];
  if (isModule) {
    const pts = smartRound((r.points || 10) * Math.pow(r.scale || 1.15, r.unit_number));
    lines.push('<div>Canvas module <b>“Unit ' + r.unit_number + '”</b> will be created (unpublished), '
      + 'with due dates from the schedule:</div>');
    if (counts.lesson) lines.push('<div>&bull; ' + counts.lesson + ' lesson assignment' + (counts.lesson > 1 ? 's' : '') + ' @ ' + pts + ' pts (review + ASSIGNMENT.md content)</div>');
    if (counts.test)   lines.push('<div>&bull; ' + counts.test + ' test placeholder' + (counts.test > 1 ? 's' : '') + ' (title + date only — no content)</div>');
    if (counts.final)  lines.push('<div>&bull; ' + counts.final + ' final placeholder' + (counts.final > 1 ? 's' : '') + ' (title + date only — exam content stays private)</div>');
    const skipped = (counts.review || 0) + (counts.flex || 0) + (counts.custom || 0) + (counts.gap || 0);
    if (skipped) lines.push('<div style="color:var(--muted)">&bull; ' + skipped + ' review/flex/custom day' + (skipped > 1 ? 's' : '') + ' stay schedule-only</div>');
  } else if (r.type === 'test' || r.type === 'final') {
    lines.push('<div>One unpublished placeholder assignment — title, date, and points only. '
      + (r.type === 'final' ? 'Exam content in the private Admin repo never leaves it.' : '') + '</div>');
  } else {
    lines.push('<div>One unpublished assignment with content from the lesson’s ASSIGNMENT.md.</div>');
  }
  lines.push('<div style="color:var(--muted)">' + fmtD(r.start) + (r.days > 1 ? ' &rarr; ' + fmtD(r.end) : '') + '</div>');
  document.getElementById('syncPreview').innerHTML = lines.join('');

  const sel = document.getElementById('syncCourse');
  try {
    await loadCourses();
  } catch (e) {
    sel.innerHTML = '';
    document.getElementById('syncBtn').disabled = true;
    document.getElementById('syncPreview').innerHTML =
      '<div style="color:var(--red)">' + esc(String(e.message || e)) + '</div>';
    return;
  }
  sel.innerHTML = '';
  // Remembered per-schedule, not globally — a teacher who syncs multiple
  // courses through this hub must not have one schedule's last-used course
  // silently carry over as the default for a different schedule's sync.
  const last = schedName ? localStorage.getItem('syncCourseId_' + schedName) : null;
  const placeholder = document.createElement('option');
  placeholder.value = '';
  placeholder.textContent = '— Select a course —';
  sel.appendChild(placeholder);
  const starred = courses.filter(c => favoriteIds.has(c.id));
  const rest    = courses.filter(c => !favoriteIds.has(c.id));
  const addGroup = (label, arr) => {
    if (!arr.length) return;
    const g = document.createElement('optgroup');
    g.label = label;
    arr.forEach(c => {
      const o = document.createElement('option');
      o.value = c.id;
      o.textContent = c.name +
        (c.concluded ? ' — concluded (read-only)'
         : c.workflow_state === 'unpublished' ? ' — unpublished' : '');
      if (c.concluded) o.disabled = true;
      if (String(c.id) === last && !c.concluded) o.selected = true;
      g.appendChild(o);
    });
    sel.appendChild(g);
  };
  addGroup('★ Starred', starred);
  addGroup('All courses', rest);
  // No remembered course for this schedule — force an explicit pick rather
  // than silently defaulting to whatever sorts first in the list.
  if (!last) placeholder.selected = true;
  onSyncCourseChange();
}

function onSyncCourseChange() {
  const sel = document.getElementById('syncCourse');
  const opt = sel.selectedOptions[0];
  const btn = document.getElementById('syncBtn');
  const target = document.getElementById('syncTarget');
  const warn = document.getElementById('syncCourseWarn');
  if (!opt || !opt.value) {
    btn.disabled = true;
    target.textContent = '';
    warn.style.display = 'none';
    return;
  }
  btn.disabled = false;
  target.innerHTML = 'Will write to: <b>' + esc(opt.textContent) + '</b>';
  const last = schedName ? localStorage.getItem('syncCourseId_' + schedName) : null;
  const switched = last && String(opt.value) !== last;
  warn.style.display = switched ? 'block' : 'none';
  if (switched) warn.textContent = '⚠ Different course than this schedule last synced to — double-check before syncing.';
}

function closeSync() {
  document.getElementById('syncOverlay').style.display = 'none';
  document.getElementById('syncModal').style.display = 'none';
}

async function doSync() {
  const sel = document.getElementById('syncCourse');
  const courseId = sel.value;
  if (!courseId || !schedName) return;
  if (!confirm('Sync to “' + sel.selectedOptions[0].textContent + '”?')) return;
  localStorage.setItem('syncCourseId_' + schedName, courseId);
  const btn = document.getElementById('syncBtn');
  btn.disabled = true;
  btn.textContent = 'Syncing…';
  const res = await fetch('/api/schedules/' + encodeURIComponent(schedName) + '/sync-block', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({course_id: parseInt(courseId), block_id: syncBlockId}),
  }).then(r => r.json()).catch(e => ({error: String(e)}));
  btn.textContent = 'Sync';
  btn.disabled = false;
  const out = document.getElementById('syncResult');
  out.style.display = 'block';
  if (res.error) {
    out.innerHTML = '<div style="color:var(--red);font-size:13px">&#x2715; ' + esc(res.error) + '</div>';
    return;
  }
  const ok = res.created || [];
  const err = res.errors || [];
  out.innerHTML =
    '<div style="color:var(--green);font-size:13px;font-weight:600;margin-bottom:6px">&#x2713; ' +
      (res.module_name ? esc(res.module_name) + ' created — ' : '') + ok.length + ' assignment' + (ok.length !== 1 ? 's' : '') + '</div>' +
    ok.map(x => '<div class="result-row"><span class="result-ok">&#x2713;</span> ' + esc(x.name) + '</div>').join('') +
    err.map(x => '<div class="result-row"><span class="result-err">&#x2715;</span> ' + esc(x.name) + '</div>').join('') +
    '<div style="margin-top:8px"><a href="https://hw.instructure.com/courses/' + courseId +
    '/modules" target="_blank" style="color:var(--accent);font-size:12px">Open in Canvas &rarr;</a></div>';
}

// ── Finals (stored in the private Admin repo) ─────────────────────────────────

async function newFinal() {
  const name = prompt('Final name — usually the topic folder name (e.g. GitUsage, MiniGPT):');
  if (!name) return;
  if (!/^[A-Za-z0-9][A-Za-z0-9 _\-]*$/.test(name)) { toast('Letters, numbers, spaces, - and _ only'); return; }
  const res = await fetch('/api/finals/' + encodeURIComponent(name), {
    method: 'POST', headers: {'Content-Type': 'application/json'}, body: '{}',
  }).then(r => r.json());
  if (res.error) { toast(res.error); return; }
  await loadPalette();
  openFinalEditor(null, name);
}

async function openFinalEditor(e, name) {
  if (e) e.stopPropagation();
  const d = await fetch('/api/finals/' + encodeURIComponent(name)).then(r => r.json());
  if (d.error) { toast(d.error); return; }
  editingFinal = name;
  document.getElementById('feTitle').textContent = 'finals/' + name + '.md (private Admin repo)';
  document.getElementById('feText').value = d.content;
  document.getElementById('finalOverlay').style.display = 'block';
  document.getElementById('finalEditorModal').style.display = 'flex';
}

function closeFinalEditor() {
  document.getElementById('finalOverlay').style.display = 'none';
  document.getElementById('finalEditorModal').style.display = 'none';
  editingFinal = null;
}

async function saveFinal() {
  if (!editingFinal) return;
  await fetch('/api/finals/' + encodeURIComponent(editingFinal), {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({content: document.getElementById('feText').value}),
  });
  toast('Saved finals/' + editingFinal + '.md');
  closeFinalEditor();
  loadPalette();
}

async function deleteFinal() {
  if (!editingFinal || !confirm('Delete finals/' + editingFinal + '.md?')) return;
  await fetch('/api/finals/' + encodeURIComponent(editingFinal), {method: 'DELETE'});
  closeFinalEditor();
  loadPalette();
}

return {init, pickSchedule, newSchedule, loadPalette, toggleDow, toggleNoSchool,
        pickCalClass, importIcs,
        addNoSchool, removeNoSchool, toggleTopic, toggleBlock, removeBlock,
        stepBlock, setBlockPoints, removeInsert, stepInsert, setInsertPoints,
        editBlockTitle, editInsertTitle, openSync, closeSync, doSync, onSyncCourseChange,
        newFinal, openFinalEditor, closeFinalEditor, saveFinal, deleteFinal};
})();
