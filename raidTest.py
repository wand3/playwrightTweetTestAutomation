#!/usr/bin/env python3
import os
import typing
import asyncio
import json
import logging
import random
from playwright.async_api import Playwright, async_playwright, expect
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

        try:
            # go to search
            await expect(page.get_by_label('Search and explore')).to_be_visible()
            search_icon = page.get_by_label('Search and explore')
            logging.info("Search button seen successfully!")
            search_pos = await search_icon.bounding_box()
            await page.mouse.move(search_pos['x'] + search_pos['width'] / 2, search_pos['y'] + search_pos['height'] / 2)
            await page.mouse.down()
            await page.mouse.up()
            logging.info("Search button clicked successfully!")
            await page.wait_for_load_state()
            await asyncio.sleep(random.randint(2, 7))

            # search input box
            s_input = page.get_by_placeholder("Search")
            s_input_pos = await s_input.bounding_box()
            await page.mouse.move(s_input_pos['x'] + s_input_pos['width'] / 2, s_input_pos['y'] + s_input_pos['height'] / 2)
            await page.mouse.down()
            await page.mouse.up()
            logging.info("Search box clicked successfully!")
            await asyncio.sleep(random.randint(1, 3))

            # input search token
            await page.keyboard.type('$wan', delay=900)
            logging.info("Search input filled successfully!")
            # submit search
            await page.keyboard.press("Enter")
            await page.wait_for_load_state()
            await asyncio.sleep(random.randint(3, 8))

            # number of times for raid
            n_raids = 3
            # valid tweets for raids count
            all_stat = []
            post_stats = []
            tweet_count = 0

            for i in range(n_raids):
                await asyncio.sleep(random.randint(1, 3))
                # get all tweets with above 2k impressions, has_text of search keyword
                all_t = await page.query_selector_all("article")
                # get all impressions
                impre = await page.query_selector_all('div[role="group"]')

                statistics = []
                links = []
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
                post_stats = statistics
                print(set(post_stats))
                print(links)
                # get all tweets or articles on each page scroll
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")


                # method2
                # get post link of each post from analytics and trim
                # on each post with sufficient impressions open link of post in new tab

                logging.info(f"Scroll {i} successful!")




        # scroll search results
        # if search meets a particular number of likes click on post
        # like, retweet, replay at random and book mark for raids
        except Exception as e:
            logging.error("Unable to click search on home page")
            logging.error(f"Failed reason {e}")






    await context.close()

asyncio.run(shill())
