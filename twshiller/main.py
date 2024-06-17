#!/usr/bin/env python3
import os
import typing
import asyncio
import json
import logging
import random
from playwright.async_api import Playwright, async_playwright
from bs4 import BeautifulSoup
import requests
import re
from clean import get_link

# Configure logging to display messages to the terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler()])



# load cookies if it exists
async def load_cookies(context, file_path):
    with open(file_path, 'r') as f:
        cookies = json.load(f)
        await context.add_cookies(cookies)


async def shill():
    async with async_playwright() as p:
        # browser configs
        browser = await p.firefox.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 375, "height": 812},  # iPhone X viewport size
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
        )

        await load_cookies(context, "cookies.json")
        logging.info("Session cookies loaded succesfully")

        page = await context.new_page()
        page.set_default_timeout(55000)
        await page.goto('https://x.com/')
        logging.info("Session continued")
        await page.wait_for_load_state()

        home_scroll = random.randrange(3, 6)
        count = 0
        while count < home_scroll:

            post_link = []
            # get height of page
            last_height = await page.evaluate("document.body.scrollHeight")
            # counter for number of pages to scroll

            logging.info(f"Home page random scroll for {home_scroll} times")

            # scroll each page to bottom
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")

            await page.wait_for_load_state()
            new_height = await page.evaluate("document.body.scrollHeight")
            last_height = new_height

            # get all tweets or articles on each page scroll
            articles = await page.query_selector_all('article')
            data = []
            for article in articles:
                tweet = await article.inner_html()
                """
                    soup = BeautifulSoup(tweet, "html.parser")
    
                    # get all links
                    links = soup.find_all("a")
                    for i in links:
                        # get href attributes
                        alinks = i.get('href')
                        data.append(alinks)
                    # try:
                    # except Exception as e:
                    #     logging.error("Didn't get like, retweets, views etc")
                 """
                data.append(tweet)
                post_link.append(data)
            print(data)
            print(post_link)
        # Save the text to a file
        # with open('output.txt', 'w') as file:
        #     for text in its:
        #         file.write(str(text))
        #
        # print(f"Text saved to file")

        # automate the process

        await asyncio.sleep(random.randint(8, 10))

    await context.close()

asyncio.run(shill())
