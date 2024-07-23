#!/usr/bin/env python3
import os
import typing
import asyncio
import json
import logging
import random
from playwright.async_api import Playwright, async_playwright, expect
import time
from bs4 import BeautifulSoup
import requests
import re

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

        await load_cookies(context, "../twshiller/cookies.json")
        logging.info("Session cookies loaded succesfully")

        page = await context.new_page()
        page.set_default_timeout(55000)
        await page.goto('https://x.com/')
        logging.info("Session continued")
        await page.wait_for_load_state()

        # home_scroll = random.choice(range(1, 6))
        home_scroll = 5

        count = 0
        while count <= home_scroll:

            # get height of page
            last_height = await page.evaluate("document.body.scrollHeight")
            # counter for number of pages to scroll
            logging.info(f"Home page random scroll for {home_scroll} times")

            # scroll each page to bottom
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")

            await page.wait_for_load_state()
            new_height = await page.evaluate("document.body.scrollHeight")
            last_height = new_height

            # Get the page content
            html_code = await page.content()

            # get all tweets or articles on each page scroll
            soup = BeautifulSoup(html_code, 'html.parser')

            # Find all divs with the specified class
            all_divs = soup.find_all('div', class_='css-175oi2r r-18u37iz r-1q142lx')
            logging.info(f"{len(all_divs)}")

            # Extract href attributes from anchor tags within each div
            all_hrefs = []
            for div in all_divs:
                anchor_tag = div.find('a')
                logging.info(f"{anchor_tag}")
                if anchor_tag:
                    href = anchor_tag.get('href')
                    if href:
                        all_hrefs.append(href)

            # Print all extracted hrefs
            print(all_hrefs)
            print(len(all_hrefs))

            count += 1

        await asyncio.sleep(random.randint(2, 5))

    await context.close()

asyncio.run(shill())
# regex likes extraction
# get all impressions
# impre = await page.query_selector_all('div[role="group"]')

# method 1 get bounding box of article and hover
# for im in impre:
#     total_likes = 0
#     total_views = 0
#     stats = await im.get_attribute("aria-label")
#     all_stat.append(stats)
#     # define regex patterns
#     rlikes = r'(\d+)\s+likes'
#     rviews = r'(\d+)\s+views'
#     for values in all_stat:
#         # Use re.search() to find the pattern in the text
#         likes = re.search(rlikes, values)
#         views = re.search(rviews, values)
#
#         if likes and views:
#             # Extract the views count (first capturing group)
#             likes_count = likes.group(1)
#             views_count = views.group(1)
#             likes = int(likes_count)
#             views = int(views_count)
#             res = "Likes = " + likes_count + " Views = " + views_count
#             statistics.append(res)
