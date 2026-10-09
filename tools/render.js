// usage: node render.js <svgPath> <outPrefix> <t1,t2,...|static>
const { chromium } = require('playwright-core');
const path = require('path');
(async () => {
  const [svg, outPrefix, times] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
  const page = await browser.newPage();
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push(String(e)));
  await page.goto('file:///' + path.resolve(svg).replace(/\\/g, '/'));
  const size = await page.evaluate(() => {
    const r = document.documentElement; return { w: +r.getAttribute('width'), h: +r.getAttribute('height') };
  });
  await page.setViewportSize({ width: size.w, height: size.h });
  await page.evaluate(() => document.fonts.ready);
  const fontsOk = await page.evaluate(() => [...document.fonts].map(f => f.family + ':' + f.weight + ':' + f.status));
  console.log('fonts', fontsOk.join(' '));
  if (times === 'static') {
    await page.evaluate(() => {
      document.querySelectorAll('animate,animateTransform,animateMotion,set').forEach(e => e.remove());
      const s = document.createElementNS('http://www.w3.org/2000/svg', 'style');
      s.textContent = '*{animation:none!important}';
      document.documentElement.appendChild(s);
    });
    await page.waitForTimeout(100);
    await page.screenshot({ path: `${outPrefix}-static.png` });
  } else {
    for (const tt of times.split(',').map(Number)) {
      await page.evaluate((t) => {
        const r = document.documentElement;
        r.pauseAnimations(); r.setCurrentTime(t);
        document.getAnimations().forEach(a => { a.pause(); a.currentTime = t * 1000; });
      }, tt);
      await page.waitForTimeout(80);
      await page.screenshot({ path: `${outPrefix}-t${String(tt).replace('.', '_')}.png` });
    }
  }
  if (errors.length) console.log('ERRORS', errors);
  await browser.close();
})();
