// Module Planner tab — create/edit curated modules (_modules/<slug>.json) and lesson files

window.Planner = (() => {

let allTopics = [];
let selectedTopics = [];
let assignments = [];        // merged lesson rows for selected topics
let reviewSelections = {};   // idx -> [{module, path, file, label}, ...] — several reviews may stack on one day
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

// Called every time the tab is re-shown — picks up topics/lessons created in
// the Module Editor (or on disk) since the tab was first initialized.
function onShow() {
  loadTopics();
  loadSavedList();
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
  assignments = []; reviewSelections = {};
  await reloadAllLessons();   // fresh rows from the repo (source of truth)

  // Rebuild the SAVED row order — lessons may be interleaved across topics,
  // with placeholders anywhere. Repo lessons not in the save are appended
  // unchecked; saved lessons gone from the repo are reported stale.
  const fresh = assignments;
  const freshMap = new Map(fresh.map(a => [a._module + '/' + a.path, a]));
  const ordered = [], orderedChecked = [], missing = [];
  reviewSelections = {};
  (m.assignments || []).forEach(p => {
    if (p.placeholder) {
      const entry = {day: p.day, duration: p.duration || 1,
                     title: p.title, path: '', _module: '', placeholder: true};
      if (p.kind) entry.kind = p.kind;
      if (p.review) reviewSelections[ordered.length] = Array.isArray(p.review) ? p.review : [p.review];
      ordered.push(entry); orderedChecked.push(true);
      return;
    }
    const key = p._module + '/' + p.path;
    const row = freshMap.get(key);
    if (!row) { missing.push(key); return; }
    freshMap.delete(key);
    if (p.duration_override) {           // teacher-set length wins over LESSONS.md
      row.duration = p.duration || 1;
      row.duration_override = true;
    }
    if (p.no_assignment) row.no_assignment = true;
    if (p.review) reviewSelections[ordered.length] = Array.isArray(p.review) ? p.review : [p.review];
    ordered.push(row); orderedChecked.push(true);
  });
  freshMap.forEach(row => { ordered.push(row); orderedChecked.push(false); });
  assignments = ordered;
  renumberDays();
  renderLessonTable();
  await reapplyRowState(orderedChecked);
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
  const checkedArr = snapshotChecked();
  const results = await Promise.all(
    selectedTopics.map(name => fetch('/api/topics/' + encodeURIComponent(name)).then(r => r.json()))
  );
  const freshByKey = new Map();
  results.forEach((r, idx) => (r.assignments || []).forEach(a =>
    freshByKey.set(selectedTopics[idx] + '/' + a.path,
                   Object.assign({}, a, {_module: selectedTopics[idx],
                                         durationDefault: a.duration || 1}))));
  // Preserve the current row order (lessons may be interleaved across topics,
  // placeholders anywhere): keep existing rows in place, drop rows whose topic
  // was removed, append lessons from newly added topics at the end.
  const keep = [], keepChecked = [], nextReviews = {};
  assignments.forEach((a, i) => {
    let row = a;
    if (!a.placeholder) {
      const key = a._module + '/' + a.path;
      if (!freshByKey.has(key)) return;
      row = freshByKey.get(key);
      freshByKey.delete(key);
    }
    if (reviewSelections[i]) nextReviews[keep.length] = reviewSelections[i];
    keep.push(row);
    keepChecked.push(checkedArr[i] !== false);
  });
  freshByKey.forEach(row => { keep.push(row); keepChecked.push(true); });
  assignments = keep;
  reviewSelections = nextReviews;
  renumberDays();
  renderLessonTable();
  await reapplyRowState(keepChecked);
}

// "Additional Day" placeholders — a stub lesson (no real path/_module yet) the
// teacher can insert above/below any row and fill in with real content later.
// They live only in this module's own assignments list (see CLAUDE.md
// "Placeholder ('Additional Day') entries"); day numbers are recomputed from
// array order whenever one is inserted or removed so the sequence stays tight.

function newPlaceholder() {
  return {day: 1, duration: 1, title: 'Additional Day', path: '', _module: '', placeholder: true};
}

// Half days: two ½-day assignments share one class day and get sub-indices
// .0 and .1 (named unit.day.0 / unit.day.1 on Canvas). An unpaired ½ day
// still consumes the whole slot — the next full-day item starts the next day.
function renumberDays() {
  let day = 1, half = false;   // half = current day already holds one ½-day item
  assignments.forEach(a => {
    const dur = a.duration || 1;
    if (dur === 0.5) {
      a.day = day;
      a.sub = half ? 1 : 0;
      if (half) { day += 1; half = false; } else half = true;
    } else {
      if (half) { day += 1; half = false; }
      a.day = day;
      delete a.sub;
      day += dur;
    }
  });
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

// Placeholder kinds: '' = ordinary Additional Day (fill in later, nothing syncs),
// 'page' = Canvas Page instead of an assignment (no homework that day),
// 'test' = reserved day number for manual test placement (nothing syncs).
function onPlaceholderKind(i, value) {
  const a = assignments[i];
  if (!a || !a.placeholder) return;
  const wasDefault = a.title === 'Additional Day' || a.title === 'Test Day' || a.title === 'In-Class Page';
  if (value) a.kind = value; else delete a.kind;
  if (wasDefault) {
    a.title = value === 'test' ? 'Test Day' : (value === 'page' ? 'In-Class Page' : 'Additional Day');
    const input = $('pltitle_' + i);
    if (input) input.value = a.title;
  }
}

// ── Row drag: interleave lessons from any selected topic in any order ─────────
// The table order IS the module order — saved as-is, so lessons from different
// topics can be intermixed day by day.

let rowDragIdx = null;

function rowDragStart(e, i) {
  rowDragIdx = i;
  e.dataTransfer.effectAllowed = 'move';
}

function rowDragOver(e) {
  if (rowDragIdx == null) return;
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
  e.currentTarget.classList.add('drag-over');
}

function rowDragLeave(e) { e.currentTarget.classList.remove('drag-over'); }

function rowDragEnd() {
  rowDragIdx = null;
  document.querySelectorAll('.lesson-row-wrap.drag-over').forEach(el => el.classList.remove('drag-over'));
}

// Move the dragged row so it sits where the drop target row was (insert-before).
async function rowDrop(e, i) {
  e.preventDefault();
  e.currentTarget.classList.remove('drag-over');
  const from = rowDragIdx;
  rowDragIdx = null;
  if (from == null || from === i) return;
  const checkedArr = snapshotChecked();
  const reviews = assignments.map((_, idx) => reviewSelections[idx] || null);
  const [row] = assignments.splice(from, 1);
  const [chk] = checkedArr.splice(from, 1);
  const [rev] = reviews.splice(from, 1);
  const to = i > from ? i - 1 : i;
  assignments.splice(to, 0, row);
  checkedArr.splice(to, 0, chk);
  reviews.splice(to, 0, rev);
  reviewSelections = {};
  reviews.forEach((r, idx) => { if (r) reviewSelections[idx] = r; });
  renumberDays();
  renderLessonTable();
  await reapplyRowState(checkedArr);
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

// Inline day-count control: reads "1 Day" like a button, opens a dropdown on
// click. Picking a value other than the LESSONS.md default marks the row
// duration_override so the teacher's length survives reloads; picking the
// default clears the override and the row follows the repo again.
function durationCell(a, i) {
  const def = a.placeholder ? null : (a.durationDefault || 1);
  let opts = '';
  [0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10].forEach(n => {
    const label = (n === 0.5 ? '½ Day' : n + (n === 1 ? ' Day' : ' Days')) + (def === n ? ' (default)' : '');
    opts += '<option value="' + n + '"' + ((a.duration || 1) === n ? ' selected' : '') + '>' + label + '</option>';
  });
  return '<select class="dur-select' + (a.duration_override ? ' overridden' : '') + '" id="pldur_' + i + '"' +
         ' title="Class periods this assignment spans — ½ Day pairs two assignments onto one class day (numbered .0 and .1)"' +
         ' onchange="Planner.onDurationChange(' + i + ', this.value)">' + opts + '</select>';
}

function onNoHwChange(i, checked) {
  const a = assignments[i];
  if (!a || a.placeholder) return;
  if (checked) a.no_assignment = true; else delete a.no_assignment;
  const label = $('plnohwlabel_' + i);
  if (label) label.classList.toggle('on', checked);
}

function onDurationChange(i, value) {
  const a = assignments[i];
  if (!a) return;
  a.duration = parseFloat(value) || 1;
  if (!a.placeholder) {
    if (a.duration === (a.durationDefault || 1)) delete a.duration_override;
    else a.duration_override = true;
  }
  $('pldur_' + i).classList.toggle('overridden', !!a.duration_override);
  renumberDays();
  refreshAll();   // re-labels every row's unit.day (ranges shift below this row)
}

function renderLessonRow(a, i, unitNum) {
  const titleCell = a.placeholder
    ? '<div class="lesson-title-cell">' +
        '<input class="lesson-title-input" id="pltitle_' + i + '" value="' + esc(a.title) +
          '" placeholder="Additional Day" oninput="Planner.onPlaceholderTitleInput(' + i + ', this.value)">' +
        '<select class="ph-kind" id="plkind_' + i + '" title="What this day becomes on Canvas sync" ' +
          'onchange="Planner.onPlaceholderKind(' + i + ', this.value)">' +
          '<option value=""' + (!a.kind ? ' selected' : '') + '>Assignment (fill in later)</option>' +
          '<option value="page"' + (a.kind === 'page' ? ' selected' : '') + '>Page — no homework</option>' +
          '<option value="test"' + (a.kind === 'test' ? ' selected' : '') + '>Test day — reserve number</option>' +
        '</select>' +
        '<button type="button" class="lesson-remove-btn" title="Remove this day" ' +
          'onclick="Planner.removePlaceholder(' + i + ')">&#x2715;</button>' +
      '</div>'
    : '<div class="lesson-title" title="View / edit lesson files" onclick="Planner.openEditor(' + i + ')">' + esc(a.title) + '</div>';
  return (
    '<div class="lesson-row-wrap"' +
      ' ondragover="Planner.rowDragOver(event)"' +
      ' ondragleave="Planner.rowDragLeave(event)"' +
      ' ondrop="Planner.rowDrop(event,' + i + ')">' +
      '<div class="lesson-row' + (a.placeholder ? ' placeholder-row' : '') + '" id="plrow_' + i + '">' +
        '<span class="row-drag" draggable="true" title="Drag to reorder — lessons from different topics can be intermixed"' +
          ' ondragstart="Planner.rowDragStart(event,' + i + ')" ondragend="Planner.rowDragEnd()">&#8942;&#8942;</span>' +
        '<input type="checkbox" checked id="plcheck_' + i + '" onchange="Planner.onLessonCheck()">' +
        '<div class="lesson-day" id="plday_' + i + '">' + fmtDayLabel(unitNum, a) + '</div>' +
        titleCell +
        durationCell(a, i) +
        (a.placeholder ? '<span></span>' :
          '<label class="nohw-toggle' + (a.no_assignment ? ' on' : '') + '" id="plnohwlabel_' + i + '"' +
            ' title="No assignment due this day — Canvas sync creates a content page (lesson + reviews) instead of a homework assignment">' +
            '<input type="checkbox"' + (a.no_assignment ? ' checked' : '') +
              ' onchange="Planner.onNoHwChange(' + i + ', this.checked)">' +
            '<span>no HW</span>' +
          '</label>') +
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
          '<span id="plrbadge_' + i + '" class="review-chips" style="display:none"></span>' +
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
  if (cb.checked) { populateReviewModules(i); renderReviewChips(i); renderReviewUsage(i); }
  else { delete reviewSelections[i]; renderReviewChips(i); renderAllOpenReviewUsages(); refreshAll(); }
}

// ── Attached-review chips (a row can stack several reviews on one day) ────────

function renderReviewChips(i) {
  const el = $('plrbadge_' + i);
  if (!el) return;
  const revs = reviewSelections[i] || [];
  el.style.display = revs.length ? 'flex' : 'none';
  el.innerHTML = revs.map((rev, k) =>
    '<span class="review-chip" title="' + esc(rev.module + '/' + rev.path + '/review/' + rev.file) + '">' +
      esc(rev.label || rev.file.replace(/\.md$/, '')) +
      '<span class="review-chip-x" onclick="Planner.removeReview(' + i + ',' + k + ')">&#x2715;</span>' +
    '</span>'
  ).join('');
}

function removeReview(i, k) {
  if (!reviewSelections[i]) return;
  reviewSelections[i].splice(k, 1);
  if (!reviewSelections[i].length) delete reviewSelections[i];
  renderReviewChips(i);
  renderAllOpenReviewUsages();
  refreshAll();
}

// Show every OTHER lesson row's already-attached reviews, and where they live,
// so picking one here doesn't silently duplicate a review already in this plan.
function renderReviewUsage(i) {
  const el = $('plrusage_' + i);
  if (!el) return;
  const unitNum = parseInt($('fUnit').value) || 0;
  const curModule = $('plrmod_' + i) ? $('plrmod_' + i).value : '';
  const curPath   = $('plrlesson_' + i) ? $('plrlesson_' + i).value : '';
  const curFile   = $('plrfile_' + i) ? $('plrfile_' + i).value : '';
  const used = [];
  Object.keys(reviewSelections).forEach(k => {
    const j = parseInt(k);
    if (j === i || !reviewSelections[j]) return;
    const a = assignments[j];
    reviewSelections[j].forEach(rev => {
      const exact = !!curFile && rev.module === curModule && rev.path === curPath && rev.file === curFile;
      const sameLesson = !exact && !!curPath && rev.module === curModule && rev.path === curPath;
      used.push({
        dayLabel: a ? fmtDayLabel(unitNum, a) : '?',
        title: a ? a.title : '(removed lesson)',
        label: rev.label || rev.file.replace(/\.md$/, ''),
        exact, sameLesson,
      });
    });
  });
  used.sort((x, y) => (y.exact - x.exact) || (y.sameLesson - x.sameLesson));
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
  const lessonSel = $('plrlesson_' + i), fileSel = $('plrfile_' + i);
  lessonSel.innerHTML = '<option value="">Lesson…</option>'; lessonSel.disabled = true;
  fileSel.innerHTML = '<option value="">Review…</option>'; fileSel.disabled = true;
  renderReviewUsage(i);
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
  const fileSel = $('plrfile_' + i);
  fileSel.innerHTML = '<option value="">Review…</option>'; fileSel.disabled = true;
  // Update usage immediately on picking a lesson — before any file is chosen —
  // so a "same lesson" match against another row's review is visible right away.
  renderReviewUsage(i);
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

// Picking a review file ADDS it to the row's stack (a day can carry several).
// The file dropdown resets afterward so the pickers never linger in a
// selected-looking state — the chips below are the single source of truth
// for what is actually attached.
function onReviewFileChange(i) {
  const module = $('plrmod_' + i).value, lessonPath = $('plrlesson_' + i).value;
  const fileSel = $('plrfile_' + i), file = fileSel.value;
  if (!file) return;
  const label = fileSel.selectedOptions[0] ? fileSel.selectedOptions[0].textContent : file.replace(/\.md$/, '');
  const revs = reviewSelections[i] || (reviewSelections[i] = []);
  if (revs.some(r => r.module === module && r.path === lessonPath && r.file === file)) {
    toast('That review is already attached to this day');
  } else {
    revs.push({module: module, path: lessonPath, file: file, label: label});
  }
  fileSel.value = '';
  renderReviewChips(i);
  renderReviewUsage(i);
  renderAllOpenReviewUsages();
  refreshAll();
}

// Restore saved review refs (one or many) onto row i — chips only; the pickers
// stay blank so nothing looks "selected" that the user didn't just choose.
async function applyReview(i, revs) {
  $('plreview_' + i).checked = true;
  $('plrpanel_' + i).style.display = 'block';
  $('plrevlabel_' + i).classList.add('on');
  populateReviewModules(i);
  reviewSelections[i] = (Array.isArray(revs) ? revs : [revs]).map(rev =>
    Object.assign({label: rev.file.replace(/\.md$/, '')}, rev));
  renderReviewChips(i);
  renderReviewUsage(i);
}

// ── Save ──────────────────────────────────────────────────────────────────────

function onNameInput() {
  if (!slugTouched) $('fSlug').value = slugify($('fName').value);
  refreshAll();
}

function touchSlug() { slugTouched = true; }

function checkedAssignments() {
  // Renumber days sequentially over just the checked subset — an unchecked
  // lesson's original day must not leave a gap in the saved schedule (the
  // Year Schedule board would otherwise render it as an open/gap day).
  // Two ½-day items pair onto one day with sub-indices .0/.1 (see renumberDays).
  let day = 1, half = false;
  return assignments
    .map((a, i) => ({a, i}))
    .filter(({i}) => { const cb = $('plcheck_' + i); return cb && cb.checked; })
    .map(({a, i}) => {
      const dur = a.duration || 1;
      let sub = null, itemDay;
      if (dur === 0.5) {
        sub = half ? 1 : 0;
        itemDay = day;
        if (half) { day += 1; half = false; } else half = true;
      } else {
        if (half) { day += 1; half = false; }
        itemDay = day;
        day += dur;
      }
      const out = {day: itemDay, duration: dur, title: a.title,
                   path: a.path, _module: a._module,
                   review: (reviewSelections[i] && reviewSelections[i].length) ? reviewSelections[i] : null};
      if (sub !== null) out.sub = sub;
      if (a.placeholder) {
        out.placeholder = true;
        if (a.kind) out.kind = a.kind;
      } else {
        if (a.duration_override) out.duration_override = true;
        if (a.no_assignment) out.no_assignment = true;
      }
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
  setEditorMode('preview');   // preview-first: reading is the common case, Edit is one click away
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
  // ASSIGNMENT.md previews include the attached review blocks, exactly like the hub upload
  const revs = editorCtx.file === 'ASSIGNMENT.md' ? (reviewSelections[editorCtx.row] || []) : [];
  if (revs.length) {
    const contents = [];
    for (const rev of revs) {
      const rc = await fetch('/api/file?module=' + encodeURIComponent(rev.module) +
                             '&path=' + encodeURIComponent(rev.path) +
                             '&file=' + encodeURIComponent('review/' + rev.file)).then(r => r.json());
      if (rc.content) contents.push(rc.content);
    }
    if (contents.length) body.review_markdowns = contents;
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
        insertPlaceholder, removePlaceholder, onPlaceholderTitleInput, onPlaceholderKind, removeReview,
        rowDragStart, rowDragOver, rowDragLeave, rowDrop, rowDragEnd, onShow, onNoHwChange,
        onDurationChange};
})();
