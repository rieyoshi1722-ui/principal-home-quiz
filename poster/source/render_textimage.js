// Poster PDFs whose lettering is an IMAGE (no fonts inside), plus the lettering alone as a transparent PNG.
// usage (from poster/source): node render_textimage.js <output folder>
const { chromium } = require('playwright');
const path = require('path');
const MM = 3.7795275591;                       // CSS px per mm
(async () => {
  const out = path.resolve(process.argv[2] || '..');
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
  const W = Math.round(297 * MM), H = Math.round(420 * MM);
  const SCALE = 3508 / W;                      // A3 at 300 dpi

  // 1) the lettering alone: everything that is not text is hidden
  let p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: SCALE });
  await p.goto('file://' + path.resolve('poster.html'));
  await p.evaluate(wrapText);
  await p.addStyleTag({ content: `
    .page{background:transparent!important}
    .page *{background:transparent!important;border-color:transparent!important;box-shadow:none!important}
    .bg,.cloud,img,svg,.sprite{visibility:hidden!important}
    html,body{background:transparent!important}` });
  await p.waitForTimeout(1200);
  const textPng = path.join(out, 'HOUSE_QUIZ_RALLY_A3_text_only.png');
  await p.screenshot({ path: textPng, omitBackground: true });
  await p.close();

  // 2) the poster with that lettering laid over it instead of live text
  for (const [name, blank] of [['with_qr', false], ['blank', true]]) {
    p = await b.newPage({ viewport: { width: W, height: H } });
    await p.goto('file://' + path.resolve('poster.html'));
    await p.evaluate(wrapText);
    await p.evaluate(v => { document.body.className = v ? 'blank' : ''; }, blank);
    await p.addStyleTag({ content: `.tx{visibility:hidden!important}
      .textlayer{position:absolute;left:0;top:0;width:297mm;height:420mm;z-index:99}` });
    await p.evaluate(src => { const i = document.createElement('img'); i.className = 'textlayer'; i.src = src; document.querySelector('.page').appendChild(i); }, 'file://' + textPng);
    await p.waitForTimeout(1500);
    await p.pdf({ path: path.join(out, 'HOUSE_QUIZ_RALLY_A3_' + name + '_textimage.pdf'), width: '297mm', height: '420mm', printBackground: true, pageRanges: '1' });
    await p.close();
  }
  await b.close();
})();

function wrapText() {
  // every piece of text goes in <x-t class="tx"> so it can be hidden or shown as a group
  const w = document.createTreeWalker(document.querySelector('.page'), NodeFilter.SHOW_TEXT);
  const nodes = []; while (w.nextNode()) nodes.push(w.currentNode);
  for (const n of nodes) {
    if (!n.nodeValue.trim() || n.parentElement.closest('style,script,svg')) continue;
    const s = document.createElement('x-t'); s.className = 'tx';   // a custom tag, so no style rule written for <span> or <b> applies to it
    n.parentNode.replaceChild(s, n); s.appendChild(n);
  }
}
