# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "009BC2CB3E61344986D51C081E1B2D9CD463CEA2A03F3A2B787E0B9DA33D7EC959B072B604D051E4662E6E8D07A9459F2CD01D9098E8E0DA89D1F391BFA2DFE61590A6487E3DBD3FC35D576800D90A45852F081A01B943A3C06F780208DC6B2C6B6185A1412D34BBA6A427A8DC376050FD850FA4A519A26DAA12FC41B9D13B5733E260D479E1027639933B411775C6E8DC6383B059CF3618FD87F673B8E42E8D64C7216A79C2B0248CB73903FF790EC7F3CDB47339FAD44AC124936C780764A35DFC4F71545FC6C92899F355229685E652D461E255845121D12EF6BE1E9F6210F334312C645FD197E9AEAB56D91D18E6602E87AC344C2E5E91B73F5AF342AA4E4ECEE56B9F1A7BF60D2F7F670BF76D1359B0B251E78BBBE7EA4E02EEC73A3F0A6D03683215D67E3BF50D8FF3725CD8507243C8344134FE0134D55E323AE58935BF3D08F4151248C6E0F76D4D9A3F8FFBE0C1D838E6DD6822922DAE5A0A038E0609"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
