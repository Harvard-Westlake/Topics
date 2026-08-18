// Courses tab — Canvas course list, grades, and the Create Module drawer

window.Courses = (() => {

let courses     = [];
let favoriteIds = new Set();
let prefetched  = {};
let inflight    = {};
let viewMode    = 'starred';
let githubAssignments = [];
let reviewSelections  = {}; // {rowIndex: {module, lessonPath, file, content}}
let allGithubModules  = []; // full list from server (no _ already filtered server-side)
let addedModules      = new Set(JSON.parse(localStorage.getItem('addedModules') || '[]'));
let selectedModules   = []; // currently selected chips in the module picker
let unlockedCourses   = new Set();
let openPanels        = {};

// ── Helpers ──────────────────────────────────────────────────────────────────

function yearOf(c)    { return c.name && c.name.includes(' :: ') ? c.name.split(' :: ')[0] : 'Other'; }
function subjectOf(c) { const p = c.name.split(' :: '); return p.length >= 2 ? p[1] : c.name; }

function fmtDate(s) {
  if (!s) return '&mdash;';
  return new Date(s).toLocaleDateString('en-US', {month:'short', day:'numeric', year:'numeric'});
}
function fmtDue(s) {
  if (!s) return '&mdash;';
  const d = new Date(s), now = new Date();
  const diff = Math.ceil((d - now) / 86400000);
  const label = d.toLocaleDateString('en-US', {month:'short', day:'numeric'});
  if (diff < 0)  return '<span style="color:var(--muted)">' + label + '</span>';
  if (diff === 0) return '<span style="color:var(--yellow)">Today</span>';
  if (diff <= 3)  return '<span style="color:var(--yellow)">' + label + '</span>';
  return label;
}
function scoreColor(v) { return v >= 90 ? 'hi' : v < 70 ? 'lo' : ''; }

function setStatus(source, fetchedAt) {
  const labels = {
    live:           ['live', '&#9679; Live'],
    cache:          ['cache', '&#9679; Cached'],
    'cache-fallback':['cache-fallback', '&#9888; Stale'],
    loading:        ['loading', '&#9679; Loading&hellip;'],
    error:          ['error', '&#10005; Error'],
    'no-token':     ['error', '&#10005; No token'],
  };
  const [cls, txt] = labels[source] || labels.loading;
  const pill = document.getElementById('statusPill');
  pill.className = 'status-pill ' + cls;
  pill.innerHTML = '<div class="dot"></div>' + txt;
  document.getElementById('cacheAge').textContent = fetchedAt ? 'Updated ' + timeAgo(fetchedAt) : '';
}

// ── Data loading ──────────────────────────────────────────────────────────────

async function init() {
  const [courseRes, favRes] = await Promise.all([
    fetch('/api/courses').then(r => r.json()),
    fetch('/api/favorites').then(r => r.json()),
  ]);
  if (courseRes.error && !courseRes.courses) {
    setStatus('no-token');
    document.getElementById('list').innerHTML = '<div class="empty">' + esc(courseRes.error) + '</div>';
    return;
  }
  courses     = courseRes.courses || [];
  favoriteIds = new Set(favRes.favorite_ids || []);
  setStatus(courseRes.source, courseRes.fetched_at);
  populateYearFilter();
  render();
  prefetchVisible();
}

async function doRefresh() {
  const btn = document.getElementById('refreshBtn');
  btn.disabled = true;
  setStatus('loading');
  const [courseRes, favRes] = await Promise.all([
    fetch('/api/courses?refresh=1').then(r => r.json()),
    fetch('/api/favorites?refresh=1').then(r => r.json()),
  ]);
  courses     = courseRes.courses || [];
  favoriteIds = new Set(favRes.favorite_ids || []);
  prefetched  = {}; inflight = {};
  setStatus(courseRes.error && !courseRes.courses ? 'no-token' : courseRes.source, courseRes.fetched_at);
  populateYearFilter();
  render();
  btn.disabled = false;
  prefetchVisible();
}

// ── Prefetch ──────────────────────────────────────────────────────────────────

function prefetchVisible() {
  const selY = document.getElementById('yearFilter').value;
  courses.filter(c => {
    return (viewMode !== 'starred' || favoriteIds.has(c.id)) &&
           (!selY || yearOf(c) === selY);
  }).forEach(c => prefetchCourse(c.id));
}

function prefetchCourse(id) {
  ['assignments', 'modules', 'grades'].forEach(type => {
    const key = id + '_' + type;
    if (prefetched[key] || inflight[key]) return;
    inflight[key] = fetch('/api/courses/' + id + '/' + type)
      .then(r => r.json())
      .then(d => { prefetched[key] = d; delete inflight[key]; })
      .catch(() => delete inflight[key]);
  });
}

// ── Render ────────────────────────────────────────────────────────────────────

function setView(mode) {
  viewMode = mode;
  document.getElementById('toggleStarred').classList.toggle('active', mode === 'starred');
  document.getElementById('toggleAll').classList.toggle('active',     mode === 'all');
  render();
  prefetchVisible();
}

function populateYearFilter() {
  const years = [...new Set(courses.map(yearOf))].sort().reverse();
  const sel = document.getElementById('yearFilter');
  const prev = sel.value;
  sel.innerHTML = '<option value="">All years</option>';
  years.forEach(y => {
    const o = document.createElement('option');
    o.value = y; o.textContent = y;
    if (y === prev) o.selected = true;
    sel.appendChild(o);
  });
}

function render() {
  const q    = document.getElementById('search').value.toLowerCase();
  const selY = document.getElementById('yearFilter').value;
  let filtered = courses.filter(c =>
    (viewMode !== 'starred' || favoriteIds.has(c.id)) &&
    (!selY || yearOf(c) === selY) &&
    (!q    || c.name.toLowerCase().includes(q))
  );
  // Fallback: if starred view returns nothing, show all
  let fallback = false;
  if (!filtered.length && viewMode === 'starred' && !q && !selY) {
    filtered = courses;
    fallback  = true;
  }
  document.getElementById('count').textContent =
    filtered.length + ' course' + (filtered.length !== 1 ? 's' : '') +
    (fallback ? ' (no starred — showing all)' : '');
  const list = document.getElementById('list');
  if (!filtered.length) {
    list.innerHTML = '<div class="empty">No courses match.</div>';
    return;
  }
  list.innerHTML = filtered.map((c, i) => buildCard(c, i)).join('');
}

function buildCard(c, i) {
  const yr      = yearOf(c);
  const sub     = subjectOf(c);
  const isOther = yr === 'Other';
  const starred = favoriteIds.has(c.id);
  return '<div class="course-wrap" id="wrap_' + c.id + '">' +
    '<div class="course-card">' +
      '<div class="course-index">' + (i + 1) + '</div>' +
      '<div class="course-body">' +
        '<div class="course-top">' +
          '<div class="course-name">' + c.name + '</div>' +
          (starred ? '<span class="star">&#9733;</span>' : '') +
          '<div class="course-date">' + fmtDate(c.created_at) + '</div>' +
        '</div>' +
        '<div class="course-meta">' +
          '<span class="badge ' + (isOther ? 'badge-other' : 'badge-year') + '">' + yr + '</span>' +
          (!isOther ? '<span class="badge badge-subj">' + sub + '</span>' : '') +
          (c.workflow_state === 'unpublished' ? '<span class="badge badge-unpub">Unpublished</span>' : '') +
          (c.concluded ? '<span class="badge badge-concl">Concluded</span>' : '') +
        '</div>' +
        '<div class="sub-btns">' +
          makeSubBtn(c.id, 'assignments', 'Assignments') +
          makeSubBtn(c.id, 'modules',     'Modules') +
          makeSubBtn(c.id, 'grades',      'Grades') +
          makeNewModuleBtn(c.id, starred) +
        '</div>' +
      '</div>' +
    '</div>' +
    '<div class="panel" id="panel_' + c.id + '"><div class="panel-inner" id="panelInner_' + c.id + '"></div></div>' +
  '</div>';
}

function makeNewModuleBtn(id, starred) {
  if (starred) {
    return '<button class="sub-btn sub-btn-new" onclick="Courses.openDrawer(' + id + ')">' +
      '<svg width="10" height="10" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.5">' +
        '<line x1="8" y1="2" x2="8" y2="14"/><line x1="2" y1="8" x2="14" y2="8"/>' +
      '</svg>' +
      '<span class="lbl">New Module</span>' +
    '</button>';
  }
  // Non-starred: greyed out, double-click unlocks
  return '<button class="sub-btn sub-btn-locked" id="newmod_' + id + '" ' +
    'ondblclick="Courses.unlockNewModule(' + id + ')" ' +
    'onclick="Courses.tryNewModule(' + id + ')" ' +
    'title="Double-click to unlock">' +
    '<svg width="10" height="10" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2">' +
      '<rect x="4" y="7" width="8" height="7" rx="1"/>' +
      '<path d="M6 7V5a2 2 0 0 1 4 0v2"/>' +
    '</svg>' +
    '<span class="lbl">New Module</span>' +
  '</button>';
}

function unlockNewModule(id) {
  unlockedCourses.add(id);
  const btn = document.getElementById('newmod_' + id);
  if (!btn) return;
  btn.classList.remove('sub-btn-locked');
  btn.classList.add('sub-btn-unlocked');
  btn.title = 'Click to add module';
  btn.innerHTML =
    '<svg width="10" height="10" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.5">' +
      '<line x1="8" y1="2" x2="8" y2="14"/><line x1="2" y1="8" x2="14" y2="8"/>' +
    '</svg>' +
    '<span class="lbl">New Module</span>';
}

function tryNewModule(id) {
  if (unlockedCourses.has(id)) openDrawer(id);
}

function makeSubBtn(id, type, label) {
  return '<button class="sub-btn" id="btn_' + id + '_' + type + '" onclick="Courses.togglePanel(' + id + ',\'' + type + '\')">' +
    '<svg class="mini-spin" width="10" height="10" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.5">' +
      '<path d="M13.5 2.5A7 7 0 1 0 15 8" stroke-linecap="round"/>' +
    '</svg>' +
    '<span class="lbl">' + label + '</span>' +
  '</button>';
}

// ── Panel ─────────────────────────────────────────────────────────────────────

async function togglePanel(courseId, type) {
  const panel = document.getElementById('panel_' + courseId);
  const wrap  = document.getElementById('wrap_' + courseId);
  const btn   = document.getElementById('btn_' + courseId + '_' + type);

  if (openPanels[courseId] === type && panel.classList.contains('open')) {
    panel.classList.remove('open');
    wrap.classList.remove('open');
    btn.classList.remove('active');
    openPanels[courseId] = null;
    return;
  }

  ['assignments', 'modules', 'grades'].forEach(t => {
    const b = document.getElementById('btn_' + courseId + '_' + t);
    if (b) b.classList.remove('active');
  });

  btn.classList.add('active', 'loading');
  openPanels[courseId] = type;

  const key = courseId + '_' + type;
  if (!prefetched[key]) {
    if (!inflight[key]) prefetchCourse(courseId);
    await inflight[key];
  }
  const data = prefetched[key];

  btn.classList.remove('loading');
  document.getElementById('panelInner_' + courseId).innerHTML = renderPanel(type, data);
  panel.classList.add('open');
  wrap.classList.add('open');
}

function renderPanel(type, data) {
  if (!data) return '<div style="color:var(--muted);font-size:13px;padding:12px 0">Failed to load.</div>';

  if (type === 'assignments') {
    const rows = data.assignments || [];
    if (!rows.length) return '<div style="color:var(--muted);font-size:13px;padding:8px 0">No assignments.</div>';
    return rows.map(a =>
      '<div class="assign-row">' +
        '<div class="assign-due">' + fmtDue(a.due_at) + '</div>' +
        '<div><a href="' + a.html_url + '" target="_blank">' + a.name + '</a></div>' +
        '<div class="assign-pts">' + (a.points != null ? a.points + ' pts' : '&mdash;') + '</div>' +
      '</div>'
    ).join('');
  }

  if (type === 'modules') {
    const rows = data.modules || [];
    if (!rows.length) return '<div style="color:var(--muted);font-size:13px;padding:8px 0">No modules.</div>';
    return rows.map(m =>
      '<div class="module-row">' +
        '<div>' + m.name + '</div>' +
        '<div class="module-items">' + m.items_count + ' item' + (m.items_count !== 1 ? 's' : '') + '</div>' +
      '</div>'
    ).join('');
  }

  if (type === 'grades') {
    const g = data.grades || {};
    const students = g.students || [];
    const avg = g.avg_current;
    const avgColor = avg >= 90 ? 'var(--green)' : avg < 70 ? 'var(--red)' : 'var(--accent)';
    return '<div class="grade-summary">' +
        '<div class="grade-stat"><div class="val">' + (g.count || '&mdash;') + '</div><div class="lbl">Students</div></div>' +
        '<div class="grade-stat"><div class="val" style="color:' + avgColor + '">' + (avg != null ? avg + '%' : '&mdash;') + '</div><div class="lbl">Class avg</div></div>' +
      '</div>' +
      students.map(s =>
        '<div class="grade-row">' +
          '<div>' + s.name + '</div>' +
          '<div class="grade-score ' + scoreColor(s.current_score) + '">' + (s.current_score != null ? s.current_score + '%' : '&mdash;') + '</div>' +
          '<div class="grade-score ' + scoreColor(s.final_score) + '">'   + (s.final_score   != null ? s.final_score   + '%' : '&mdash;') + '</div>' +
        '</div>'
      ).join('');
  }
  return '';
}

// ── Drawer ────────────────────────────────────────────────────────────────────

function openDrawer(preselectedId) {
  const sel  = document.getElementById('dmCourse');
  const prev = preselectedId ? String(preselectedId) : sel.value;
  sel.innerHTML = '<option value="">Select a course…</option>';
  const starred = courses.filter(c => favoriteIds.has(c.id));
  const rest    = courses.filter(c => !favoriteIds.has(c.id));
  if (starred.length) {
    const g = document.createElement('optgroup');
    g.label = '★ Starred';
    starred.forEach(c => addCourseOption(g, c, prev));
    sel.appendChild(g);
  }
  if (rest.length) {
    const g = document.createElement('optgroup');
    g.label = 'All courses';
    rest.forEach(c => addCourseOption(g, c, prev));
    sel.appendChild(g);
  }
  document.getElementById('drawer').style.display = 'flex';
  document.getElementById('drawerOverlay').style.display = 'block';
  document.getElementById('dmResult').style.display = 'none';
  selectedModules = [];
  renderModuleChips();
  document.getElementById('dmModuleText').value = '';
  githubAssignments = [];
  document.getElementById('dmLessons').style.display = 'none';
  document.getElementById('dmSavedModule').value = '';
  if (sel.value) onCourseChange();
  loadGithubModuleList();
  loadSavedModuleList();
}

function addCourseOption(group, c, selected) {
  const o = document.createElement('option');
  o.value = c.id; o.textContent = c.name;
  if (String(c.id) === String(selected)) o.selected = true;
  group.appendChild(o);
}

function closeDrawer() {
  document.getElementById('drawer').style.display = 'none';
  document.getElementById('drawerOverlay').style.display = 'none';
}

async function onCourseChange() {
  const courseId = document.getElementById('dmCourse').value;
  if (!courseId) return;
  document.getElementById('dmUnitHint').textContent = '…';
  const d = await fetch('/api/courses/' + courseId + '/next-unit').then(r => r.json());
  document.getElementById('dmUnit').value = d.next_unit;
  document.getElementById('dmUnitHint').textContent = '(next after ' + (d.next_unit - 1) + ')';
  buildPreview();
}

async function loadGithubModuleList() {
  if (!allGithubModules.length) {
    const res = await fetch('/api/github/modules').then(r => r.json()).catch(() => null);
    if (!res || res.error) {
      document.getElementById('dmModuleText').placeholder = 'Topics repo not found';
      return;
    }
    allGithubModules = res.modules || [];
  }
  refreshModuleDatalist(document.getElementById('dmModuleText').value || '');
}

function refreshModuleDatalist(filter) {
  const hideUsed = document.getElementById('dmHideUsed').checked;
  const dl = document.getElementById('dmGithubModuleList');
  dl.innerHTML = '';
  allGithubModules
    .filter(n => (!hideUsed || !addedModules.has(n)) && !selectedModules.includes(n))
    .filter(n => !filter || n.toLowerCase().includes(filter.toLowerCase()))
    .forEach(name => {
      const o = document.createElement('option');
      o.value = name;
      dl.appendChild(o);
    });
}

function clearUsedModules(e) {
  e.stopPropagation();
  addedModules.clear();
  localStorage.removeItem('addedModules');
  refreshModuleDatalist(document.getElementById('dmModuleText').value);
}

// ── Curated modules saved in _modules/ ───────────────────────────────────────

async function loadSavedModuleList() {
  const sel = document.getElementById('dmSavedModule');
  const res = await fetch('/api/github/saved-modules').then(r => r.json()).catch(() => null);
  const mods = (res && res.modules) || [];
  sel.innerHTML = '<option value="">&#8212; none &#8212;</option>';
  mods.forEach(m => {
    const o = document.createElement('option');
    o.value = m.slug;
    o.textContent = m.name + ' (' + m.lesson_count + ' lesson' + (m.lesson_count !== 1 ? 's' : '') + ')';
    sel.appendChild(o);
  });
  document.getElementById('dmSavedField').style.display = mods.length ? 'flex' : 'none';
}

async function loadSavedModule() {
  const slug = document.getElementById('dmSavedModule').value;
  if (!slug) return;
  const m = await fetch('/api/github/saved-modules/' + encodeURIComponent(slug)).then(r => r.json());
  if (m.error) return;
  selectedModules = (m.topic_names || []).slice();
  renderModuleChips();
  refreshModuleDatalist('');
  if (m.points_per_assignment != null) document.getElementById('dmPoints').value = m.points_per_assignment;
  if (m.scale_factor != null) document.getElementById('dmScale').value = m.scale_factor;
  if (m.unit_number != null && !document.getElementById('dmUnit').value) {
    document.getElementById('dmUnit').value = m.unit_number;
  }
  // Use the curated assignment list as-is (it may be a subset spanning topics)
  const savedReviews = {};
  githubAssignments = (m.assignments || []).map((a, i) => {
    if (a.review_markdown) savedReviews[i] = a;
    const copy = Object.assign({}, a);
    delete copy.review_markdown;
    return copy;
  });
  renderLessonTable();
  for (const i of Object.keys(savedReviews)) {
    const a = savedReviews[i];
    if (a.review_ref) {
      await applySavedReview(i, a.review_ref);   // replay pickers, fetch fresh content
    } else {
      reviewSelections[i] = {content: a.review_markdown};
      const cb = document.getElementById('lreview_' + i);
      if (cb) { cb.checked = true; document.getElementById('lrevlabel_' + i).classList.add('on'); }
      const badge = document.getElementById('rbadge_' + i);
      if (badge) { badge.textContent = 'review'; badge.style.display = 'inline-block'; }
    }
  }
  buildPreview();
}

async function applySavedReview(i, rev) {
  const cb = document.getElementById('lreview_' + i);
  if (!cb) return;
  cb.checked = true;
  document.getElementById('rpanel_' + i).style.display = 'block';
  document.getElementById('lrevlabel_' + i).classList.add('on');
  populateReviewModules(i);
  document.getElementById('rmod_' + i).value = rev.module;
  await onReviewModuleChange(i);
  document.getElementById('rmod_' + i).value = rev.module;
  document.getElementById('rlesson_' + i).value = rev.path;
  await onReviewLessonChange(i);
  document.getElementById('rlesson_' + i).value = rev.path;
  document.getElementById('rfile_' + i).value = rev.file;
  await onReviewFileChange(i);
}

function onModuleTextInput() {
  refreshModuleDatalist(document.getElementById('dmModuleText').value);
}

function onModuleTextChange() {
  const val = document.getElementById('dmModuleText').value.trim();
  if (allGithubModules.includes(val) && !selectedModules.includes(val)) {
    addModuleChip(val);
  }
}

function onModuleTextKey(e) {
  const input = document.getElementById('dmModuleText');
  if (e.key === 'Enter') {
    const val = input.value.trim();
    if (allGithubModules.includes(val) && !selectedModules.includes(val)) {
      addModuleChip(val);
      e.preventDefault();
    }
  }
  if (e.key === 'Backspace' && !input.value && selectedModules.length) {
    removeModuleChip(selectedModules[selectedModules.length - 1]);
  }
}

function addModuleChip(name) {
  selectedModules.push(name);
  document.getElementById('dmModuleText').value = '';
  renderModuleChips();
  refreshModuleDatalist('');
  reloadAllLessons();
}

function removeModuleChip(name) {
  selectedModules = selectedModules.filter(n => n !== name);
  renderModuleChips();
  refreshModuleDatalist('');
  reloadAllLessons();
}

function renderModuleChips() {
  const container = document.getElementById('dmModuleChips');
  container.querySelectorAll('.module-chip').forEach(c => c.remove());
  const input = document.getElementById('dmModuleText');
  input.placeholder = selectedModules.length ? '' : 'Search module…';
  [...selectedModules].reverse().forEach(name => {
    const chip = document.createElement('span');
    chip.className = 'module-chip';
    chip.innerHTML = name + '<span class="module-chip-x" onclick="Courses.removeModuleChip(\'' +
                     name.replace(/'/g, "\\'") + '\')">&#x2715;</span>';
    container.insertBefore(chip, input);
  });
}

async function reloadAllLessons() {
  if (!selectedModules.length) {
    githubAssignments = [];
    document.getElementById('dmLessons').style.display = 'none';
    document.getElementById('dmCreateBtn').disabled = true;
    buildPreview();
    return;
  }
  const results = await Promise.all(
    selectedModules.map(name =>
      fetch('/api/github/modules/' + encodeURIComponent(name)).then(r => r.json())
    )
  );
  // Tag each assignment with its source module so the backend can find ASSIGNMENT.md
  githubAssignments = results.flatMap((r, idx) =>
    (r.assignments || []).map(a => Object.assign({}, a, {_module: selectedModules[idx]}))
  );
  renderLessonTable();
  buildPreview();
}

function renderLessonTable() {
  const unitNum = parseInt(document.getElementById('dmUnit').value) || 0;
  const lessons = document.getElementById('dmLessons');
  const rowsEl  = document.getElementById('dmLessonRows');

  if (!githubAssignments.length) {
    lessons.style.display = 'none';
    return;
  }
  lessons.style.display = 'block';

  reviewSelections = {};
  rowsEl.innerHTML = githubAssignments.map((a, i) =>
    '<div class="lesson-row-wrap" id="lwrap_' + i + '">' +
      '<div class="lesson-row" id="lrow_' + i + '">' +
        '<input type="checkbox" checked id="lcheck_' + i + '" onchange="Courses.onLessonCheck(' + i + ')">' +
        '<div class="lesson-day" id="lday_' + i + '">' + fmtDayLabel(unitNum, a) + '</div>' +
        '<div>' + a.title + '</div>' +
        '<label class="review-toggle" id="lrevlabel_' + i + '">' +
          '<input type="checkbox" id="lreview_' + i + '" onchange="Courses.toggleReview(' + i + ')">' +
          '<span>+ Review</span>' +
        '</label>' +
      '</div>' +
      '<div class="review-panel" id="rpanel_' + i + '" style="display:none">' +
        '<div class="review-picker">' +
          '<select id="rmod_' + i + '" onchange="Courses.onReviewModuleChange(' + i + ')"></select>' +
          '<select id="rlesson_' + i + '" onchange="Courses.onReviewLessonChange(' + i + ')" disabled></select>' +
          '<select id="rfile_' + i + '" onchange="Courses.onReviewFileChange(' + i + ')" disabled></select>' +
          '<span id="rbadge_' + i + '" class="review-badge" style="display:none"></span>' +
        '</div>' +
      '</div>' +
    '</div>'
  ).join('');

  onLessonCheck();
}

function onLessonCheck(idx) {
  // dim unchecked rows
  githubAssignments.forEach((_, i) => {
    const cb  = document.getElementById('lcheck_' + i);
    const row = document.getElementById('lrow_' + i);
    if (cb && row) row.classList.toggle('unchecked', !cb.checked);
  });
  const anyChecked = githubAssignments.some((_, i) => {
    const cb = document.getElementById('lcheck_' + i);
    return cb && cb.checked;
  });
  document.getElementById('dmCreateBtn').disabled =
    !anyChecked || !document.getElementById('dmCourse').value;
}

function toggleReview(i) {
  const cb    = document.getElementById('lreview_' + i);
  const panel = document.getElementById('rpanel_' + i);
  const label = document.getElementById('lrevlabel_' + i);
  panel.style.display = cb.checked ? 'block' : 'none';
  label.classList.toggle('on', cb.checked);
  if (cb.checked) populateReviewModules(i);
  else { delete reviewSelections[i]; }
}

function populateReviewModules(i) {
  const sel = document.getElementById('rmod_' + i);
  if (sel.options.length > 1) return; // already populated
  sel.innerHTML = '<option value="">Module…</option>';
  allGithubModules.forEach(name => {
    const o = document.createElement('option');
    o.value = name; o.textContent = name;
    sel.appendChild(o);
  });
}

async function onReviewModuleChange(i) {
  const module = document.getElementById('rmod_' + i).value;
  const lessonSel = document.getElementById('rlesson_' + i);
  const fileSel   = document.getElementById('rfile_' + i);
  const badge     = document.getElementById('rbadge_' + i);
  lessonSel.innerHTML = '<option value="">Lesson…</option>';
  lessonSel.disabled = true;
  fileSel.innerHTML = '<option value="">Day…</option>';
  fileSel.disabled = true;
  badge.style.display = 'none';
  delete reviewSelections[i];
  if (!module) return;
  const res = await fetch('/api/github/modules/' + encodeURIComponent(module)).then(r => r.json());
  const lessons = (res.assignments || []).filter(a => a.path);
  if (!lessons.length) { lessonSel.innerHTML = '<option value="">No lessons</option>'; return; }
  lessons.forEach(a => {
    const o = document.createElement('option');
    o.value = a.path; o.dataset.title = a.title; o.textContent = a.title;
    lessonSel.appendChild(o);
  });
  lessonSel.disabled = false;
}

async function onReviewLessonChange(i) {
  const module    = document.getElementById('rmod_' + i).value;
  const lessonPath = document.getElementById('rlesson_' + i).value;
  const fileSel   = document.getElementById('rfile_' + i);
  const badge     = document.getElementById('rbadge_' + i);
  fileSel.innerHTML = '<option value="">Day…</option>';
  fileSel.disabled = true;
  badge.style.display = 'none';
  delete reviewSelections[i];
  if (!lessonPath) return;
  const res = await fetch('/api/github/reviews?module=' + encodeURIComponent(module) +
                          '&path=' + encodeURIComponent(lessonPath)).then(r => r.json());
  const files = res.files || [];
  if (!files.length) { fileSel.innerHTML = '<option value="">No reviews</option>'; return; }
  files.forEach(f => {
    const o = document.createElement('option');
    o.value = f; o.textContent = f.replace(/\.md$/, '');
    fileSel.appendChild(o);
  });
  fileSel.disabled = false;
}

async function onReviewFileChange(i) {
  const module     = document.getElementById('rmod_' + i).value;
  const lessonPath = document.getElementById('rlesson_' + i).value;
  const file       = document.getElementById('rfile_' + i).value;
  const badge      = document.getElementById('rbadge_' + i);
  if (!file) { badge.style.display = 'none'; delete reviewSelections[i]; return; }
  const res = await fetch('/api/github/review-content?module=' + encodeURIComponent(module) +
                          '&path=' + encodeURIComponent(lessonPath) +
                          '&file=' + encodeURIComponent(file)).then(r => r.json());
  if (res.content) {
    reviewSelections[i] = {module, lessonPath, file, content: res.content};
    badge.textContent = file.replace(/\.md$/, '');
    badge.style.display = 'inline-block';
  }
}

function getParsedAssignments() {
  return githubAssignments.filter((_, i) => {
    const cb = document.getElementById('lcheck_' + i);
    return cb ? cb.checked : true;
  }).map(a => {
    // Find original index in githubAssignments to look up reviewSelections
    const origIdx = githubAssignments.indexOf(a);
    const rev = reviewSelections[origIdx];
    return rev ? Object.assign({}, a, {review_markdown: rev.content}) : a;
  });
}

// ── Point scaling ─────────────────────────────────────────────────────────────
// multiplier = scale^unit_number, applied silently on create

function getScale() {
  return parseFloat(document.getElementById('dmScale').value) || 1.15;
}

function unlockScale() {
  const el = document.getElementById('dmScale');
  if (!el.disabled) return;
  el.disabled = false;
  el.style.pointerEvents = 'auto';
  el.parentElement.style.cursor = 'auto';
  el.classList.remove('scale-locked');
  el.classList.add('scale-unlocked');
  el.focus();
  el.select();
}

function scaledPoints(basePoints, unitNum) {
  return smartRound(basePoints * Math.pow(getScale(), unitNum));
}

function buildPreview() {
  const unitNum   = parseInt(document.getElementById('dmUnit').value);
  const base      = parseInt(document.getElementById('dmPoints').value) || 10;
  const parsed = getParsedAssignments();
  const btn    = document.getElementById('dmCreateBtn');

  if (isNaN(unitNum)) {
    btn.disabled = true;
    return;
  }

  const multiplier = Math.pow(1.15, unitNum);
  const applied    = scaledPoints(base, unitNum);

  document.getElementById('dmScaleFactor').textContent = multiplier.toFixed(3);
  document.getElementById('dmScaledPts').textContent   = applied;

  // Refresh day labels in lesson table if unit number changed
  githubAssignments.forEach((a, i) => {
    const el = document.getElementById('lday_' + i);
    if (el) el.textContent = fmtDayLabel(unitNum, a);
  });

  btn.disabled = !document.getElementById('dmCourse').value || !parsed.length;
}

async function createModule() {
  const courseId  = document.getElementById('dmCourse').value;
  const unitNum   = parseInt(document.getElementById('dmUnit').value);
  const startDate = document.getElementById('dmStartDate').value || null;
  const base      = parseInt(document.getElementById('dmPoints').value) || 10;
  const points    = scaledPoints(base, unitNum);  // silently apply multiplier
  const parsed    = getParsedAssignments();

  const btn = document.getElementById('dmCreateBtn');
  btn.disabled = true;
  btn.textContent = 'Creating…';

  const res = await fetch('/api/courses/' + courseId + '/create-module', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({unit_number: unitNum, start_date: startDate,
                          points_per_assignment: points, assignments: parsed,
                          topic_names: selectedModules})
  }).then(r => r.json());

  btn.textContent = 'Create Module';
  btn.disabled = false;

  const resultEl = document.getElementById('dmResult');
  resultEl.style.display = 'block';

  if (res.error) {
    resultEl.innerHTML = '<div style="color:var(--red);font-size:13px">✕ ' + res.error + '</div>';
    return;
  }

  const ok  = (res.created || []).filter(r => r.linked);
  const err = res.errors || [];
  resultEl.innerHTML =
    '<div style="color:var(--green);font-size:13px;font-weight:600;margin-bottom:8px">' +
      '✓ Unit ' + res.unit_number + ' created &mdash; ' + ok.length + ' assignment' + (ok.length !== 1 ? 's' : '') + ' linked' +
    '</div>' +
    ok.map(r  => '<div class="result-row"><span class="result-ok">✓</span> ' + r.name + '</div>').join('') +
    err.map(r => '<div class="result-row"><span class="result-err">✕</span> ' + r.name + '</div>').join('') +
    '<div style="margin-top:10px"><a href="https://hw.instructure.com/courses/' + courseId + '/modules" target="_blank" style="color:var(--accent);font-size:12px">Open in Canvas →</a></div>';

  delete prefetched[courseId + '_modules'];
  delete prefetched[courseId + '_assignments'];

  // Mark all selected Topics modules as added so they drop off the list
  if (selectedModules.length) {
    selectedModules.forEach(n => addedModules.add(n));
    localStorage.setItem('addedModules', JSON.stringify([...addedModules]));
    refreshModuleDatalist('');
  }
}

return {init, render, setView, doRefresh, togglePanel, openDrawer, closeDrawer,
        onCourseChange, buildPreview, unlockScale, loadSavedModule,
        refreshModuleDatalist, clearUsedModules, onModuleTextInput,
        onModuleTextChange, onModuleTextKey, createModule, onLessonCheck,
        toggleReview, onReviewModuleChange, onReviewLessonChange,
        onReviewFileChange, removeModuleChip, unlockNewModule, tryNewModule};
})();
