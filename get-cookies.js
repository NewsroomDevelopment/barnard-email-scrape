const puppeteer = require("puppeteer");
require("dotenv").config();

const destinationURI = "https://directory.columbia.edu/people/search";
const authenticationURL =
  "http://cas.columbia.edu/cas/login?TARGET=" +
  encodeURIComponent(destinationURI);

async function init() {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto(authenticationURL);

  // Type in username and password
  await page.type("#username", process.env.USERNAME);
  await page.type("#password", process.env.PASSWORD);

  // Submit form and wait for network activity to finish (i.e. redirect finished)
  await Promise.all([
    page.evaluate(
      (selector) => document.querySelector(selector).click(),
      "[type=submit]"
    ),
    page.waitForNavigation({ waitUntil: "networkidle0" }),
  ]);

  // Send cookies as JSON to stdout
  const cookies = await page.cookies();
  console.log(
    JSON.stringify(
      cookies.reduce((acc, val) => {
        acc[val.name] = val.value;
        return acc;
      }, {})
    )
  );

  await page.close();
  await browser.close();
}

init().catch(console.error);
