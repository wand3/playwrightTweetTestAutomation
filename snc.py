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

# login if it auto logs out
async def sign_in(page, context):
    login_button = await page.get_by_test_id("loginButton").is_visible()

    if login_button:
        await page.get_by_test_id("loginButton").click()
        logging.info("Login button spotted succesfully")
    else:
        logging.error("Login button not found")
        return "Not Visible"
    await page.locator("input[name='text']").click()
    await asyncio.sleep(random.randint(2, 5))
    await page.locator("input[name='text']").fill("countriaro@gmail.com")

    # await page.locator('input[type="text"][placeholder="Username"]').fill("countriaro@gmail.com")
    await page.get_by_role("button", name="Next").click()
    await page.get_by_label("Password", exact=True).click()
    await page.get_by_label("Password", exact=True).fill("/Poiuytrewq123")
    await page.get_by_test_id("controlView").get_by_test_id("LoginForm_Login_Button").click()

    # Wait for login to complete
    await asyncio.sleep(10)

    # Save the login cookies
    async def save_cookies(context, file_path):
        cookies = await context.cookies()
        with open(file_path, 'w') as f:
            json.dump(cookies, f)
    await save_cookies(context, '../twshiller/cookies.json')

# handle and dismiss dialogs
async def handle_dialog(dialog):
    print(dialog.message)
    await dialog.dismiss()

# beautiful soup to get each post link from a scroll
async def post_hrefs(all_divs):
    all_hrefs = []
    for div in all_divs:
        anchor_tag = div.find('a')
        logging.info(f"{anchor_tag}")
        if anchor_tag:
            href = anchor_tag.get('href')
            if href:
                all_hrefs.append(href)
    return all_hrefs


async def interact(new):
    tweetText = await new.query_selector_all('div[data-testid="tweetText"]')
    likeTweet = await new.query_selector_all('button[data-testid="like"]')
    unlikeTweet = await new.query_selector_all('button[data-testid="unlike"]')
    retweet = await new.query_selector_all('button[data-testid = "retweet"]')
    reply = await new.query_selector_all('button[data-testid="reply"]')
    # unretweet = await new.query_selector_all('button[data-testid="unretweet"]')

    try:
        if unlikeTweet:
            # click to go back if post already liked
            goBack = new.get_by_test_id('app-bar-back')
            goBackPos = await goBack.bounding_box()
            await new.mouse.move(goBackPos["x"] + goBackPos["width"] / 2, goBackPos["y"] + goBackPos["height"] / 2)
            await new.mouse.down()
            await new.mouse.up()
            logging.info("Back to home new")
            await asyncio.sleep(random.randint(4, 6))
            # await new.wait_for_load_state()

        elif likeTweet:
            # like
            await likeTweet[0].click()
            logging.info("Liking post successful")
            await asyncio.sleep(random.randint(4, 6))

            new.on("dialog", lambda dialog: dialog.accept())

            # retweet
            await retweet[0].click(delay=2000)
            retweetConfirm = new.get_by_test_id("retweetConfirm")

            await asyncio.sleep(random.randint(2, 3))
            retweetConfirmPos = await retweetConfirm.bounding_box()
            await new.mouse.move(retweetConfirmPos["x"] + retweetConfirmPos["width"] / 2,
                                 retweetConfirmPos["y"] + retweetConfirmPos["height"] / 2)
            await new.mouse.down()
            await new.mouse.up()
            await asyncio.sleep(random.randint(2, 3))
            logging.info("Retweet post successful")
            # bookmark
            tweetBookmark = new.get_by_test_id("bookmark")
            tweetBookmarkPos = await tweetBookmark.bounding_box()
            await new.mouse.move(tweetBookmarkPos["x"] + tweetBookmarkPos["width"] / 2,
                                 tweetBookmarkPos["y"] + tweetBookmarkPos["height"] / 2)
            await new.mouse.down()
            await new.mouse.up()
            await new.wait_for_load_state()
            await asyncio.sleep(random.randint(1, 3))
            logging.info("Bookmark successful")
            # reply
            await reply[0].click()
            await new.on("dialog", handle_dialog)

            await new.wait_for_load_state()
            await asyncio.sleep(random.randint(2, 4))

            # get reply input box
            replyInput = new.get_by_test_id("tweetTextarea_0")
            replyInputPos = await replyInput.bounding_box()
            await new.mouse.move(replyInputPos["x"] + replyInputPos["width"] / 2,
                                 replyInputPos["y"] + replyInputPos["height"] / 2)
            await new.mouse.down()
            await new.mouse.up()
            await new.keyboard.type("I love this", delay=200)
            await asyncio.sleep(random.randint(2, 3))

            # send reply
            tweetReply = new.get_by_test_id("tweetTextarea_0")
            tweetReplyPos = await tweetReply.bounding_box()
            await new.mouse.move(tweetReplyPos["x"] + tweetReplyPos["width"] / 2,
                                 tweetReplyPos["y"] + tweetReplyPos["height"] / 2)
            await new.mouse.down()
            await new.mouse.up()
            await asyncio.sleep(random.randint(1, 3))
            # click tweet for reply
            expect(new.get_by_test_id("tweetButton")).to_be_visible()
            await new.get_by_test_id("tweetButton").click()
            await new.wait_for_load_state()
            logging.info("Post reply successful")
            await asyncio.sleep(random.randint(6, 10))

    except Exception as e:
        logging.error("Post already Liked check logs")
        logging.error(f"Failed reason {e}")


async def satisfy(new):
    # regex likes extraction
    # get all stats
    all_stat = []
    impre = await new.query_selector_all('div[role="group"]')
    logging.info(f"stat group: {impre}")
    # method 1 get bounding box of article and hover
    for im in impre:
        total_likes = 0
        total_views = 0
        stats = await im.get_attribute("aria-label")
        all_stat.append(stats)
        # define regex patterns
        rlikes = r'(\d+)\s+likes'
        rviews = r'(\d+)\s+views'
        for values in all_stat:
            # Use re.search() to find the pattern in the text
            likes = re.search(rlikes, values)
            views = re.search(rviews, values)

            if likes and views:
                # Extract the views count (first capturing group)
                likes_count = likes.group(1)
                views_count = views.group(1)
                likes = int(likes_count)
                views = int(views_count)
                res = "Likes = " + likes_count + " Views = " + views_count
                logging.info(f"Post stat : {res}")

                total_likes += likes
                total_views += views
                if total_likes >= random.choice(range(70, 1000)) or total_views >= 1000:
                    logging.info("Post stat satisfied")
                    return True
    logging.error("Likes and views pattern not found")
    return False


async def get_urls(all_links=None):
    post_urls = []
    if all_links is not None:
        links_len = len(all_links)
        for i in range(links_len):
            link = 'https://x.com' + all_links[i]
            logging.info(f"Link {i} {link}")
            post_urls.append(link)
        return post_urls


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

        login_button = await page.get_by_test_id("loginButton").is_visible()
        if login_button:
            await sign_in(page, context)

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
            all_links = await post_hrefs(all_divs)
            # Print all extracted hrefs
            print(len(all_links))
            # visit each extracted link one after the other open and interact in new context
            each_post = await get_urls(all_links)
            each_post_len = len(each_post)

            # loop through and open context for each
            for i in range(each_post_len):
                new = await context.new_page()
                await new.goto(each_post[i])
                logging.info(f"Link {each_post[i]} visited success fully")
                await new.wait_for_load_state()
                await asyncio.sleep(random.randint(2, 5))

                # check if post satisfies numbers of likes and views
                valid = await satisfy(new)
                logging.info(f"Stats {valid}")
                if valid:
                    await interact(new)
                    await asyncio.sleep(random.randint(2, 5))
                    await new.close()
                await asyncio.sleep(random.randint(2, 5))
                await new.close()
            count += 1

        await asyncio.sleep(random.randint(2, 5))

    await context.close()

asyncio.run(shill())
