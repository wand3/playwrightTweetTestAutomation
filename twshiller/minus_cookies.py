#!/usr/bin/env python3
import asyncio
import json
import logging
import random
from playwright.async_api import Playwright, async_playwright
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


async def hill():
    async with async_playwright() as p:
        # browser configs
        browser = await p.firefox.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 375, "height": 812},  # iPhone X viewport size
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
        )
        await load_cookies(context, "cookies.json")
        logging.info("Session cookies loaded succesfully")

        url = 'https://x.com/'
        page = await context.new_page()
        # await page.goto('https://x.com/')

        logging.info("Session continued")

        # beautiful soup config
        # sp = await page.goto(url)
        await page.goto(url)
        await page.get_by_test_id("tweet").is_visible()
        resp = await page.content()

        await asyncio.sleep(random.randint(8, 10))


        soup = BeautifulSoup(resp, "html.parser")
        # print(soup)
        posts = soup.find_all('div', {"data-testid": "cellInnerDiv"})
        await asyncio.sleep(random.randint(8, 10))

        print(len(posts))
        print(posts)

        data = []
        for p in posts:
            item = {}
            item['Title'] = p.find("span")
            data.append(item)
        print(data)
        # scroll home page
        # for i in range(1, 2):
        #     await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
        #     logging.info(f"Page {i} scrolled")
        #
        #     # get all tweets from page one
        #     article_elements = await page.query_selector_all('article')
        #
        #     # Scroll through each article element
        #     for article_element in article_elements:
        #         await page.evaluate('(element) => { element.scrollIntoView(); }', article_element)
        #         # Wait for a short time to allow for visual inspection
        #         await asyncio.sleep(4)
        #
        #         logging.info(f"Element {article_element} viewed")
        #     article_elements.clear()
        #
        #     # wait for a while after each page
        #     await asyncio.sleep(random.randint(5, 10))

        # get and click on search button
        # await page.get_by_test_id("AppTabBar_Explore_Link").click()
        # await page.get_by_test_id("SearchBox_Search_Input").fill("$smole")
        # await page.get_by_test_id("SearchBox_Search_Input").press("Enter")
        # logging.info("Search loaded succesfully")

        # scroll through each search result
        # for i in range(1, 2):
        #     await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
        #     logging.info(f"Page {i} scrolled")

            # get all tweets from page one
            # search_elements = await page.query_selector_all('article')

            # Scroll through each article element
            # for search_element in search_elements:
            #     await page.evaluate('(element) => { element.scrollIntoView(); }', search_element)
            #     # Wait for a short time to allow for visual inspection
            #     await asyncio.sleep(4)
            #
            #     # click each search post to open in new tab
            #     await search_element.click(button='middle', modifiers=['Shift'])
            #     await asyncio.sleep(3)
            #
            #     # wait for new tab to open
            #     new_page = await context.wait_for_event("page")
            #     # switch to new tab
            #     await new_page.bring_to_front()
            #
            #     # await new_page.get_by_test_id("reply").click()
            #     logging.info("Reply of post clicked")
            #     # await new_page.get_by_label("Post text").fill("lfg")
            #     logging.info("Post section filled")
            #     await new_page.get_by_test_id("tweetButton").click()
            #     await new_page.go_back()
            #
            #     '''
            #     # click each search post to open in new tab
            #     await article_element.click(button='middle', modifiers=['Shift'])
            #     await asyncio.sleep(3)
            #
            #     # wait for new tab to open
            #     new_page = await context.wait_for_event("page")
            #     # switch to new tab
            #     await new_page.bring_to_front()
            #
            #     # click the back button
            #     await new_page.get_by_test_id("app-bar-back").click()
            #     # check for number in impressions
            #
            #     # views_spans = await new_page.query_selector_all('span')
            #     # for j in views_spans:
            #     #     print(j)
            #
            #     logging.info("Post has been clicked")
            #
            #     # await new_page.close()
            #     '''
            #     logging.info("Successfully moved out of post")
            #     logging.info("Post viewed succesfully")
            #     await asyncio.sleep(3)
            #
            #     logging.info(f"Element {search_element} viewed")
            #     # article_elements.pop()

            # wait for a while after each page
    await asyncio.sleep(random.randint(5, 15))

    await context.close()

asyncio.run(hill())
