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

            # send_button click to access schedule messages switch for first schedule from device
            """
                message = page.get_by_label("Message", exact=True)     
                if message.is_visible():
                    message.click()
                    message.clear()
                    message.fill("gd")
                    time.sleep(1)



                    send_button = page.locator('//*[@id="MiddleColumn"]/div[3]/div[2]/div/div[2]/div/button')
                    if send_button.is_visible():
                        # expect(page.get_by_title('Send Message')).to_be_visible()
                        logging.info("send message visible")

                        # send_button = page.get_by_label('Send Message')
                        click_pos = send_button.bounding_box()

                        # Set the delay before click
                        # click_options = {'delay': 3000}  # 1000 milliseconds (1 second) delay

                        page.mouse.move(click_pos["x"] + click_pos["width"] / 2, click_pos["y"] + click_pos["height"] / 2)

                        page.mouse.down()
                        page.wait_for_timeout(9000)  # Hold for 3 seconds
                        logging.info("hold butto delay  3 secs succesfully")
                        # page.mouse.up()



                        # Click and hold the element
                        # send_button.click(options=click_options)

                        # page.mouse.hover(click_pos)
                        # page.mouse.down()
                        # page.mouse.click()
                        get_sch = page.locator('//*[@id="MiddleColumn"]/div[3]/div[2]/div/div[2]/div[1]/div[3]/div/div[2]')
                        expect(get_sch).to_be_visible()
                        # page.get_by_label('Send Message').click(delay=3000)
                        # get_sch = page.get_by_text('Schedule Message')
                        if get_sch:
                            # expect(page.get_by_text('Schedule Message')).to_be_visible()
                            page.mouse.up()
                            get_sch.click()
                            logging.info("send message seen click hold succesfully")
                            time.sleep(2)
                        else:
                            logging.info("no schedule button")
                    else:
                        logging.info("send message not seen or click")


                    time.sleep(20)
                else:
                    print("message button failed")
                    time.sleep(5)
            """

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
                while count < slow:
                    try:
                        # get send message button
                        if count == 0:
                            # check if schedule message is visible
                            expect(page.get_by_label('Open scheduled messages')).to_be_visible(timeout=10000)

                            sch_locator = page.get_by_label('Open scheduled messages')
                            logging.info("Scheduled messages icon seen")

                            # get and click schedule message
                            sch_locator.click()
                            page.wait_for_load_state()

                            # find text box and click
                            # Select the div element with the specified class
                            text = page.get_by_label("Message", exact=True).nth(1)  #
                            position = text.bounding_box()
                            logging.info("text input box found successfully")
                            page.mouse.move(position["x"] + position["width"] / 2,
                                            position["y"] + position["height"] / 2)
                            logging.info("Hover to input box successfully")

                            page.mouse.down()
                            page.mouse.up()

                            # for message in range(total_messages):
                            page.keyboard.type(messages[count], delay=100)
                            page.keyboard.press("Enter")

                            # text.click(force=True)
                            logging.info(f"schedule message {count} typed successfully")

                            snd = page.query_selector(
                                "button.Button.schedule.main-button.default.secondary.round.click-allowed")
                            logging.info("send message schedule send message check logs")
                            snd_pos = snd.bounding_box()
                            page.mouse.move(snd_pos["x"] + snd_pos["width"] / 2, snd_pos["y"] + snd_pos["height"] / 2)
                            # page.on("dialog", lambda dialog: dialog.accept())
                            page.mouse.down()
                            page.mouse.up()
                            logging.info("send first message schedule send message click successful")

                            # page.on("dialog", lambda dialog: dialog.accept())

                            # page.get_by_role("d
                            hour = page.locator(
                                "#portals > div > div > div > div.modal-dialog > div > div.timepicker > input:nth-child(1)")
                            print(hour)

                            # hour = page.query_selector('.timepicker input')
                            hour_pos = hour.bounding_box()
                            page.mouse.move(hour_pos["x"] + hour_pos["width"] / 2,
                                            hour_pos["y"] + hour_pos["height"] / 2)
                            logging.info("Hover to set Hour")
                            page.mouse.down()
                            page.mouse.down()
                            page.mouse.up()
                            page.keyboard.press("ArrowRight")
                            page.keyboard.press("ArrowRight")
                            page.keyboard.press("Backspace")
                            page.keyboard.press("Backspace")

                            # set hour
                            message_hour = 23
                            page.keyboard.type(f'{message_hour}', delay=1000)
                            logging.info("Hour set")

                            # select minute
                            minute = page.query_selector('.timepicker input:nth-child(2)')
                            min_pos = minute.bounding_box()
                            page.mouse.move(min_pos["x"] + min_pos["width"] / 2, min_pos["y"] + min_pos["height"] / 2)
                            logging.info("Hover to set minute")
                            page.mouse.down()
                            page.mouse.up()
                            page.keyboard.press("ArrowRight")
                            page.keyboard.press("ArrowRight")
                            page.keyboard.press("Backspace")
                            page.keyboard.press("Backspace")

                            # set minute
                            message_minute = random.randrange(1, 58)

                            page.keyboard.type(f'{message_minute}', delay=2000)
                            logging.info("Minute set")

                            expect(page.locator(
                                '//*[@id="portals"]/div[1]/div/div/div[2]/div/div[4]/div/button')).to_be_visible()
                            # send today button
                            send_sch = page.locator('//*[@id="portals"]/div[1]/div/div/div[2]/div/div[4]/div/button')
                            send_pos = send_sch.bounding_box()
                            # move bouse to location
                            page.mouse.move(send_pos["x"] + send_pos["width"] / 2,
                                            send_pos["y"] + send_pos["height"] / 2)
                            logging.info("Hover to set Hour")
                            page.mouse.down()
                            page.mouse.up()
                            logging.info("Set Schedule Successful")
                            page.wait_for_load_state()
                            text = page.query_selector("#message-input-text > div:nth-child(1)")
                            logging.info("Next schedule loading")
                            time.sleep(random.randint(3, 5))
                        elif count > 0:
                            # go back to chat and click schedule again
                            back = page.query_selector_all('button[title="Back"]')
                            back_pos = back[1].bounding_box()
                            # move bouse to location
                            page.mouse.move(back_pos["x"] + back_pos["width"] / 2,
                                            back_pos["y"] + back_pos["height"] / 2)
                            logging.info("Hover to Back")
                            time.sleep(random.randint(2, 5))
                            page.mouse.down()
                            page.mouse.down()

                            # back[1].click()
                            page.mouse.up()
                            logging.info("Click back Successful")
                            page.wait_for_load_state()

                            # go to home page
                            back[0].click()
                            page.goto("https://web.telegram.org/a/#-1002038450855")
                            page.wait_for_load_state()
                            time.sleep(random.randint(1, 4))

                            # button of same group link to close side panel
                            # chat = page.locator("a[href='#-1002038450855']")
                            # chat.click()
                            logging.info("Page with side panel closed")

                            time.sleep(random.randint(1, 5))
                            # check if schedule message is visible
                            page.locator("button[title='Open scheduled messages']").click()
                            # expect(page.get_by_label('Open scheduled messages')).to_be_visible(timeout=20000)

                            # sch_locator = page.get_by_label('Open scheduled messages')

                            logging.info("Scheduled messages icon seen")

                            # get and click schedule message
                            # sch_locator.click()
                            page.wait_for_load_state()

                            # find text box and click
                            # Select the div element with the specified class
                            text = page.get_by_label("Message", exact=True).nth(1)  #
                            position = text.bounding_box()
                            logging.info("text input box found successfully")
                            page.mouse.move(position["x"] + position["width"] / 2,
                                            position["y"] + position["height"] / 2)
                            logging.info("Hover to input box successfully")

                            page.mouse.down()
                            page.mouse.up()

                            # for message in range(total_messages):
                            page.keyboard.type(messages[count], delay=100)
                            page.keyboard.press("Enter")
                            time.sleep(random.randint(3, 5))

                            # text.click(force=True)
                            logging.info(f"schedule message {count} typed successfully")
                            # page.on("dialog", lambda dialog: dialog.accept())
                            # find schedule icon and click
                            page.wait_for_load_state()
                            snd = page.query_selector_all('button[aria-label="Send Message"]')
                            snd[0].click()
                            logging.info("send message schedule send message check logs")
                            page.wait_for_load_state()

                            # hover to time picker and click
                            # timep = page.query_selector('div[class="timepicker"]')
                            # timep_pos = timep.bounding_box()
                            # # Calculate coordinates for clicking on the left side of the element
                            # left_x = timep_pos['x']
                            # center_y = timep_pos['y'] + timep_pos['height'] / 2
                            #
                            # # Perform the click on the left side of the element
                            # page.mouse.click(left_x + 5, center_y,
                            #                  button='left')  # Adding a small offset (5px) to the left

                            # page.mouse.move(timep_pos["x"] + timep_pos["width"] / 2, timep_pos["y"] + timep_pos["height"] / 2)
                            # page.mouse.down()
                            # time.sleep(random.randint(3, 5))
                            logging.info("send message schedule send message click successful")

                            # Wait until the element is visible
                            # page.wait_for_selector('h4:visible:has-text("June")').is_visible()
                            expect(page.locator(
                                "#portals > div:nth-child(2) > div > div > div.modal-dialog > div > div.timepicker")).to_be_visible()
                            # expect(page.query_selector_all('input[inputmode="decimal"]')).to_be_visible()
                            logging.info("Time picker load successful")

                            hour = page.query_selector_all('input[inputmode="decimal"]')
                            # page.evaluate("arguments[0].click()", hour[0])
                            # hour[0].click()
                            # hour[0].click()
                            # hour = page.locator("#portals > div > div > div > div.modal-dialog > div > div.timepicker > input:nth-child(1)")
                            # hour = page.query_selector('//*[@id="portals"]/div[1]/div/div/div[2]/div/div[3]/input[1]')
                            # hour.click(delay=6000)
                            # hour = page.query_selector('.timepicker input')
                            print(hour)
                            hour_pos = hour[0].bounding_box()
                            page.mouse.move(hour_pos["x"] + hour_pos["width"] / 2,
                                            hour_pos["y"] + hour_pos["height"] / 2)
                            logging.info("Hover to set Hour")
                            page.mouse.down()
                            page.mouse.up()
                            page.keyboard.press("ArrowRight")
                            page.keyboard.press("ArrowRight")
                            page.keyboard.press("Backspace")
                            page.keyboard.press("Backspace")

                            # set hour
                            message_hour = 23
                            page.keyboard.type(f'{message_hour}', delay=1000)
                            logging.info("Hour set")

                            # select minute
                            minute = page.query_selector('.timepicker input:nth-child(2)')
                            # minute = page.query_selector_all('input[inputmode="decimal"]')
                            # minute[1].click()
                            # page.evaluate("arguments[0].click()", minute[-1])
                            time.sleep(random.randint(1, 3))

                            min_pos = minute.bounding_box()
                            page.mouse.move(min_pos["x"] + min_pos["width"] / 2, min_pos["y"] + min_pos["height"] / 2)
                            logging.info("Hover to set minute")
                            page.mouse.down()
                            page.mouse.up()
                            page.keyboard.press("ArrowRight")
                            page.keyboard.press("ArrowRight")
                            page.keyboard.press("Backspace")
                            page.keyboard.press("Backspace")

                            # set minute
                            message_minute = random.randrange(1, 58)

                            page.keyboard.type(f'{message_minute}', delay=2000)
                            logging.info("Minute set")

                            # expect(page.locator(
                            #     '//*[@id="portals"]/div[1]/div/div/div[2]/div/div[4]/div/button')).to_be_visible()
                            # send today button
                            send_sch = page.locator('//*[@id="portals"]/div[1]/div/div/div[2]/div/div[4]/div/button')
                            # send_sch = page.query_selector('#portals > div:nth-child(1) > div > div > div.modal-dialog > div > div.footer > div > button')
                            # send_sch.click()

                            send_pos = send_sch.bounding_box()
                            # move bouse to location
                            page.mouse.move(send_pos["x"] + send_pos["width"] / 2,
                                            send_pos["y"] + send_pos["height"] / 2)
                            page.mouse.down()
                            page.mouse.up()
                            logging.info("Set Schedule Successful")
                            page.wait_for_load_state()
                            text = page.query_selector("#message-input-text > div:nth-child(1)")
                            logging.info("Next schedule loading")
                            time.sleep(4)

                            # select hour
                            page.wait_for_load_state()
                            # time.sleep(7)
                    except Exception as e:
                        logging.error(traceback.format_exc(e))
                        logging.info(f"Unable to send message check logs : {e}")
                        exit_program()

                    count += 1
                    logging.info(f"Count schedule {count} succesful!")
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