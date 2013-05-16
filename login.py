import commands
import alp
from alp.request import requests
from conf import *
from alp.request.bs4 import BeautifulSoup
import cookielib

def checkLogin(responseTree = None):
    if responseTree == None:
        response = requests.get(LOGIN_URL, headers=headers, cookies=cookie_jar)
        responseTree = BeautifulSoup(response.content)

    # check for login 
    return responseTree.find('input', id="signinpasswd") == None

def login(login, password):
    response = requests.post(LOGIN_URL, {'login': login, 'passwd': password, 'remember': 'on'}, headers=headers, cookies=cookie_jar)
    return checkLogin(BeautifulSoup(response.content))

if len(alp.args()) == 1 and alp.args()[0] == "-safari":
    status, output = commands.getstatusoutput("python BinaryCookieReader.py ~/Library/Cookies/Cookies.binarycookies .turbofilm.tv")
    cookie_params = output.split('; ')
    name = cookie_params[0].split('=')[0]
    value = cookie_params[0].split('=')[1]
    domain = cookie_params[1].split('=')[1]
    path = cookie_params[2].split('=')[1]
    expires = cookie_params[3].split('=')[1]
    ck = cookielib.Cookie(version=0, name=name, value=value, port=None, port_specified=False, domain=domain, domain_specified=True, domain_initial_dot=True, path=path, path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
    cookie_jar.set_cookie(ck)
    cookie_jar.save(cookie_file, ignore_discard=True)

if len(alp.args()) == 0: #check for auth state
    if not checkLogin():
        print "Not authenticated"
    else:
        print "Authenticated"
elif not checkLogin():
    if len(alp.args()) < 2:
        print "Authentication failed"
    else :
        result = login(alp.args()[0], alp.args()[1])
        if result:
            cookie_jar.save(cookie_file, ignore_discard=True)
            print "Authentication succeeded"
        else:
            print "Authentication failed"
else:
    print "Authenticated"