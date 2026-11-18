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
    browser.add_cookie({"name": "MUSIC_U", "value": "00269D37B29D1CEC7BB154413CFED61855B7CE76CDF5BE716EF0D86DCF8AE5B0A263B250980A347EBB94AC8435B374CB95892B4F26DD19D9B3F9FE8F3E8D4E4EEB424EC30CEDE1E0C708D27BBE9D6D1320CAA176C09D0D1197950491F5B87B1AD80DA645EDB3FF9EAACE4B6FE4188D7A1F63B8B33DDD1249B158933829F27B1DD05A326FDFC061816806211F082124ED8A74226FC757AB29EC8E1007BAD5A292F8330ADF20D4A56441CF8C3DA0AA0B3B3D39DCAEEEB0D36A0ADBFD7ADB6D6A63C45A1DB054BB4018F169458028EB7253A9FECF5AAAF40C021128BD2FF28EAA393156AFF5867E82B3CD1A569784F31AA405A32713C08240D9D26F910AB4F3D6E9428A8F2A0F1C3FE6AAE396E75C80DFC52939558D0A9D282C17F71945C449C2D344530AD4E6E92138E054237F141C7920FC75287453192FBAAEA09228165A86F8101008B63F23AEE5ECB6111F5C064BD1C4FD4238DB099A41B3F1C687585B51CD7DBD0B16279729B35EA9996653A9BED626C60CC1B4E3E247006B27F2AA4E89AF5A76BF62235D7E087B6A4FCB356E9522156BCEF09614D102035CBAF0081FEC7ED0"})
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
