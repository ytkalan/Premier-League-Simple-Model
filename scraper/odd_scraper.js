const puppeteer = require('puppeteer');

// use node odd_scraper.js
const scrape = async (url) => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    const result = [];
    await page.goto(url, {waitUntil: 'networkidle2'});
    await page.waitForSelector('#col-content > #tournamentTable > #tournamentTable > tbody')
    const data = await page.evaluate(() => {
        const rows = Array.from(document.querySelectorAll(
            '#col-content > #tournamentTable > #tournamentTable > tbody > .deactivate'
        ))
        return rows.map(td => td.innerHTML)
      });
    await browser.close();
    return data;
};

scrape('https://www.oddsportal.com/soccer/england/premier-league-2015-2016/results/#/page/1/').then((value) => {
    const result = value.map(data => {
        const regex = RegExp('odds_text');
        return regex.exec(data);
    });
    console.log(result);
    console.log(result.length);
});