// Syllabus tab — renders the repo's live SYLLABUS.md, not a copy

window.Syllabus = (() => {
  async function init() {
    const view = document.getElementById('syllabusView');
    try {
      const res = await fetch('/api/syllabus').then(r => r.json());
      if (res.error) { view.innerHTML = `<p style="color:var(--red)">${esc(res.error)}</p>`; return; }
      view.innerHTML = res.html;
      if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([view]).catch(() => {});
    } catch (e) {
      view.innerHTML = `<p style="color:var(--red)">Failed to load syllabus: ${esc(e.message)}</p>`;
    }
  }

  return {init};
})();
