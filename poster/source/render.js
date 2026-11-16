// Make the two A3 PDFs and a preview from poster.html.
// usage (from poster/source): node render.js <output folder>      needs: npm i playwright (and a Chromium)
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const out = path.resolve(process.argv[2] || '..');
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || undefined});
  for (const [name, blank] of [['with_qr', false], ['blank', true]]) {
    const p = await b.newPage({ viewport: { width: 1123, height: 1587 }, deviceScaleFactor: 1.5 });
    await p.goto('file://' + path.resolve('poster.html'));
    await p.evaluate(v => { document.body.className = v ? 'blank' : ''; }, blank);
    await p.waitForTimeout(1200);
    if (!blank) await p.screenshot({ path: path.join(out, 'HOUSE_QUIZ_RALLY_A3_preview.png') });
    await p.pdf({ path: path.join(out, 'HOUSE_QUIZ_RALLY_A3_' + name + '.pdf'), width: '297mm', height: '420mm', printBackground: true, pageRanges: '1' });
    await p.close();
  }
  await b.close();
})();
