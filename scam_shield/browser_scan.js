const { chromium } = require('playwright');
const fs = require('fs');

async function scanClawHub() {
    const browser = await chromium.launch();
    const page = await browser.newPage();
    try {
        console.log("Navigiere zu ClawHub...");
        await page.goto('https://clawhub.ai/skills', { waitUntil: 'networkidle' });
        
        // Extrahiere alle Links, die /skill/ enthalten
        const links = await page.evaluate(() => {
            const anchors = Array.from(document.querySelectorAll('a'));
            return anchors
                .map(a => a.href)
                .filter(href => href.includes('/skill/'));
        });
        
        const uniqueLinks = [...new Set(links)];
        console.log(JSON.stringify(uniqueLinks, null, 2));
    } catch (error) {
        console.error("Browser-Scan fehlgeschlagen:", error.message);
    } finally {
        await browser.close();
    }
}

scanClawHub();
