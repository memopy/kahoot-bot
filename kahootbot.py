from playwright.async_api import async_playwright
from random import choices
from string import ascii_lowercase,ascii_uppercase
from time import sleep
import asyncio

async def main():
    def sumStr(list_):
        new = ""
        for i in list_:
            new += i
        return new

    abcList = [i for i in ascii_lowercase] + [i for i in ascii_uppercase]

    gameId = input("enter a game pin:")
    botNamePrefix = input("enter the name prefix:")
    botCount = int(input("enter the bot count(max 40):"))
    browsers = []
    pages = []

    print("the botting is starting")

    print("%0")
    session = await async_playwright().start()
    browser = await session.chromium.launch()
    print("%5")
    async def getready(x):
        name = botNamePrefix + "_" + sumStr(choices(abcList,k=5))
        await x.goto("https://kahoot.it",wait_until="load")
        await x.locator("input#game-input").fill(str(gameId))
        await x.locator("button.button__Button-sc-vzgdbz-0").click()
        await x.wait_for_load_state("load")
        await x.locator("input#nickname").fill(name) 
    
    for i in range(botCount):
        browsers.append(await browser.new_context(java_script_enabled=True))
    print("%15")
    for i in browsers:
        pages.append(await i.new_page())
    print("%30")
    taskList = []
    for i in pages:
        taskList.append(asyncio.create_task(getready(i)))
    await asyncio.gather(*taskList)
    print("%80")
    for i in pages:
        await i.locator("button.button__Button-sc-vzgdbz-0").click()
    print("%100")
    print("the bots are sent. waiting a second to avoid any error.")
    sleep(1.0)
    print("exiting")
    await browser.close()
    await session.stop()
       
asyncio.run(main())
