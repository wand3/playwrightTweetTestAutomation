#!/usr/bin/env python3
"""
    Playwright test

"""
import asyncio
import json
import logging
from playwright.async_api import Playwright, async_playwright


# async save browser cookies
async def save_cookies(context, file_path):
    cookies = await context.cookies()
    with open(file_path, 'w') as f:
        json.dump(cookies, f)


# async def load cookies
async def load_cookies(context, file_path):
    with open(file_path, 'r') as f:
        cookies = json.load(f)
        await context.add_cookies(cookies)


# async function for running test
async def hill():
    async with async_playwright() as p:

        # browser configs
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 375, "height": 812},  # iPhone X viewport size
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
        )
      
        page = await context.new_page()
        # goto site
        await page.goto("https://x.com/")
        login_button = await page.get_by_test_id("loginButton").is_visible()

        if login_button:
            await page.get_by_test_id("loginButton").click()
            logging.info("Login button spotted succesfully")
        else:
            logging.error("Login button not found")
            return "Not Visible"

        await page.get_by_label("Phone, email address, or").is_visible()
        await page.get_by_label("Phone, email address, or").fill("countriaro@gmail.com")
        await page.get_by_role("button", name="Next").click()
        await page.get_by_label("Password", exact=True).click()
        await page.get_by_label("Password", exact=True).fill("/Poiuytrewq123")
        await page.get_by_test_id("controlView").get_by_test_id("LoginForm_Login_Button").click()

        # Wait for login to complete
        await asyncio.sleep(10)

        # Save the login cookies
        await save_cookies(context, 'cookies.json')

    await context.close()
asyncio.run(hill())



#     page.get_by_label("135 Replies. Reply").click()
#     page.get_by_test_id("tweetTextarea_0").fill("good")
#     page.get_by_test_id("tweetButton").click()
#     page.get_by_test_id("AppTabBar_DirectMessage_Link").click()
#     page.get_by_role("button", name="Got it!").click()
#     page.get_by_test_id("AppTabBar_Notifications_Link").click()
#     page.get_by_test_id("AppTabBar_Home_Link").click()
#     page.get_by_test_id("DashButton_ProfileIcon_Link").click()
#     page.get_by_role("link", name="Profile").click()
#     page.get_by_role("tab", name="Replies").click()
#     page.get_by_test_id("app-bar-back").click()
#     page.get_by_label(":16").get_by_test_id("playButton").click()
#     page.get_by_test_id("immersive-tweet-back-button-1771188351678173676").click()
