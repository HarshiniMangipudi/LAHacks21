import fbchat

def send_msg(msg):
    cookies = {
        'c_user': '100010066151598',
        'xs': '8%3A-GZNhW4SKd1sYg%3A2%3A1616721209%3A13274%3A12570'
    }

    messenger = fbchat.Client("", "", session_cookies=cookies)

    messenger.send(fbchat.Message(text=msg), thread_id=100007055893034)

def selenium_get():
    from selenium import webdriver
    import time

    test_driver = webdriver.Firefox()
    test_driver.get("https://www.messenger.com/")

    email_input = test_driver.find_element_by_id("email")
    pass_input = test_driver.find_element_by_id("pass")
    login_button = test_driver.find_element_by_id("loginbutton")

    email = "Natan.luc.232@gmail.com"
    password = "Lahacksspoof"

    email_input.send_keys(email)
    time.sleep(1)
    pass_input.send_keys(password)
    time.sleep(1)
    login_button.click()
    time.sleep(10)
    HOLD = test_driver.get_cookies()
