import os
import time
import logging
from selenium import webdriver

filehandler = logging.FileHandler(os.path.join(os.path.dirname(__file__), 'events.log'))
filehandler.setFormatter(logging.Formatter(fmt="%(asctime)s:%(levelname)s:%(message)s"))
logger = logging.getLogger("loginslogger")
logger.setLevel(logging.INFO)
logger.addHandler(filehandler)

ON_PI = False

def getcookies(config):
    if ON_PI:
        os.environ['PATH'] += os.pathsep + "/home/pi/Downloads/geckodriver-0.29.0/target/armv7-unknown-linux-gnueabihf/release"

    opts = webdriver.FirefoxOptions()
    opts.add_argument("--headless")
    opts.add_argument("--window-size=1080,1080")
    test_driver = webdriver.Firefox(options=opts)
    test_driver.get("https://www.messenger.com/")

    email_input = test_driver.find_element_by_id("email")
    pass_input = test_driver.find_element_by_id("pass")
    login_button = test_driver.find_element_by_id("loginbutton")
    email_input.send_keys(config['facebook']['email'])
    time.sleep(5)
    pass_input.send_keys(config['facebook']['password'])
    time.sleep(5)
    login_button.submit()
    time.sleep(5)
    allcookies = test_driver.get_cookies()
    
    successes = 0

    for cookie in allcookies:
        if cookie['name'] == 'c_user':
            config['cookies']['c_user'] = cookie['value']
            successes += 1
        elif cookie['name'] == 'xs':
            config['cookies']['xs'] = cookie['value']
            successes += 1

    if successes != 2:
        raise RuntimeError("Selenium Login Failed")
    
    return config
