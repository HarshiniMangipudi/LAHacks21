import os
import time
import fbchat
import random
from selenium import webdriver

ON_PI = False

class LoginException(Exception):
    def __init__(self, message):
        super().__init__(message)

def getcookies(login):
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
    time.sleep(2.5)
    email_input.send_keys(login['email'])
    time.sleep(2.5)
    pass_input.send_keys(login['password'])
    time.sleep(2.2523)
    login_button.submit()
    time.sleep(7.345345234)
    allcookies = test_driver.get_cookies()
    
    successes = 0
    cookies = {}

    for cookie in allcookies:
        if cookie['name'] == 'c_user':
            cookies['c_user'] = cookie['value']
            successes += 1
        elif cookie['name'] == 'xs':
            cookies['xs'] = cookie['value']
            successes += 1

    if successes != 2:
        raise LoginException("Login to Facebook failed using email and password.")
    
    return cookies

def searchname(session, name):
    """Find uid and real name

    Args:
        session: fbchat session
        name: search string

    Returns:
        tuple: uid (str), autocorrect name (str)
    """
    time.sleep(0.3)
    user = session.searchForUsers(name, limit=1)[0]
    return user.uid, user.name

def getsession(login, cookies):
    """Get a messenger session

    Args:
        login ([type]): email and password
        cookies (dict): xs and c_user

    Returns:
        tuple: session, refreshed cookies
    """
    refresh = False
    if cookies is not None:
        try:
            msnger = fbchat.Client("", "", session_cookies=cookies) 
            print("FIRST LOGIN GOOD")
        except fbchat.FBchatException:
            print("FIRST LOGIN FAILED")
            refresh = True
    else: 
        refresh = True
    if refresh:
        print("REFRESHING COOKIES")
        cookies = getcookies(login)
        try:
            time.sleep(3.1) 
            msnger = fbchat.Client("", "", session_cookies=cookies) 
        except fbchat.FBchatException:
            raise LoginException("Login to Facebook failed using newly baked cookies. This is very bad.")
    
    return (msnger, cookies)

def send(session, message, tid):
    time.sleep((random.betavariate(2, 5) * 2) + 1)
    session.send(fbchat.Message(text=message), thread_id=tid)
