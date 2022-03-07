import asyncio
from pyppeteer import launch
import time
import random
import string


def gen_credentials():
    return "".join(
        [
            random.choice(list(string.ascii_letters + string.digits))
            for _ in range(random.randint(10, 15))
        ]
    )


def gen_email():
    return f"{gen_credentials()}@mail.ru"


async def main():
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto("https://nftines.city-mobil.ru/")
    await page.click('div[data-type="iText"]')

    await page.evaluate(
        """() => {
        uploadImage()
    }"""
    )

    await page.evaluate(
        """() => {
        document.getElementsByClassName('editor__share-wrapper editor__right-block hidden')[0].classList.remove('hidden')
    }"""
    )

    time.sleep(6)
    await page.evaluate(
        """() => {
        document.getElementsByClassName("editor__share-email")[0].value ="""
        + f"'{gen_email()}'"
        + """
    }"""
    )
    await page.click('div[class="editor__share-button button"]')

    time.sleep(4)

    promo = await page.evaluate(
        """document.getElementsByClassName("editor__final-promo")[0].textContent"""
    )
    print(promo)
    if promo == "ПРОМОКОД":
        await browser.close()
    else:
        open("codes.txt", "a").write(promo + "\n")
        await browser.close()


while True:
    asyncio.get_event_loop().run_until_complete(main())
    input()
