#!/usr/bin/env python3
"""
    Playwright test

"""
import asyncio
import json
import logging
import traceback
import re
import time
import sys
from playwright.sync_api import Playwright, sync_playwright, Page, expect
from to_list import text_to_list
import random

"""
    switch selectors to CSS selector if XPATH or 
"""

# Configure logging to display messages to the terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])


# exit program
def exit_program():
    print("Exiting program")
    sys.exit()


# load cookies if it exists
async def load_cookies(context, file_path):
    with open(file_path, 'r') as f:
        cookies = json.load(f)
        await context.add_cookies(cookies)


def handle_dialog(dialog):
    print(dialog.message)
    dialog.dismiss()


with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)
    context = browser.new_context(
        viewport={"width": 768, "height": 1024},  # iPad Mini viewport size
        user_agent="Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        geolocation={"longitude": 7.4985, "latitude": 9.0563},
        permissions=["geolocation"]
    )
    context.set_geolocation({"longitude": 7.4985, "latitude": 9.0563})
    """
     # load up cookies
    load_cookies(context, "tele.json")
    logging.info("Session cookies loaded succesfully")

    page = context.new_page()



    # login with stored cookies
    page.goto("https://web.telegram.org/a/#-1002054370498")
    page.wait_for_load_state()

    # Load cookies from cookies.json file
    with open('tele.json', 'r') as file:
        cookies = json.load(file)
        context.add_cookies(cookies)

    page = context.new_page()

    page.goto("https://web.telegram.org/a/#-1002054370498")
    page.wait_for_load_state()
    """

    page = context.new_page()
    # change default timeout from 30secs
    page.set_default_timeout(55000)
    page.goto("https://web.telegram.org/a")
    page.wait_for_load_state()

    page.get_by_role("button", name="Log in by phone Number").is_visible()
    page.get_by_role("button", name="Log in by phone Number").click()

    # login input phone number
    tel_input = page.get_by_label("Your phone number")
    if tel_input:
        tel_input.click()
        page.get_by_label("Your phone number").fill('+123 45 6789 1011')

        print("success phone number")
        page.get_by_role("button", name="Next").is_visible()
        page.get_by_role("button", name="Next").click()

        page.wait_for_load_state()
        # login otp code input
        otp_input = page.get_by_label("Code")
        if otp_input:
            otp = input("Enter Otp: ")
            otp_input.click()
            otp_input.fill(otp)
            page.wait_for_load_state()

            # await the page load
            page.goto('https://web.telegram.org/a/#-1002038450855')
            time.sleep(10)
            # find group by the href value of the group name

            # find anchor element with href equal to group link and click
            element = page.locator("a[href='#-1002038450855']")
            # click on this group
            element.click()
            # click on groups message input
            time.sleep(5)
            page.wait_for_load_state()

            # schedule message button click visible to access schedule messages switch after first schedule from device
            try:
                """
                    Loop to read from each text file and schedule it line after line

                """
                # open page based on token stage
                messages = text_to_list(filename="pre_presale.txt")
                logging.info("Convert to list from text file succesful")

                total_messages = len(messages)
                slow = 15
                fast = 25

                count = 0
                for _ in range(slow):
                    new = context.new_page()
                    # await the page load
                    new.goto('https://web.telegram.org/a/#-1002038450855')
                    new.wait_for_load_state()
                    # check if schedule message is visible
                    expect(new.get_by_label('Open scheduled messages')).to_be_visible(timeout=20000)
                    # get send message button
                    sch_locator = new.get_by_label('Open scheduled messages')
                    logging.info("Scheduled messages icon seen")

                    # get and click schedule message
                    sch_locator.click()
                    new.wait_for_load_state()

                    # find text box and click
                    # Select the div element with the specified class
                    text = new.get_by_label("Message", exact=True).nth(1)  #
                    position = text.bounding_box()
                    logging.info("text input box found successfully")
                    new.mouse.move(position["x"] + position["width"] / 2,
                                   position["y"] + position["height"] / 2)
                    logging.info("Hover to input box successfully")

                    new.mouse.down(click_count=3)
                    # new.mouse.down()
                    new.mouse.up()
                    new.keyboard.press('Delete')
                    time.sleep(random.randint(2, 4))

                    # for message in range(total_messages):
                    new.keyboard.type(messages[count], delay=100)
                    time.sleep(random.randint(3, 5))
                    new.keyboard.press("Enter")

                    # text.click(force=True)
                    logging.info(f"schedule message {count} typed successfully")

                    snd = new.query_selector("button.Button.schedule.main-button.default.secondary.round.click-allowed")
                    logging.info("send message schedule send message check logs")
                    snd_pos = snd.bounding_box()
                    new.mouse.move(snd_pos["x"] + snd_pos["width"] / 2, snd_pos["y"] + snd_pos["height"] / 2)
                    # page.on("dialog", lambda dialog: dialog.accept())
                    new.mouse.down()
                    new.mouse.up()
                    logging.info("send first message schedule send message click successful")
                    time.sleep(random.randint(3, 6))

                    # page.on("dialog", lambda dialog: dialog.accept())

                    # page.get_by_role("d
                    hour = new.locator(
                        "#portals > div > div > div > div.modal-dialog > div > div.timepicker > input:nth-child(1)")
                    print(hour)

                    # hour = page.query_selector('.timepicker input')
                    hour_pos = hour.bounding_box()
                    new.mouse.move(hour_pos["x"] + hour_pos["width"] / 2,
                                   hour_pos["y"] + hour_pos["height"] / 2)
                    logging.info("Hover to set Hour")
                    new.mouse.down()
                    new.mouse.down()
                    new.mouse.up()
                    new.keyboard.press("ArrowRight")
                    new.keyboard.press("ArrowRight")
                    new.keyboard.press("Backspace")
                    new.keyboard.press("Backspace")

                    # set hour
                    message_hour = 23
                    new.keyboard.type(f'{message_hour}', delay=1000)
                    logging.info("Hour set")
                    time.sleep(random.randint(3, 6))

                    # select minute
                    minute = new.query_selector('.timepicker input:nth-child(2)')
                    min_pos = minute.bounding_box()
                    new.mouse.move(min_pos["x"] + min_pos["width"] / 2, min_pos["y"] + min_pos["height"] / 2)
                    logging.info("Hover to set minute")
                    new.mouse.down()
                    new.mouse.up()
                    new.keyboard.press("ArrowRight")
                    new.keyboard.press("ArrowRight")
                    new.keyboard.press("Backspace")
                    new.keyboard.press("Backspace")

                    # set minute
                    message_minute = random.randrange(1, 58)

                    new.keyboard.type(f'{message_minute}', delay=2000)
                    logging.info("Minute set")
                    time.sleep(random.randint(3, 5))

                    expect(new.locator(
                        '//*[@id="portals"]/div[1]/div/div/div[2]/div/div[4]/div/button')).to_be_visible()
                    # send today button
                    send_sch = new.locator('//*[@id="portals"]/div[1]/div/div/div[2]/div/div[4]/div/button')
                    send_pos = send_sch.bounding_box()
                    # move bouse to location
                    new.mouse.move(send_pos["x"] + send_pos["width"] / 2,
                                   send_pos["y"] + send_pos["height"] / 2)
                    logging.info("Hover to set Hour")
                    new.mouse.down()
                    new.mouse.up()
                    logging.info("Set Schedule Successful")
                    new.wait_for_load_state()
                    text = new.query_selector("#message-input-text > div:nth-child(1)")
                    logging.info("Next schedule loading")
                    time.sleep(random.randint(3, 6))

                    # go back to chat and click schedule again
                    back = new.query_selector_all('button[title="Back"]')
                    back_pos = back[1].bounding_box()
                    # move bouse to location
                    new.mouse.move(back_pos["x"] + back_pos["width"] / 2,
                                   back_pos["y"] + back_pos["height"] / 2)
                    logging.info("Hover to Back")
                    time.sleep(random.randint(2, 5))
                    new.mouse.down()
                    new.mouse.down()

                    # # back[1].click()
                    # new.mouse.up()
                    # logging.info("Click back Successful")
                    # new.wait_for_load_state()
                    # back[0].click()

                    # new home page
                    # new = context.new_page()
                    count += 1
                    logging.info(f"Count schedule {count} succesful!")
                    new.close()
                sys.exit(1)

            except Exception as e:
                # logs the error appropriately
                logging.error(traceback.format_exc())
                logging.info(f"Failed to see schedule message button reason {e}")
                exit_program()

        else:
            logging.info("Log not in successful Groups buttons not available")

    else:
        print("Signin with phone number failed")

    print(page.title())
    browser.close()

    # ---------------------