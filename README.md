# James Oneyibo — professional portfolio

Static HTML/CSS portfolio for GitHub Pages. No application framework, package manager, runtime dependencies or backend is required. Existing legacy assets are retained for history; the new pages do not load the old animation/Angular stack.

## Edit and build

Update `data/profile.json` (English) and `data/profile.fi.json` (Finnish), then run `python3 scripts/build.py`. Both language entry points and the printable/downloadable resumes are generated from their complete localized content. Keep project status, employment details, dates and links synchronized in both data files. Proper names and technology names retain their original spelling. The Finnish page links to `resume-fi.html`, `resume-fi.pdf` and `resume-fi.txt`; the English versions remain at `resume.html`, `resume.pdf` and `resume.txt`.

Run `python3 scripts/check.py` and `node --check js/resume.js`. Preview with `python3 -m http.server 8000`. GitHub Pages serves the repository root directly; there is no Node lint/type-check/build pipeline to run.

See `CONTENT_RECOVERY.md` for recovered details, evidence, corrections and remaining assets. Downloadable resumes are PDF and plain text. After changing content, regenerate both PDFs and social preview PNGs using `node scripts/browser-check.cjs /tmp/oneyibo-portfolio-qa/node_modules` after installing optional QA dependencies with `npm install --prefix /tmp/oneyibo-portfolio-qa playwright @sparticuz/chromium`. These tools stay outside the site and are not runtime dependencies. The HTML resume also supports browser Print / Save as PDF.
