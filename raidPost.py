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
        await page.goto('https://x.com/mymixtapez/status/1802807348404105393')
        logging.info("Session continued")
        await page.wait_for_load_state()
        await asyncio.sleep(random.randint(5, 8))

        tweetText = await page.query_selector_all('div[data-testid="tweetText"]')
        likeTweet = await page.query_selector_all('button[data-testid="like"]')
        unlikeTweet = await page.query_selector_all('button[data-testid="unlike"]')
        retweet = await page.query_selector_all('button[data-testid = "retweet"]')
        reply = await page.query_selector_all('button[data-testid="reply"]')
        # unretweet = await page.query_selector_all('button[data-testid="unretweet"]')

        try:
            if unlikeTweet:
                # click to go back if post already liked
                goBack = page.get_by_test_id('app-bar-back')
                goBackPos = await goBack.bounding_box()
                await page.mouse.move(goBackPos["x"] + goBackPos["width"] / 2, goBackPos["y"] + goBackPos["height"] / 2)
                await page.mouse.down()
                await page.mouse.up()
                logging.info("Back to home page")
                await asyncio.sleep(random.randint(4, 6))
                # await page.wait_for_load_state()

            elif likeTweet:
                # like
                await likeTweet[0].click()
                logging.info("Liking post successful")
                await asyncio.sleep(random.randint(4, 6))

                page.on("dialog", lambda dialog: dialog.accept())

                # retweet
                await retweet[0].click(delay=2000)
                retweetConfirm = page.get_by_test_id("retweetConfirm")

                await asyncio.sleep(random.randint(2, 3))
                retweetConfirmPos = await retweetConfirm.bounding_box()
                await page.mouse.move(retweetConfirmPos["x"] + retweetConfirmPos["width"] / 2,
                                      retweetConfirmPos["y"] + retweetConfirmPos["height"] / 2)
                await page.mouse.down()
                await page.mouse.up()
                await asyncio.sleep(random.randint(2, 3))
                logging.info("Retweet post successful")
                # bookmark
                tweetBookmark = page.get_by_test_id("bookmark")
                tweetBookmarkPos = await tweetBookmark.bounding_box()
                await page.mouse.move(tweetBookmarkPos["x"] + tweetBookmarkPos["width"] / 2,
                                      tweetBookmarkPos["y"] + tweetBookmarkPos["height"] / 2)
                await page.mouse.down()
                await page.mouse.up()
                await page.wait_for_load_state()
                await asyncio.sleep(random.randint(1, 3))
                logging.info("Bookmark successful")
                # reply
                await reply[0].click()
                await page.wait_for_load_state()
                await asyncio.sleep(random.randint(2, 4))


                # get reply input box
                replyInput = page.get_by_test_id("tweetTextarea_0")
                replyInputPos = await replyInput.bounding_box()
                await page.mouse.move(replyInputPos["x"] + replyInputPos["width"] / 2,
                                      replyInputPos["y"] + replyInputPos["height"] / 2)
                await page.mouse.down()
                await page.mouse.up()
                await page.keyboard.type("My First Shill i love this", delay=900)
                await asyncio.sleep(random.randint(2, 3))

                # send reply
                tweetReply = page.get_by_test_id("tweetTextarea_0")
                tweetReplyPos = await tweetReply.bounding_box()
                await page.mouse.move(tweetReplyPos["x"] + tweetReplyPos["width"] / 2,
                                      tweetReplyPos["y"] + tweetReplyPos["height"] / 2)
                await page.mouse.down()
                await page.mouse.up()
                await page.wait_for_load_state()
                await asyncio.sleep(random.randint(1, 3))
                logging.info("Post reply successful")

        except Exception as e:
            logging.error("Post already Liked check logs")
            logging.error(f"Failed reason {e}")

        # like, retweet, replay at random and book mark for raids
    await context.close()

asyncio.run(shill())
