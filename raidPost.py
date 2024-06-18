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
        await page.goto('https://x.com/PaamanuelUtd_/status/1802604963262079044')
        logging.info("Session continued")
        await page.wait_for_load_state()

        tweetText = await page.query_selector_all('div[data-testid="tweetText"]')
        likeTweet = await page.query_selector_all('button[data-testid="like"]')
        unlikeTweet = await page.query_selector_all('button[data-testid="unlike"]')
        retweet = await page.query_selector_all('button[data-testid = "retweet"]')
        unretweet = await page.query_selector_all('button[data-testid="unretweet"]')
        retweetConfirm = await page.query_selector_all('div[data-testid="retweetConfirm"]')

        await retweet[0].click(delay=2000)
        await asyncio.sleep(random.randint(2, 3))
        await retweetConfirm[0].click()
        await asyncio.sleep(random.randint(2, 3))

        await likeTweet[0].click()
        await asyncio.sleep(random.randint(5, 8))

        # like, retweet, replay at random and book mark for raids
    await context.close()

asyncio.run(shill())
