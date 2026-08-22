// Module Editor tab — edit the topic folders themselves (the content source of
// truth): lesson files, activities (with README-toggle auto-sync), reviews,
// demos, and uploaded materials, plus structural ops (create/rename/delete/
// reorder lessons, new topics) that keep every index file in step server-side.

window.Editor = (() => {

const $ = id => document.getElementById(id);

let topics = [];
let curTopic = null;
let lessons = [];            // [{day, duration, title, path}] in LESSONS.md order
let curPath = null;
let curTitle = '';
let listing = null;          // /api/lesson-files result
let curFile = null;          // open file, or '::assets'
let dirty = false;
let impact = {modules: [], schedules: []};
let pendingDelete = null;    // {kind, file, label, typed}

function init() {
  fetch('/api/topics?with_lessons=1').then(r => r.json()).then(res => {
    topics = res.topics || [];
    renderTopicList();
  });
}

function onShow() { init(); }   // re-shown: pick up topics created elsewhere

// ── left rails ────────────────────────────────────────────────────────────────

function renderTopicList() {
  $('meTopicList').innerHTML = topics.map(t =>
    '<div class="me-item' + (t === curTopic ? ' active' : '') + '" onclick="Editor.pickTopic(\'' + t + '\')">' + esc(t) + '</div>'
  ).join('');
}

async function pickTopic(name) {
  if (dirty && !confirm('Discard unsaved changes?')) return;
  dirty = false;
  curTopic = name;
  curPath = null;
  renderTopicList();
  $('meTopicName').textContent = name;
  $('meLessonsPane').style.display = 'block';
  $('meWork').style.display = 'none';
  $('meEmpty').style.display = 'block';
  await reloadLessons();
}

async function reloadLessons() {
  const res = await fetch('/api/topics/' + encodeURIComponent(curTopic)).then(r => r.json());
  lessons = (res.assignments || []).filter(a => a.path);
  renderLessonList();
}

function renderLessonList() {
  $('meLessonList').innerHTML = lessons.map((a, i) =>
    '<div class="me-item me-lesson' + (a.path === curPath ? ' active' : '') + '" onclick="Editor.pickLesson(\'' + a.path + '\')">' +
      '<span class="me-day">' + esc(String(a.day)) + (a.duration > 1 ? '–' + (a.day + a.duration - 1) : '') + '</span>' +
      '<span class="me-lesson-title">' + esc(a.title) + '</span>' +
      '<span class="me-arrows" onclick="event.stopPropagation()">' +
        '<button title="Move up"   ' + (i === 0 ? 'disabled' : '') + ' onclick="Editor.moveLesson(' + i + ',-1)">&#9650;</button>' +
        '<button title="Move down" ' + (i === lessons.length - 1 ? 'disabled' : '') + ' onclick="Editor.moveLesson(' + i + ',1)">&#9660;</button>' +
      '</span>' +
    '</div>'
  ).join('') || '<div class="pal-note">No lessons yet</div>';
}

async function moveLesson(i, delta) {
  const order = lessons.map(a => a.path);
  const j = i + delta;
  [order[i], order[j]] = [order[j], order[i]];
  const res = await fetch('/api/editor/lessons', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({topic: curTopic, op: 'reorder', order}),
  }).then(r => r.json());
  if (res.error) { toast('✕ ' + res.error); return; }
  await reloadLessons();
  toast('Reordered — all index files updated');
}

// ── lesson workspace ──────────────────────────────────────────────────────────

async function pickLesson(path) {
  if (dirty && !confirm('Discard unsaved changes?')) return;
  dirty = false;
  curPath = path;
  const a = lessons.find(l => l.path === path);
  curTitle = a ? a.title : path;
  renderLessonList();
  $('meEmpty').style.display = 'none';
  $('meWork').style.display = 'flex';
  $('meLessonTitle').textContent = curTitle;
  $('meLessonPath').textContent = curTopic + '/' + path;
  const [files, imp] = await Promise.all([
    fetch('/api/lesson-files?module=' + encodeURIComponent(curTopic) + '&path=' + encodeURIComponent(path)).then(r => r.json()),
    fetch('/api/editor/impact?module=' + encodeURIComponent(curTopic) + '&path=' + encodeURIComponent(path)).then(r => r.json()),
  ]);
  if (files.error) { toast('✕ ' + files.error); return; }
  listing = files;
  impact = imp.error ? {modules: [], schedules: []} : imp;
  renderImpact();
  buildTabs();
  openTab('README.md');
}

function renderImpact() {
  const el = $('meImpact');
  const mods = impact.modules || [], scheds = impact.schedules || [];
  if (!mods.length && !scheds.length) {
    el.style.display = 'block';
    el.className = 'me-impact ok';
    el.innerHTML = 'Not referenced by any curated module — content edits flow automatically; structural changes affect only this topic.';
    return;
  }
  el.style.display = 'block';
  el.className = 'me-impact warn';
  el.innerHTML = 'Used by ' +
    (mods.length ? 'curated module' + (mods.length > 1 ? 's' : '') + ' ' +
      mods.map(m => '<strong>' + esc(m.name) + '</strong>' + (m.unit_number != null ? ' (Unit ' + m.unit_number + ')' : '')).join(', ') : '') +
    (mods.length && scheds.length ? ' · ' : '') +
    (scheds.length ? 'schedule' + (scheds.length > 1 ? 's' : '') + ' ' +
      scheds.map(s => '<strong>' + esc(s.name) + '</strong>' + (s.year ? ' (' + esc(s.year) + ')' : '')).join(', ') : '') +
    '. Content edits sync automatically; renames rewrite these references; adding/removing days re-dates the schedules.';
}

function tabId(file) { return 'metab_' + file.replace(/[^A-Za-z0-9]/g, '_'); }

// One labeled row per content type, so lesson / activities / reviews /
// materials read as clearly separate groups instead of one flowing strip.
function buildTabs() {
  const btn = (file, label, extra) =>
    '<button class="editor-tab' + (extra || '') + '" id="' + tabId(file) + '" onclick="Editor.openTab(\'' + file + '\')">' + esc(label) + '</button>';
  const newBtn = (label, fn) =>
    '<button class="editor-tab create" onclick="Editor.' + fn + '()">' + label + '</button>';
  const row = (label, inner) => inner
    ? '<div class="me-tabrow"><span class="me-tabrow-label">' + label + '</span><div class="me-tabrow-tabs">' + inner + '</div></div>'
    : '';

  const lesson = (listing.files || []).map(f => btn(f, f)).join('') +
                 (listing.can_create || []).map(f => btn(f, '+ ' + f, ' create')).join('');
  const milestones = (listing.milestones || []).map(f => btn(f, f.replace('milestones/', ''))).join('');
  const activities = (listing.activities || []).map(f => btn(f, f.replace('activities/', ''))).join('') +
                     newBtn('+ new activity', 'openNewActivity');
  const reviews = (listing.review || []).map(f => btn(f, f.replace('review/', ''))).join('') +
                  newBtn('+ new review', 'openNewReview');
  const demos = (listing.demos || []).map(f => btn(f, f.replace('demos/', ''))).join('');
  const materials = btn('::assets', 'Uploads (' + (listing.assets || []).length + ')');

  $('meTabs').innerHTML =
    row('Lesson', lesson) + row('Milestones', milestones) +
    row('Activities', activities) + row('Reviews', reviews) +
    row('Demos', demos) + row('Materials', materials);
}

async function openTab(file) {
  if (dirty && !confirm('Discard unsaved changes?')) return;
  dirty = false;
  curFile = file;
  document.querySelectorAll('#meTabs .editor-tab').forEach(t => t.classList.remove('active'));
  const tab = $(tabId(file));
  if (tab) tab.classList.add('active');
  $('meResult').textContent = '';

  if (file === '::assets') {
    $('meToolbar').style.display = 'none';
    $('meText').style.display = 'none';
    $('mePreview').style.display = 'none';
    $('meAssets').style.display = 'block';
    renderAssets();
    return;
  }
  $('meAssets').style.display = 'none';
  $('meToolbar').style.display = 'flex';

  const isActivity = file.startsWith('activities/');
  const isReview = file.startsWith('review/');
  $('meFileDeleteBtn').style.display = (isActivity || isReview) ? 'inline-block' : 'none';

  const res = await fetch('/api/file?module=' + encodeURIComponent(curTopic) +
                          '&path=' + encodeURIComponent(curPath) +
                          '&file=' + encodeURIComponent(file)).then(r => r.json());
  $('meText').value = res.content || '';
  const isDemo = file.startsWith('demos/');
  $('meModePreview').textContent = isDemo ? 'Live Preview' : 'Canvas Preview';
  $('meEngine').textContent = isActivity ? 'saving re-syncs the README toggle automatically' : '';
  setMode(isDemo ? 'preview' : 'edit');
}

function setMode(mode) {
  $('meModeEdit').classList.toggle('active', mode === 'edit');
  $('meModePreview').classList.toggle('active', mode === 'preview');
  $('meText').style.display = mode === 'edit' ? 'block' : 'none';
  $('mePreview').style.display = mode === 'preview' ? 'block' : 'none';
  if (mode === 'preview') renderPreview();
}

async function renderPreview() {
  const isDemo = curFile && curFile.startsWith('demos/');
  $('mePreview').classList.toggle('demo', isDemo);
  if (isDemo) {
    $('mePreview').innerHTML = '';
    const frame = document.createElement('iframe');
    frame.className = 'demoframe';
    frame.srcdoc = $('meText').value;
    $('mePreview').appendChild(frame);
    return;
  }
  const res = await fetch('/api/render', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({markdown: $('meText').value, base_path: curTopic + '/' + curPath}),
  }).then(r => r.json());
  $('mePreview').innerHTML = res.html || '';
  if (window.MathJax && MathJax.typesetPromise) {
    if (MathJax.typesetClear) MathJax.typesetClear([$('mePreview')]);
    MathJax.typesetPromise([$('mePreview')]).catch(() => {});
  }
}

function markDirty() { dirty = true; }

async function saveFile() {
  if (!curFile || curFile === '::assets') return;
  let res;
  if (curFile.startsWith('activities/')) {
    res = await fetch('/api/editor/activity', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({topic: curTopic, path: curPath, op: 'save',
                            file: curFile.replace('activities/', ''), content: $('meText').value}),
    }).then(r => r.json());
  } else {
    res = await fetch('/api/file', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({module: curTopic, path: curPath, file: curFile, content: $('meText').value}),
    }).then(r => r.json());
  }
  if (res.error) { $('meResult').innerHTML = '<span class="result-err">✕ ' + esc(res.error) + '</span>'; return; }
  dirty = false;
  const extra = res.readme_synced ? ' · README toggle synced' : '';
  $('meResult').innerHTML = res.broken_links && res.broken_links.length
    ? '<span class="result-err">Saved, but broken links: ' + res.broken_links.map(esc).join(', ') + '</span>'
    : '<span class="result-ok">✓ Saved' + extra + '</span>';
}

// ── assets (uploads) ──────────────────────────────────────────────────────────

function fmtSize(n) {
  if (n >= 1048576) return (n / 1048576).toFixed(1) + ' MB';
  if (n >= 1024)    return Math.round(n / 1024) + ' KB';
  return n + ' B';
}

function assetSnippet(name) {
  const img = /\.(png|jpe?g|gif|svg|webp)$/i.test(name);
  const label = name.replace(/\.[^.]+$/, '').replace(/[-_]/g, ' ');
  return img ? '![' + label + '](assets/' + name + ')' : '[' + label + '](assets/' + name + ')';
}

function renderAssets() {
  const items = listing.assets || [];
  $('meAssetList').innerHTML = items.length ? items.map(a =>
    '<div class="me-asset">' +
      '<span class="me-asset-name">' + esc(a.name) + '</span>' +
      '<span class="me-asset-size">' + fmtSize(a.size) + '</span>' +
      '<button class="btn-icon" onclick="Editor.copySnippet(\'' + a.name + '\')">Copy link snippet</button>' +
      '<button class="btn-icon me-danger" onclick="Editor.openDeleteAsset(\'' + a.name + '\')">Delete</button>' +
    '</div>'
  ).join('') : '<div class="pal-note">Nothing uploaded for this lesson yet.</div>';
}

function copySnippet(name) {
  navigator.clipboard.writeText(assetSnippet(name))
    .then(() => toast('Copied: ' + assetSnippet(name)))
    .catch(() => toast('Copy failed — snippet: ' + assetSnippet(name)));
}

async function uploadAsset(input) {
  const f = input.files[0];
  input.value = '';
  if (!f) return;
  const fd = new FormData();
  fd.append('module', curTopic);
  fd.append('path', curPath);
  fd.append('file', f);
  const res = await fetch('/api/editor/upload', {method: 'POST', body: fd}).then(r => r.json());
  if (res.error) { toast('✕ ' + res.error); return; }
  listing.assets = res.assets;
  buildTabs();
  $(tabId('::assets')).classList.add('active');
  renderAssets();
  navigator.clipboard.writeText(res.snippet).catch(() => {});
  toast('Uploaded ' + res.uploaded + ' — snippet copied');
}

// ── modals ────────────────────────────────────────────────────────────────────

const MODALS = ['meNewTopic', 'meNewLesson', 'meRename', 'meDelete', 'meNewFile'];
function showModal(name) {
  $(name + 'Overlay').style.display = 'block';
  $(name + 'Modal').style.display = 'flex';
}
function closeModals() {
  MODALS.forEach(m => { $(m + 'Overlay').style.display = 'none'; $(m + 'Modal').style.display = 'none'; });
  pendingDelete = null;
}

function openNewTopic() {
  ['mtFolder', 'mtTitle', 'mtSummary', 'mtLessonFolder', 'mtLessonTitle'].forEach(id => $(id).value = '');
  $('mtResult').textContent = '';
  showModal('meNewTopic');
}

async function createTopic() {
  const res = await fetch('/api/editor/topics', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      folder: $('mtFolder').value, title: $('mtTitle').value, summary: $('mtSummary').value,
      type_label: $('mtType').value,
      lesson: {folder: $('mtLessonFolder').value, title: $('mtLessonTitle').value},
    }),
  }).then(r => r.json());
  if (res.error) { $('mtResult').innerHTML = '<span class="result-err">✕ ' + esc(res.error) + '</span>'; return; }
  closeModals();
  topics = await fetch('/api/topics?with_lessons=1').then(r => r.json()).then(r => r.topics || []);
  renderTopicList();
  await pickTopic(res.created);
  toast('Created topic ' + res.created + ' — root README and CLAUDE.md updated');
}

function openNewLesson() {
  if (!curTopic) return;
  ['mlFolder', 'mlTitle', 'mlSubtitle'].forEach(id => $(id).value = '');
  $('mlDuration').value = 1;
  $('mlResult').textContent = '';
  const sel = $('mlPosition');
  sel.innerHTML = lessons.map((a, i) =>
    '<option value="' + i + '">Before ' + esc(a.title) + '</option>').join('') +
    '<option value="' + lessons.length + '" selected>At the end</option>';
  showModal('meNewLesson');
}

async function createLesson() {
  const res = await fetch('/api/editor/lessons', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      topic: curTopic, op: 'create',
      folder: $('mlFolder').value, title: $('mlTitle').value, subtitle: $('mlSubtitle').value,
      type_label: $('mlType').value, duration: parseInt($('mlDuration').value) || 1,
      position: parseInt($('mlPosition').value),
    }),
  }).then(r => r.json());
  if (res.error) { $('mlResult').innerHTML = '<span class="result-err">✕ ' + esc(res.error) + '</span>'; return; }
  closeModals();
  await reloadLessons();
  await pickLesson($('mlFolder').value);
  toast('Created — LESSONS.md, READMEs, CLAUDE.md and navs updated');
}

function openRename() {
  if (!curPath) return;
  $('mrFolder').value = curPath;
  $('mrTitle').value = curTitle;
  $('mrResult').textContent = '';
  const mods = impact.modules || [], scheds = impact.schedules || [];
  $('mrImpact').innerHTML = (mods.length || scheds.length)
    ? 'References in ' + [mods.length && (mods.length + ' curated module(s)'),
                          scheds.length && (scheds.length + ' schedule(s)')].filter(Boolean).join(' and ') +
      ' will be rewritten automatically.'
    : 'No curated module references this lesson — only this topic’s files change.';
  showModal('meRename');
}

async function doRename() {
  const res = await fetch('/api/editor/lessons', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({topic: curTopic, op: 'rename', path: curPath,
                          new_folder: $('mrFolder').value, new_title: $('mrTitle').value}),
  }).then(r => r.json());
  if (res.error) { $('mrResult').innerHTML = '<span class="result-err">✕ ' + esc(res.error) + '</span>'; return; }
  closeModals();
  const newPath = $('mrFolder').value;
  await reloadLessons();
  await pickLesson(newPath);
  toast('Renamed' + (res.modules_updated && res.modules_updated.length
    ? ' — updated modules: ' + res.modules_updated.join(', ') : ''));
}

// ── deletes (typed confirmation) ──────────────────────────────────────────────

function openDeleteLesson() {
  if (!curPath) return;
  const mods = impact.modules || [];
  if (mods.length) {
    $('mdHead').textContent = 'Cannot Delete Lesson';
    $('mdMessage').innerHTML = '<strong>' + esc(curTopic + '/' + curPath) + '</strong> is referenced by curated module' +
      (mods.length > 1 ? 's' : '') + ' ' + mods.map(m => '<strong>' + esc(m.name) + '</strong>').join(', ') +
      '. Remove it from those modules in the Module Planner first — the hub never deletes content out from under a saved plan.';
    $('mdTypedField').style.display = 'none';
    $('mdConfirmBtn').style.display = 'none';
    pendingDelete = null;
  } else {
    $('mdHead').textContent = 'Delete Lesson';
    $('mdMessage').innerHTML = 'This permanently deletes <strong>' + esc(curTopic + '/' + curPath) +
      '</strong> and everything inside it (activities, reviews, demos, assets), and updates every index file.';
    $('mdTypedField').style.display = 'block';
    $('mdTypedTarget').textContent = curPath;
    $('mdTyped').value = '';
    $('mdConfirmBtn').style.display = 'inline-block';
    pendingDelete = {kind: 'lesson', typed: curPath};
  }
  $('mdResult').textContent = '';
  showModal('meDelete');
}

function openDeleteFile(kind, file) {
  $('mdHead').textContent = kind === 'review' ? 'Delete Review File' : 'Delete Activity';
  $('mdMessage').innerHTML = 'This permanently deletes <strong>' + esc(file) + '</strong>' +
    (kind === 'activity' ? ' and removes its embedded toggle from the README.' : '.');
  $('mdTypedField').style.display = 'none';
  $('mdConfirmBtn').style.display = 'inline-block';
  $('mdResult').textContent = '';
  pendingDelete = {kind, file};
  showModal('meDelete');
}

function deleteCurrentFile() {
  if (!curFile) return;
  if (curFile.startsWith('review/')) openDeleteFile('review', curFile);
  else if (curFile.startsWith('activities/')) openDeleteFile('activity', curFile);
}

function openDeleteAsset(name) {
  $('mdHead').textContent = 'Delete Uploaded File';
  $('mdMessage').innerHTML = 'This permanently deletes <strong>assets/' + esc(name) +
    '</strong>. The hub refuses if any markdown in this topic still links to it.';
  $('mdTypedField').style.display = 'none';
  $('mdConfirmBtn').style.display = 'inline-block';
  $('mdResult').textContent = '';
  pendingDelete = {kind: 'asset', file: name};
  showModal('meDelete');
}

async function doDelete() {
  if (!pendingDelete) return;
  const p = pendingDelete;
  if (p.kind === 'lesson' && $('mdTyped').value !== p.typed) {
    $('mdResult').innerHTML = '<span class="result-err">✕ Type the folder name exactly to confirm</span>';
    return;
  }
  let res;
  if (p.kind === 'lesson') {
    res = await fetch('/api/editor/lessons', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({topic: curTopic, op: 'delete', path: curPath, confirm: $('mdTyped').value}),
    }).then(r => r.json());
  } else if (p.kind === 'review' || p.kind === 'activity') {
    res = await fetch('/api/editor/' + (p.kind === 'review' ? 'review' : 'activity'), {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({topic: curTopic, path: curPath, op: 'delete',
                            file: p.file.replace(/^(review|activities)\//, ''), confirm: true}),
    }).then(r => r.json());
  } else {
    res = await fetch('/api/editor/asset-delete', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({topic: curTopic, path: curPath, file: p.file, confirm: true}),
    }).then(r => r.json());
  }
  if (res.error) {
    $('mdResult').innerHTML = '<span class="result-err">✕ ' + esc(res.error) +
      (res.referenced_by ? '<br>' + res.referenced_by.map(esc).join('<br>') : '') + '</span>';
    return;
  }
  closeModals();
  if (p.kind === 'lesson') {
    curPath = null;
    $('meWork').style.display = 'none';
    $('meEmpty').style.display = 'block';
    await reloadLessons();
    toast('Deleted — all index files updated');
  } else {
    await pickLesson(curPath);
    toast('Deleted ' + (res.deleted || p.file));
  }
}

// ── new review / activity ─────────────────────────────────────────────────────

let newFileKind = null;

// Intention prompts appended after the lesson's full text bundle — the whole
// thing is copied in one click and pasted straight into an AI chat.
const REVIEW_AI_PROMPT =
  'I need to make a review based on this lesson, assignment, and attached reviews or ' +
  'activities if they are included. The review should cover a small section of this ' +
  'content and motivate the concepts here from another angle and with direct explanation ' +
  'and additional questions to check for understanding. Format it as a standalone review ' +
  'fragment: "# Review — [Concept Name]", then "*Originally covered in [Lesson Title](../README.md)*", ' +
  'a terse reference table (commands/syntax only, no explanations), then a numbered ' +
  '"## Tasks" list of concrete actions the student performs.';

const ACTIVITY_AI_PROMPT =
  'I need to make a short in-lecture activity based on this lesson, assignment, and ' +
  'attached reviews or activities if they are included. The activity should prove one ' +
  'concept from this content hands-on in a few minutes, motivating it from another angle ' +
  'than the lecture, with concrete numbered steps a student can follow without extra ' +
  'instructions. Format: "# Activity — [Title]", then "*Concept: [one sentence naming ' +
  'the idea this activity proves]*", then "## Task" with numbered steps.';

let aiPromptFull = '';   // real multi-line prompt; the textarea shows a one-line condensed view

async function loadAiPrompt(intent) {
  aiPromptFull = '';
  $('mfAiText').value = 'Collecting lesson text…';
  const res = await fetch('/api/editor/bundle?module=' + encodeURIComponent(curTopic) +
                          '&path=' + encodeURIComponent(curPath)).then(r => r.json());
  aiPromptFull = (res.text || '') + '\n\n' + intent;
  $('mfAiText').value = aiPromptFull.replace(/\s+/g, ' ').trim();
}

function copyAiPrompt() {
  if (!aiPromptFull) { toast('Still collecting lesson text…'); return; }
  navigator.clipboard.writeText(aiPromptFull)
    .then(() => toast('AI prompt copied (' + aiPromptFull.length + ' chars) — paste it into chat'))
    .catch(() => toast('Copy failed — select the text manually'));
}

function openNewReview() {
  newFileKind = 'review';
  $('mfHead').textContent = 'New Review File';
  $('mfLabel1').textContent = 'Concept name';
  $('mfName').value = ''; $('mfName').placeholder = 'e.g. Branch and Merge Basics';
  $('mfConceptField').style.display = 'none';
  $('mfHint').textContent = 'Creates review/<concept-kebab>.md with the standard terse-reference + Tasks scaffold. Attach it to assignments in the Module Planner.';
  $('mfResult').textContent = '';
  loadAiPrompt(REVIEW_AI_PROMPT);
  showModal('meNewFile');
}

function openNewActivity() {
  newFileKind = 'activity';
  $('mfHead').textContent = 'New Activity';
  $('mfLabel1').textContent = 'Activity title';
  $('mfName').value = ''; $('mfName').placeholder = 'e.g. The Hidden Detective';
  $('mfConceptField').style.display = 'block';
  $('mfConcept').value = '';
  $('mfHint').textContent = 'Creates activities/NN-<title-kebab>.md and inserts the collapsed "Activity: [Title]" toggle into the README (above Check for Understanding — move it in the README editor if it belongs elsewhere).';
  $('mfResult').textContent = '';
  loadAiPrompt(ACTIVITY_AI_PROMPT);
  showModal('meNewFile');
}

async function createFile() {
  let res;
  if (newFileKind === 'review') {
    res = await fetch('/api/editor/review', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({topic: curTopic, path: curPath, op: 'create', concept: $('mfName').value}),
    }).then(r => r.json());
  } else {
    res = await fetch('/api/editor/activity', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({topic: curTopic, path: curPath, op: 'create',
                            title: $('mfName').value, concept: $('mfConcept').value}),
    }).then(r => r.json());
  }
  if (res.error) { $('mfResult').innerHTML = '<span class="result-err">✕ ' + esc(res.error) + '</span>'; return; }
  closeModals();
  await pickLesson(curPath);
  openTab(res.created);
  toast('Created ' + res.created + (res.readme_synced ? ' — toggle added to README' : ''));
}

return {init, onShow, pickTopic, pickLesson, moveLesson, openTab, setMode, saveFile, markDirty,
        copySnippet, uploadAsset, closeModals,
        openNewTopic, createTopic, openNewLesson, createLesson,
        openRename, doRename, openDeleteLesson, deleteCurrentFile, openDeleteAsset, doDelete,
        openNewReview, openNewActivity, createFile, copyAiPrompt};
})();
