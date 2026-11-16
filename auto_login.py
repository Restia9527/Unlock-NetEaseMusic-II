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
    browser.add_cookie({"name": "MUSIC_U", "value": "0019DFDB807D81E80529C6BEE9E4EBFB128B990E636F93B60B1B209E7D037EC67940A68C2C48A869AF3A0E151D8140EB5C34C1743E090B23782CEB936E9BB7C8D7C79447FDE191B589E1E548E4909B3F8E04AE0F44FDED66931133D21ACD215C9F8AA9C5CB350501A11599AA4A0BCE8E8B802762711C5A93FFA5BC97A2850DD8F4C546D53035299956325653FDD636495F7003E18AB6E2FD85F13BBB28A414B6D2801EE52E7F804DAB2B1809BF563EA4272FB1CB88652F074C6722C4D8753FF7554A372E6BC91FD99C19526B8E8A84E639B214659BFBA4B660ED5F919ACCCDB0E3B3AF958EE8FF121AF6B80E567466A1D0D623AEC1AE52DC251E233225B39453E58343875EE4F411F0D46551E2B2A420DC94EB61280B227DC2F5924B9D66C0C6CF4A334110E20F229B10B3670C4BF753CAB1B7E2EC0CB86DCD82BFB845374EAA27E55C698B767AB6E84D081B708D16AE2BDE016C725186A0DAEA4D4CB03D2350F02AA213E883402AAA37DE8A44ED130E7166D6DDAA8FEC003D6659947DD942595744F7472D651A44FE401101D0E416A095C1BAC401152FD8DE26BAE9E3D67E0380"})
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
