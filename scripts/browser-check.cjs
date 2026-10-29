// Optional browser QA and generated PDF/PNG artifacts; no site runtime dependencies.
'use strict';
const path = require('node:path');
const fs = require('node:fs');
const http = require('node:http');
const assert = require('node:assert/strict');
const { pathToFileURL } = require('node:url');
const root = path.resolve(__dirname, '..');
async function main() {
  const modules = process.argv[2];
  assert(modules, 'Usage: node scripts/browser-check.cjs /absolute/path/to/node_modules');
  const { chromium: playwright } = require(path.join(modules, 'playwright'));
  const chromium = (await import(pathToFileURL(path.join(modules, '@sparticuz/chromium/build/index.js')).href)).default;
  const server = http.createServer((req, res) => {
    const route = new URL(req.url, 'http://localhost').pathname;
    const file = path.resolve(root, '.' + (route === '/' ? '/index.html' : decodeURIComponent(route)));
    if (!file.startsWith(root + path.sep)) { res.writeHead(403); return res.end(); }
    fs.readFile(file, (err, data) => {
      if (err) { res.writeHead(404); return res.end('Missing'); }
      res.setHeader('Content-Type', ({'.html':'text/html', '.css':'text/css', '.js':'text/javascript', '.svg':'image/svg+xml', '.png':'image/png', '.pdf':'application/pdf'})[path.extname(file)] || 'text/plain');
      res.end(data);
    });
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const base = 'http://127.0.0.1:' + server.address().port;
  let browser;
  try {
    browser = await playwright.launch({ executablePath: await chromium.executablePath(), args: chromium.args, headless: true });
    const page = await browser.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('response', response => { if (response.status() >= 400) errors.push(response.status() + ' ' + response.url()); });
    for (const width of [375, 768, 1440]) {
      await page.setViewportSize({ width, height: 1000 });
      for (const file of ['index.html', 'en.html', 'resume.html', 'resume-fi.html']) {
        await page.goto(base + '/' + file, { waitUntil: 'networkidle' });
        const info = await page.evaluate(() => ({ overflow: document.documentElement.scrollWidth > innerWidth, headings: document.querySelectorAll('h1').length, projects: document.querySelectorAll('.project').length }));
        assert.deepEqual(info, { overflow: false, headings: 1, projects: 9 }, width + ' ' + file);
        console.log('PASS', width, file);
      }
    }
    await page.setViewportSize({width:1440,height:1000});
    await page.goto(base + '/en.html');
    await page.screenshot({path:'/tmp/oneyibo-portfolio-desktop.png'});
    await page.locator('a[href="#education"]').click();
    await page.locator('#education').scrollIntoViewIfNeeded();
    assert(await page.locator('#education h2').isVisible());
    await page.screenshot({path:'/tmp/oneyibo-portfolio-education.png'});
    await page.setViewportSize({width:375,height:900});
    await page.goto(base + '/en.html');
    await page.screenshot({path:'/tmp/oneyibo-portfolio-mobile.png'});
    await page.locator('a.language').click();
    assert.equal(await page.locator('html').getAttribute('lang'), 'fi');
    assert.equal(await page.locator('.hero .outline').getAttribute('href'), 'resume-fi.html');
    assert(await page.getByText('Vakituinen työntekijä', {exact:false}).isVisible());
    await page.locator('#project-1 summary').click();
    assert(await page.getByText('Android-sovellus kuljettajille', {exact:true}).isVisible());
    await page.setViewportSize({width:1440,height:1000});
    await page.locator('.hero').scrollIntoViewIfNeeded();
    await page.screenshot({path:'/tmp/oneyibo-portfolio-finnish.png'});
    await page.locator('.hero .outline').click();
    assert.equal(await page.locator('html').getAttribute('lang'), 'fi');
    assert.equal(await page.locator('h1').textContent(), 'James Oneyibo');
    assert(await page.getByRole('link', {name:'Lataa PDF-ansioluettelo',exact:true}).isVisible());
    if (fs.existsSync(path.join(root, 'resume-fi.pdf'))) {
    const downloadPromise = page.waitForEvent('download');
    await page.getByRole('link', {name:'Lataa PDF-ansioluettelo',exact:true}).click();
    const download = await downloadPromise;
    assert.equal(download.suggestedFilename(), 'resume-fi.pdf');
    assert.equal(await download.failure(), null);
    }
    await page.locator('a.language').click();
    assert.equal(await page.locator('html').getAttribute('lang'), 'en');
    assert(page.url().endsWith('/resume.html'));
    await page.setViewportSize({width:1200,height:630});
    for (const suffix of ['', '-fi']) {
      await page.emulateMedia({media:'screen'});
      await page.goto(base + '/img/social-card' + suffix + '.svg');
      await page.locator('svg').screenshot({path:path.join(root,'img/social-card' + suffix + '.png')});
      await page.goto(base + '/resume' + suffix + '.html');
      await page.emulateMedia({media:'print'});
      await page.pdf({path:path.join(root,'resume' + suffix + '.pdf'),format:'A4',margin:{top:'14mm',bottom:'14mm',left:'14mm',right:'14mm'}});
    }
    assert.deepEqual(errors, []);
    console.log('PASS: language switching, navigation, browser errors, local responses; PDF and PNG generated.');
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve));
  }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
