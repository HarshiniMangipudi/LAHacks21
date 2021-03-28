# { date +%H; echo 15; } | xargs -n 2 python3.7 skript.py
import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django; django.setup()
import fblogin
from fblogin import logger
import logging
from pages.models import Task, Profile
import datetime

tm = datetime.datetime.now()

FIFTEEN = datetime.timedelta(minutes=15)
FIFTEEN_HALF = datetime.timedelta(minutes=7, seconds=30)

def rnd15(tm):
    discard = datetime.timedelta(minutes=tm.minute % 15,
                                seconds=tm.second,
                                microseconds=tm.microsecond)
    tm -= discard
    if discard >= FIFTEEN_HALF:
        tm += FIFTEEN
    
    return tm

def parsedow(task):
    days = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday'
    ]
    return [task.__getattribute__(d) for d in days]

def close(tm, task, lbound, rbound):
    lbound = datetime.datetime.combine(lbound, datetime.datetime.min.time())
    rbound = datetime.datetime.combine(rbound, datetime.datetime.min.time())

    if tm < lbound or rbound < tm:
        return False
    x = task.time_of_day
    xdows = parsedow(task)
    tmrnd = rnd15(tm)
    l, r = tmrnd - FIFTEEN_HALF, tmrnd + FIFTEEN_HALF
    ltime, rtime = l.time(), r.time()
    ldow, rdow = l.weekday(), r.weekday()
    if ltime < rtime:
        return ltime <= x and x < rtime and xdows[ldow] # ldow == rdow
    else: 
        return (ltime <= x and xdows[ldow]) or (x < rtime and xdows[rdow])


for profile in Profile.objects.all():
    logger.info(profile)
    try:
        login = {
            'email': profile.fb_email, 
            'password':  profile.fb_password,
        }
    except AttributeError: # no login info yet, skip the user
        continue
    
    fbsession = None
    loginfailed = False
    for task in Task.objects.filter(user=profile.user):
        logger.info(task)
        if loginfailed:
            break
        if not close(tm, task, task.start_date, task.end_date): # check if we are going to send this task
            logger.info("SKIPPING. TIME TOO FAR")
        else:
            if fbsession is None: # we are sending a message, so get session
                # check for saved cookies
                # if hasattr(profile, 'fb_cookie_c_user') and hasattr(profile, 'fb_cookie_xs'):
                #     cookies = {
                #         'c_user': profile.fb_cookie_c_user,
                #         'xs': profile.fb_cookie_xs
                #     }
                if profile.c_user == '': # if no cookies, get some
                    cookies = None
                else: 
                    cookies = {
                        'c_user': profile.fb_cookie_c_user,
                        'xs': profile.fb_cookie_xs
                    }
                try:
                    (fbsession, newcookies) = fblogin.getsession(login, cookies)
                    logger.info("GOT SESSION")
                    profile.fb_cookie_c_user = newcookies['c_user']
                    profile.fb_cookie_xs = newcookies['xs']
                    profile.save()
                except fblogin.LoginException:
                    logger.info("FAILED LOGIN")
                    loginfailed = True
                    continue
            
            # autofill fb_id 
            if task.friend_fb_id == '':
                task.friend_fb_id, task.friend_name = fblogin.searchname(fbsession, task.friend_name)
                task.save()
            
            fblogin.send(fbsession, task.body, task.friend_fb_id)
            logger.info("SENT MESSAGE")
