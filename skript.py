# { date +%H; echo 15; } | xargs -n 2 python3.7 skript.py
import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django; django.setup()
import fblogin
from pages.models import Task, Profile
import datetime
tm = datetime.datetime.now()
# tm2 = datetime.datetime(2020, 5, 5, hour=5, minute=7, second=29)
# tm3 = datetime.datetime(2020, 5, 5, hour=5, minute=7, second=31)
# tm4 = datetime.datetime(2020, 5, 5, hour=4, minute=52, second=31)

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

def close(tm, task):
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
    print(profile)
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
        print(task)
        if loginfailed:
            break
        if close(tm, task): # check if we are going to send this task
            if fbsession is None: # we are sending a message, so get session
                # check for saved cookies
                if hasattr(profile, 'c_user') and hasattr(profile, 'xs'):
                    cookies = {
                        'c_user': profile.fb_cookie_c_user,
                        'xs': profile.fb_cookie_xs
                    }
                else: # if no cookies, get some
                    cookies = None
                try:
                    session = fblogin.getsession(login, cookies)
                except fblogin.LoginException:
                    loginfailed = True
                    continue
            
            # autofill fb_id 
            if task.friend_fb_id == '':
                task.friend_fb_id, task.friend_name = fblogin.searchname(fbsession, task.friend_name)
            
            fblogin.send(fbsession, task.body, task.friend_fb_id)
