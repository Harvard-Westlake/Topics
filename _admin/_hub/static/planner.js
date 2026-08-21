// Module Planner tab — create/edit curated modules (_modules/<slug>.json) and lesson files

window.Planner = (() => {

let allTopics = [];
let selectedTopics = [];
let assignments = [];        // merged lesson rows for selected topics
let reviewSelections = {};   // idx -> {module, path, file}
let savedModules = [];
let currentSlug = null;      // slug of the loaded saved module (null = new)
let slugTouched = false;

const $ = id => document.getElementById(id);

function slugify(s) {
  return s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
}

function init() {
  loadTopics().then(loadSavedList);
}

// ── Saved modules sidebar ─────────────────────────────────────────────────────

async function loadSavedList() {
  const res = await fetch('/api/saved').then(r => r.json());
  savedModules = res.modules || [];
  renderSavedList();
}

function renderSavedList() {
  $('plSavedList').innerHTML = savedModules.map((m, i) =>
    '<div class="saved-item' + (m.slug === currentSlug ? ' active' : '') + '" draggable="true"' +
    ' ondragstart="Planner.savedDragStart(event,' + i + ')"' +
    ' ondragover="Planner.savedDragOver(event)"' +
    ' ondragleave="Planner.savedDragLeave(event)"' +
    ' ondrop="Planner.savedDrop(event,' + i + ')"' +
    ' ondragend="Planner.savedDragEnd()"' +
    ' onclick="Planner.loadSaved(\'' + m.slug + '\')">' +
      '<div class="name">' + m.name + '</div>' +
      '<div class="meta">Unit ' + (m.unit_number ?? '—') + ' · ' + m.lesson_count + ' lessons · ' + (m.topic_names || []).join(', ') + '</div>' +
    '</div>'
  ).join('') || '<div style="font-size:12px;color:var(--muted)">No saved modules yet</div>';
}

// Drag to reorder the library — the new order autosaves: unit_number becomes
// the list position (1..N) and lesson plans regenerate server-side.

let savedDragIdx = null;

function savedDragStart(e, i) {
  savedDragIdx = i;
  e.dataTransfer.effectAllowed = 'move';
}

function savedDragOver(e) {
  if (savedDragIdx === null) return;
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
  const box = e.currentTarget.getBoundingClientRect();
  const above = e.clientY < box.top + box.height / 2;
  e.currentTarget.classList.toggle('drop-above', above);
  e.currentTarget.classList.toggle('drop-below', !above);
}

function savedDragLeave(e) {
  e.currentTarget.classList.remove('drop-above', 'drop-below');
}

function savedDrop(e, i) {
  e.preventDefault();
  const above = e.currentTarget.classList.contains('drop-above');
  e.currentTarget.classList.remove('drop-above', 'drop-below');
  if (savedDragIdx === null) return;
  const from = savedDragIdx;
  savedDragIdx = null;
  let to = i + (above ? 0 : 1);
  if (to > from) to--;
  if (to === from) return;
  const [moved] = savedModules.splice(from, 1);
  savedModules.splice(to, 0, moved);
  renderSavedList();
  saveOrder();
}

function savedDragEnd() {
  savedDragIdx = null;
  document.querySelectorAll('#plSavedList .drop-above, #plSavedList .drop-below')
    .forEach(el => el.classList.remove('drop-above', 'drop-below'));
}

async function saveOrder() {
  const d = await fetch('/api/saved-order', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({order: savedModules.map(m => m.slug)}),
  }).then(r => r.json()).catch(err => ({error: String(err)}));
  if (d.error) { toast(d.error); loadSavedList(); return; }
  savedModules = d.modules || savedModules;
  renderSavedList();
  // keep the open editor's Unit field in step with the renumbering
  const cur = savedModules.find(m => m.slug === currentSlug);
  if (cur && cur.unit_number != null) $('fUnit').value = cur.unit_number;
  toast('Order saved — unit numbers now 1–' + savedModules.length);
}

function newModule() {
  currentSlug = null;
  slugTouched = false;
  selectedTopics = [];
  assignments = [];
  reviewSelections = {};
  $('fName').value = ''; $('fSlug').value = ''; $('fDesc').value = '';
  $('fUnit').value = 0; $('fPoints').value = 10; $('fScale').value = 1.15;
  $('plDeleteBtn').style.display = 'none';
  $('plResult').textContent = '';
  $('plStaleNote').style.display = 'none';
  renderTopicChips(); renderLessonTable(); refreshAll();
  loadSavedList();
}

async function loadSaved(slug) {
  const m = await fetch('/api/saved/' + encodeURIComponent(slug)).then(r => r.json());
  if (m.error) { $('plResult').innerHTML = '<span class="result-err">✕ ' + m.error + '</span>'; return; }
  currentSlug = slug;
  slugTouched = true;
  $('fName').value  = m.name || '';
  $('fSlug').value  = m.slug || slug;
  $('fDesc').value  = m.description || '';
  $('fUnit').value  = m.unit_number ?? 0;
  $('fPoints').value = m.points_per_assignment ?? 10;
  $('fScale').value  = m.scale_factor ?? 1.15;
  $('plDeleteBtn').style.display = 'inline-block';
  $('plResult').textContent = '';

  selectedTopics = (m.topic_names || []).slice();
  renderTopicChips();
  await reloadAllLessons();   // fresh rows from the repo (source of truth)

  // Placeholder ("Additional Day") entries don't come from the repo, so
  // reloadAllLessons() never recreates them — reinsert each at the position
  // matching its saved day, and remember any review it had attached.
  const savedPlaceholders = (m.assignments || []).filter(a => a.placeholder);
  savedPlaceholders.forEach(p => {
    let at = assignments.findIndex(a => a.day >= p.day);
    if (at === -1) at = assignments.length;
    assignments.splice(at, 0, {day: p.day, duration: p.duration || 1,
                               title: p.title, path: '', _module: '', placeholder: true});
    if (p.review) reviewSelections[at] = p.review;
  });
  if (savedPlaceholders.length) renderLessonTable();

  // Re-apply the saved selection: check only saved lessons, restore reviews
  const savedKey = a => a._module + '/' + a.path;
  const savedReal = (m.assignments || []).filter(a => !a.placeholder);
  const savedMap = new Map(savedReal.map(a => [savedKey(a), a]));
  const freshKeys = new Set(assignments.filter(a => !a.placeholder).map(savedKey));
  for (let i = 0; i < assignments.length; i++) {
    if (assignments[i].placeholder) {
      $('plcheck_' + i).checked = true;
      if (reviewSelections[i]) await applyReview(i, reviewSelections[i]);
      continue;
    }
    const saved = savedMap.get(savedKey(assignments[i]));
    $('plcheck_' + i).checked = !!saved;
    if (saved && saved.review) await applyReview(i, saved.review);
  }
  onLessonCheck();

  // Anything saved that no longer exists in the repo
  const missing = [...savedMap.keys()].filter(k => !freshKeys.has(k));
  $('plStaleNote').style.display = missing.length ? 'block' : 'none';
  $('plStaleNote').textContent = missing.length
    ? 'Saved lessons no longer found in the repo (removed on next save): ' + missing.join(', ')
    : '';
  loadSavedList();
}

async function deleteModule() {
  if (!currentSlug) return;
  if (!confirm('Delete _modules/' + currentSlug + '.json and its lesson plan?')) return;
  await fetch('/api/saved/' + encodeURIComponent(currentSlug), {method: 'DELETE'});
  newModule();
}

// ── Topic chips ───────────────────────────────────────────────────────────────

async function loadTopics() {
  const res = await fetch('/api/topics').then(r => r.json());
  allTopics = res.topics || [];
  refreshTopicDatalist();
}

function refreshTopicDatalist() {
  const filter = $('plTopicText').value || '';
  const dl = $('plTopicList');
  dl.innerHTML = '';
  allTopics
    .filter(n => !selectedTopics.includes(n))
    .filter(n => !filter || n.toLowerCase().includes(filter.toLowerCase()))
    .forEach(name => {
      const o = document.createElement('option');
      o.value = name;
      dl.appendChild(o);
    });
}

function onTopicTextChange() {
  const val = $('plTopicText').value.trim();
  if (allTopics.includes(val) && !selectedTopics.includes(val)) addTopicChip(val);
}

function onTopicTextKey(e) {
  const input = $('plTopicText');
  if (e.key === 'Enter') {
    const val = input.value.trim();
    if (allTopics.includes(val) && !selectedTopics.includes(val)) { addTopicChip(val); e.preventDefault(); }
  }
  if (e.key === 'Backspace' && !input.value && selectedTopics.length) {
    removeTopicChip(selectedTopics[selectedTopics.length - 1]);
  }
}

function addTopicChip(name)    { selectedTopics.push(name); $('plTopicText').value = ''; renderTopicChips(); refreshTopicDatalist(); reloadAllLessons(); }
function removeTopicChip(name) { selectedTopics = selectedTopics.filter(n => n !== name); renderTopicChips(); refreshTopicDatalist(); reloadAllLessons(); }

function renderTopicChips() {
  const container = $('plTopicChips');
  container.querySelectorAll('.module-chip').forEach(c => c.remove());
  const input = $('plTopicText');
  input.placeholder = selectedTopics.length ? '' : 'Search topic…';
  [...selectedTopics].reverse().forEach(name => {
    const chip = document.createElement('span');
    chip.className = 'module-chip';
    chip.innerHTML = name + '<span class="module-chip-x" onclick="Planner.removeTopicChip(\'' + name + '\')">&#x2715;</span>';
    container.insertBefore(chip, input);
  });
}

// ── Lesson table ──────────────────────────────────────────────────────────────

async function reloadAllLessons() {
  if (!selectedTopics.length) {
    assignments = []; reviewSelections = {};
    renderLessonTable(); refreshAll();
    return;
  }
  const results = await Promise.all(
    selectedTopics.map(name => fetch('/api/topics/' + encodeURIComponent(name)).then(r => r.json()))
  );
  assignments = results.flatMap((r, idx) =>
    (r.assignments || []).map(a => Object.assign({}, a, {_module: selectedTopics[idx]}))
  );
  reviewSelections = {};
  renderLessonTable();
  refreshAll();
}

// "Additional Day" placeholders — a stub lesson (no real path/_module yet) the
// teacher can insert above/below any row and fill in with real content later.
// They live only in this module's own assignments list (see CLAUDE.md
// "Placeholder ('Additional Day') entries"); day numbers are recomputed from
// array order whenever one is inserted or removed so the sequence stays tight.

function newPlaceholder() {
  return {day: 1, duration: 1, title: 'Additional Day', path: '', _module: '', placeholder: true};
}

function renumberDays() {
  let day = 1;
  assignments.forEach(a => { a.day = day; day += a.duration || 1; });
}

// idx -> checked state, read from the DOM before a re-render throws it away
function snapshotChecked() {
  return assignments.map((_, i) => { const cb = $('plcheck_' + i); return !cb || cb.checked; });
}

// Re-key reviewSelections (idx -> review ref) after inserting at `insertAt`
// or removing `removeAt` (pass the other as null).
function shiftReviewSelections(insertAt, removeAt) {
  const next = {};
  Object.keys(reviewSelections).forEach(k => {
    let idx = parseInt(k, 10);
    if (insertAt != null && idx >= insertAt) idx += 1;
    if (removeAt != null) {
      if (idx === removeAt) return;
      if (idx > removeAt) idx -= 1;
    }
    next[idx] = reviewSelections[k];
  });
  reviewSelections = next;
}

// Reapply checkbox state after a full re-render (which defaults every row to
// checked) and reopen any review panel a row had selected.
async function reapplyRowState(checkedArr) {
  assignments.forEach((_, i) => {
    const cb = $('plcheck_' + i);
    if (cb) cb.checked = checkedArr[i] !== false;
  });
  onLessonCheck();
  for (let i = 0; i < assignments.length; i++) {
    if (reviewSelections[i]) await applyReview(i, reviewSelections[i]);
  }
}

function insertPlaceholder(at) {
  const checkedArr = snapshotChecked();
  checkedArr.splice(at, 0, true);
  shiftReviewSelections(at, null);
  assignments.splice(at, 0, newPlaceholder());
  renumberDays();
  renderLessonTable();
  reapplyRowState(checkedArr).then(() => {
    const input = $('pltitle_' + at);
    if (input) { input.focus(); input.select(); }
  });
}

function removePlaceholder(i) {
  if (!assignments[i] || !assignments[i].placeholder) return;
  const checkedArr = snapshotChecked();
  checkedArr.splice(i, 1);
  shiftReviewSelections(null, i);
  assignments.splice(i, 1);
  renumberDays();
  renderLessonTable();
  reapplyRowState(checkedArr);
}

function onPlaceholderTitleInput(i, value) {
  if (assignments[i]) assignments[i].title = value;
}

function renderLessonTable() {
  const unitNum = parseInt($('fUnit').value) || 0;
  $('plLessonsBlock').style.display = assignments.length ? 'block' : 'none';
  $('plLessonRows').innerHTML = assignments.map((a, i) => renderInsertStrip(i) + renderLessonRow(a, i, unitNum)).join('')
    + renderInsertStrip(assignments.length);
  onLessonCheck();
}

function renderInsertStrip(at) {
  return '<div class="lesson-insert" onclick="Planner.insertPlaceholder(' + at + ')" title="Insert an Additional Day here">' +
           '<span class="lesson-insert-btn">+ Additional Day</span>' +
         '</div>';
}

function renderLessonRow(a, i, unitNum) {
  const titleCell = a.placeholder
    ? '<div class="lesson-title-cell">' +
        '<input class="lesson-title-input" id="pltitle_' + i + '" value="' + esc(a.title) +
          '" placeholder="Additional Day" oninput="Planner.onPlaceholderTitleInput(' + i + ', this.value)">' +
        '<button type="button" class="lesson-remove-btn" title="Remove this day" ' +
          'onclick="Planner.removePlaceholder(' + i + ')">&#x2715;</button>' +
      '</div>'
    : '<div class="lesson-title" title="View / edit lesson files" onclick="Planner.openEditor(' + i + ')">' + esc(a.title) + '</div>';
  return (
    '<div class="lesson-row-wrap">' +
      '<div class="lesson-row' + (a.placeholder ? ' placeholder-row' : '') + '" id="plrow_' + i + '">' +
        '<input type="checkbox" checked id="plcheck_' + i + '" onchange="Planner.onLessonCheck()">' +
        '<div class="lesson-day" id="plday_' + i + '">' + fmtDayLabel(unitNum, a) + '</div>' +
        titleCell +
        '<label class="review-toggle" id="plrevlabel_' + i + '">' +
          '<input type="checkbox" id="plreview_' + i + '" onchange="Planner.toggleReview(' + i + ')">' +
          '<span>+ Review</span>' +
        '</label>' +
      '</div>' +
      '<div class="review-panel" id="plrpanel_' + i + '" style="display:none">' +
        '<div class="review-picker">' +
          '<select id="plrmod_' + i + '" onchange="Planner.onReviewModuleChange(' + i + ')"></select>' +
          '<select id="plrlesson_' + i + '" onchange="Planner.onReviewLessonChange(' + i + ')" disabled></select>' +
          '<select id="plrfile_' + i + '" onchange="Planner.onReviewFileChange(' + i + ')" disabled></select>' +
          '<span id="plrbadge_' + i + '" class="review-badge" style="display:none"></span>' +
        '</div>' +
        '<div class="review-usage" id="plrusage_' + i + '"></div>' +
      '</div>' +
    '</div>'
  );
}

function onLessonCheck() {
  assignments.forEach((_, i) => {
    const cb = $('plcheck_' + i), row = $('plrow_' + i);
    if (cb && row) row.classList.toggle('unchecked', !cb.checked);
  });
  refreshAll();
}

function toggleReview(i) {
  const cb = $('plreview_' + i);
  $('plrpanel_' + i).style.display = cb.checked ? 'block' : 'none';
  $('plrevlabel_' + i).classList.toggle('on', cb.checked);
  if (cb.checked) { populateReviewModules(i); renderReviewUsage(i); }
  else { delete reviewSelections[i]; $('plrbadge_' + i).style.display = 'none'; renderAllOpenReviewUsages(); }
}

// Show every OTHER lesson row's already-selected review, and where it lives,
// so picking one here doesn't silently duplicate a review already in this plan.
function renderReviewUsage(i) {
  const el = $('plrusage_' + i);
  if (!el) return;
  const unitNum = parseInt($('fUnit').value) || 0;
  const curModule = $('plrmod_' + i) ? $('plrmod_' + i).value : '';
  const curPath   = $('plrlesson_' + i) ? $('plrlesson_' + i).value : '';
  const curFile   = $('plrfile_' + i) ? $('plrfile_' + i).value : '';
  const used = Object.keys(reviewSelections)
    .map(k => parseInt(k))
    .filter(j => j !== i && reviewSelections[j])
    .map(j => {
      const rev = reviewSelections[j];
      const a = assignments[j];
      const exact = !!curFile && rev.module === curModule && rev.path === curPath && rev.file === curFile;
      const sameLesson = !exact && !!curPath && rev.module === curModule && rev.path === curPath;
      return {
        dayLabel: a ? fmtDayLabel(unitNum, a) : '?',
        title: a ? a.title : '(removed lesson)',
        label: rev.label || rev.file.replace(/\.md$/, ''),
        exact, sameLesson,
      };
    })
    .sort((x, y) => (y.exact - x.exact) || (y.sameLesson - x.sameLesson));
  if (!used.length) { el.innerHTML = ''; return; }
  el.innerHTML = '<div class="review-usage-head">Already used in this plan:</div>' +
    used.map(u =>
      '<div class="review-usage-item' + (u.exact ? ' dup' : (u.sameLesson ? ' same-lesson' : '')) + '">' +
        '<span class="rday">' + esc(u.dayLabel) + '</span>' +
        '<span class="rtitle">' + esc(u.title) + '</span>' +
        '<span class="rwhat">' + esc(u.label) + '</span>' +
        (u.exact ? '<span class="rtag">exact duplicate</span>'
                 : (u.sameLesson ? '<span class="rtag">same lesson</span>' : '')) +
      '</div>'
    ).join('');
}

// Re-render usage in every row whose review panel is currently open, so a
// change on one row is reflected wherever else a picker happens to be open.
function renderAllOpenReviewUsages() {
  assignments.forEach((_, j) => {
    const panel = $('plrpanel_' + j);
    if (panel && panel.style.display !== 'none') renderReviewUsage(j);
  });
}

function populateReviewModules(i) {
  const sel = $('plrmod_' + i);
  if (sel.options.length > 1) return;
  sel.innerHTML = '<option value="">Module…</option>';
  allTopics.forEach(name => {
    const o = document.createElement('option');
    o.value = name; o.textContent = name;
    sel.appendChild(o);
  });
}

async function onReviewModuleChange(i) {
  const module = $('plrmod_' + i).value;
  const lessonSel = $('plrlesson_' + i), fileSel = $('plrfile_' + i), badge = $('plrbadge_' + i);
  lessonSel.innerHTML = '<option value="">Lesson…</option>'; lessonSel.disabled = true;
  fileSel.innerHTML = '<option value="">Day…</option>'; fileSel.disabled = true;
  badge.style.display = 'none';
  delete reviewSelections[i];
  renderReviewUsage(i); renderAllOpenReviewUsages();
  if (!module) return;
  const res = await fetch('/api/topics/' + encodeURIComponent(module)).then(r => r.json());
  const lessons = (res.assignments || []).filter(a => a.path);
  if (!lessons.length) { lessonSel.innerHTML = '<option value="">No lessons</option>'; return; }
  lessons.forEach(a => {
    const o = document.createElement('option');
    o.value = a.path; o.textContent = a.title;
    lessonSel.appendChild(o);
  });
  lessonSel.disabled = false;
}

async function onReviewLessonChange(i) {
  const module = $('plrmod_' + i).value, lessonPath = $('plrlesson_' + i).value;
  const fileSel = $('plrfile_' + i), badge = $('plrbadge_' + i);
  fileSel.innerHTML = '<option value="">Day…</option>'; fileSel.disabled = true;
  badge.style.display = 'none';
  delete reviewSelections[i];
  // Update usage immediately on picking a lesson — before any file is chosen —
  // so a "same lesson" match against another row's review is visible right away.
  renderReviewUsage(i); renderAllOpenReviewUsages();
  if (!lessonPath) return;
  const res = await fetch('/api/reviews?module=' + encodeURIComponent(module) +
                          '&path=' + encodeURIComponent(lessonPath)).then(r => r.json());
  const files = res.files || [];
  if (!files.length) { fileSel.innerHTML = '<option value="">No reviews</option>'; return; }
  files.forEach(f => {
    const o = document.createElement('option');
    o.value = f.file; o.textContent = f.label;
    fileSel.appendChild(o);
  });
  fileSel.disabled = false;
}

function onReviewFileChange(i) {
  const module = $('plrmod_' + i).value, lessonPath = $('plrlesson_' + i).value;
  const fileSel = $('plrfile_' + i), file = fileSel.value;
  const label = fileSel.selectedOptions[0] ? fileSel.selectedOptions[0].textContent : file.replace(/\.md$/, '');
  const badge = $('plrbadge_' + i);
  if (!file) { badge.style.display = 'none'; delete reviewSelections[i]; renderReviewUsage(i); renderAllOpenReviewUsages(); return; }
  reviewSelections[i] = {module: module, path: lessonPath, file: file, label: label};
  badge.textContent = label;
  badge.style.display = 'inline-block';
  renderReviewUsage(i);
  renderAllOpenReviewUsages();
}

// Restore a saved review ref into row i's pickers
async function applyReview(i, rev) {
  $('plreview_' + i).checked = true;
  $('plrpanel_' + i).style.display = 'block';
  $('plrevlabel_' + i).classList.add('on');
  populateReviewModules(i);
  $('plrmod_' + i).value = rev.module;
  await onReviewModuleChange(i);
  $('plrmod_' + i).value = rev.module;
  $('plrlesson_' + i).value = rev.path;
  await onReviewLessonChange(i);
  $('plrlesson_' + i).value = rev.path;
  $('plrfile_' + i).value = rev.file;
  onReviewFileChange(i);
}

// ── Save ──────────────────────────────────────────────────────────────────────

function onNameInput() {
  if (!slugTouched) $('fSlug').value = slugify($('fName').value);
  refreshAll();
}

function touchSlug() { slugTouched = true; }

function checkedAssignments() {
  return assignments
    .map((a, i) => ({a, i}))
    .filter(({i}) => { const cb = $('plcheck_' + i); return cb && cb.checked; })
    .map(({a, i}) => {
      const out = {day: a.day, duration: a.duration || 1, title: a.title,
                   path: a.path, _module: a._module,
                   review: reviewSelections[i] || null};
      if (a.placeholder) out.placeholder = true;
      return out;
    });
}

function refreshAll() {
  const unitNum = parseInt($('fUnit').value) || 0;
  const base    = parseFloat($('fPoints').value) || 10;
  const scale   = parseFloat($('fScale').value) || 1.15;
  const mult    = Math.pow(scale, unitNum);
  $('plScaleFactor').textContent = mult.toFixed(3);
  $('plScaledPts').textContent   = smartRound(base * mult);
  assignments.forEach((a, i) => {
    const el = $('plday_' + i);
    if (el) el.textContent = fmtDayLabel(unitNum, a);
  });
  $('plSaveBtn').disabled = !$('fName').value.trim() || !checkedAssignments().length;
}

async function saveModule() {
  const slug = $('fSlug').value.trim() || slugify($('fName').value);
  const body = {
    name: $('fName').value.trim(),
    slug: slug,
    description: $('fDesc').value.trim(),
    unit_number: parseInt($('fUnit').value) || 0,
    points_per_assignment: parseFloat($('fPoints').value) || 10,
    scale_factor: parseFloat($('fScale').value) || 1.15,
    start_date: null,
    topic_names: selectedTopics,
    assignments: checkedAssignments(),
  };
  const btn = $('plSaveBtn');
  btn.disabled = true; btn.textContent = 'Saving…';
  const res = await fetch('/api/saved/' + encodeURIComponent(slug), {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(body),
  }).then(r => r.json());
  btn.textContent = 'Save Module'; btn.disabled = false;
  if (res.error) {
    $('plResult').innerHTML = '<span class="result-err">✕ ' + res.error +
      (res.problems ? '\n' + res.problems.join('\n') : '') + '</span>';
    return;
  }
  currentSlug = slug;
  $('plDeleteBtn').style.display = 'inline-block';
  $('plResult').innerHTML = '<span class="result-ok">✓ Saved _modules/' + slug + '.json</span>';
  loadSavedList();
}

// ── Lesson file editor (view/edit lesson files, preview as Canvas renders) ────

let editorCtx = null;   // {module, path, row, file}
let editorDirty = false;

async function openEditor(i) {
  const a = assignments[i];
  editorCtx = {module: a._module, path: a.path, row: i, file: null};
  $('edTitle').textContent = a._module + '/' + a.path;
  const listing = await fetch('/api/lesson-files?module=' + encodeURIComponent(a._module) +
                              '&path=' + encodeURIComponent(a.path)).then(r => r.json());
  if (listing.error) return;
  buildEditorTabs(listing);
  $('plEditor').style.display = 'flex';
  $('plEditorOverlay').style.display = 'block';
  const first = listing.files.includes('ASSIGNMENT.md') ? 'ASSIGNMENT.md' : listing.files[0];
  openEditorTab(first);
}

function tabId(file) { return 'edtab_' + file.replace(/[^A-Za-z0-9]/g, '_'); }

function buildEditorTabs(listing) {
  const tabs = [];
  (listing.files || []).forEach(f => tabs.push({file: f, create: false}));
  (listing.review || []).forEach(f => tabs.push({file: f, create: false}));
  (listing.demos || []).forEach(f => tabs.push({file: f, create: false}));
  (listing.can_create || []).forEach(f => tabs.push({file: f, create: true}));
  $('edTabs').innerHTML = tabs.map(t =>
    '<button class="editor-tab' + (t.create ? ' create' : '') + '" id="' + tabId(t.file) + '"' +
    ' onclick="Planner.openEditorTab(\'' + t.file + '\')">' + (t.create ? '+ ' : '') + t.file + '</button>'
  ).join('');
}

async function openEditorTab(file) {
  if (editorDirty && !confirm('Discard unsaved changes?')) return;
  editorDirty = false;
  editorCtx.file = file;
  document.querySelectorAll('.editor-tab').forEach(t => t.classList.remove('active'));
  const tab = $(tabId(file));
  if (tab) tab.classList.add('active');
  const res = await fetch('/api/file?module=' + encodeURIComponent(editorCtx.module) +
                          '&path=' + encodeURIComponent(editorCtx.path) +
                          '&file=' + encodeURIComponent(file)).then(r => r.json());
  $('edText').value = res.content || '';
  $('edResult').textContent = '';
  const isDemo = file.startsWith('demos/');
  $('edModePreview').textContent = isDemo ? 'Live Preview' : 'Canvas Preview';
  $('edSub').textContent = isDemo
    ? 'Standalone demo page — previews the current buffer exactly as a browser renders it'
    : 'Files render exactly as the hub uploads them to Canvas';
  setEditorMode(isDemo ? 'preview' : 'edit');
}

function setEditorMode(mode) {
  $('edModeEdit').classList.toggle('active', mode === 'edit');
  $('edModePreview').classList.toggle('active', mode === 'preview');
  $('edText').style.display = mode === 'edit' ? 'block' : 'none';
  $('edPreview').style.display = mode === 'preview' ? 'block' : 'none';
  if (mode === 'preview') renderEditorPreview();
}

async function renderEditorPreview() {
  const isDemo = editorCtx.file && editorCtx.file.startsWith('demos/');
  $('edPreview').classList.toggle('demo', isDemo);
  if (isDemo) {
    // Standalone HTML renders live in an iframe; the current buffer is shown,
    // so unsaved edits preview without saving.
    $('edPreview').innerHTML = '';
    const frame = document.createElement('iframe');
    frame.className = 'demoframe';
    frame.srcdoc = $('edText').value;
    $('edPreview').appendChild(frame);
    $('edEngine').textContent = '';
    return;
  }
  const body = {
    markdown: $('edText').value,
    base_path: editorCtx.module + '/' + editorCtx.path,
  };
  // ASSIGNMENT.md previews include the attached review block, exactly like the hub upload
  const rev = editorCtx.file === 'ASSIGNMENT.md' ? reviewSelections[editorCtx.row] : null;
  if (rev) {
    const rc = await fetch('/api/file?module=' + encodeURIComponent(rev.module) +
                           '&path=' + encodeURIComponent(rev.path) +
                           '&file=' + encodeURIComponent('review/' + rev.file)).then(r => r.json());
    if (rc.content) body.review_markdown = rc.content;
  }
  const res = await fetch('/api/render', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(body),
  }).then(r => r.json());
  $('edPreview').innerHTML = res.html || '';
  $('edEngine').textContent = res.engine === 'builtin'
    ? 'approximate preview — pip3 install markdown for exact hub rendering' : '';
  // typeset math the way Canvas does (MathJax; CDN — needs internet)
  if (window.MathJax && MathJax.typesetPromise) {
    if (MathJax.typesetClear) MathJax.typesetClear([$('edPreview')]);
    MathJax.typesetPromise([$('edPreview')]).catch(() => {});
  }
}

async function saveFile() {
  const res = await fetch('/api/file', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({module: editorCtx.module, path: editorCtx.path,
                          file: editorCtx.file, content: $('edText').value}),
  }).then(r => r.json());
  if (res.error) { $('edResult').innerHTML = '<span class="result-err">✕ ' + res.error + '</span>'; return; }
  editorDirty = false;
  $('edResult').innerHTML = res.broken_links && res.broken_links.length
    ? '<span style="color:var(--yellow)">Saved, but broken links: ' + res.broken_links.join(', ') + '</span>'
    : '<span class="result-ok">✓ Saved ' + res.saved + '</span>';
  // A newly created file (e.g. ASSIGNMENT.md) becomes a real tab after saving
  const listing = await fetch('/api/lesson-files?module=' + encodeURIComponent(editorCtx.module) +
                              '&path=' + encodeURIComponent(editorCtx.path)).then(r => r.json());
  buildEditorTabs(listing);
  const tab = $(tabId(editorCtx.file));
  if (tab) tab.classList.add('active');
}

function markDirty() { editorDirty = true; }

function closeEditor() {
  if (editorDirty && !confirm('Discard unsaved changes?')) return;
  editorDirty = false;
  $('plEditor').style.display = 'none';
  $('plEditorOverlay').style.display = 'none';
}

return {init, newModule, loadSaved, deleteModule, onNameInput, touchSlug,
        refreshAll, refreshTopicDatalist, onTopicTextChange, onTopicTextKey,
        removeTopicChip, onLessonCheck, toggleReview, onReviewModuleChange,
        onReviewLessonChange, onReviewFileChange, saveModule, openEditor,
        openEditorTab, setEditorMode, saveFile, markDirty, closeEditor,
        savedDragStart, savedDragOver, savedDragLeave, savedDrop, savedDragEnd,
        insertPlaceholder, removePlaceholder, onPlaceholderTitleInput};
})();
