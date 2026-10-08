// Renders every figures/*.svg to a 2x PNG with Chromium (correct Persian shaping and bidi).
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
const dir = path.join(__dirname, '..', 'figures');
const font = 'file:///home/user/shop/frontend/node_modules/vazirmatn/misc/UI-Farsi-Digits/fonts/webfonts/';
(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox'] });
  for (const file of fs.readdirSync(dir).filter(f => f.endsWith('.svg'))) {
    const svg = fs.readFileSync(path.join(dir, file), 'utf8');
    const [, w, h] = svg.match(/width="(\d+)" height="(\d+)"/);
    const page = await browser.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: 2 });
    const css = ['Regular:400', 'Medium:500', 'Bold:700'].map(x => { const [n, wt] = x.split(':'); return `@font-face{font-family:'Vazirmatn UI FD';font-weight:${wt};src:url('${font}Vazirmatn-UI-FD-${n}.woff2')}`; }).join('');
    await page.setContent(`<style>${css}body{margin:0}</style>${svg}`);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(150);
    await page.screenshot({ path: path.join(dir, file.replace('.svg', '.png')) });
    await page.close();
  }
  await browser.close();
  console.log('png done');
})();
