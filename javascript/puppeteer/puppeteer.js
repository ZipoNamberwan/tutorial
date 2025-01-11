const puppeteer = require('puppeteer');
// Or import puppeteer from 'puppeteer-core';

async function main() {
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();

    await page.goto('https://www.tokopedia.com/');
}

main()