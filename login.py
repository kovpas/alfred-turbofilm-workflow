import alp
from alp.request import requests
import html5lib
from conf import *

htmlParser = html5lib.HTMLParser(tree=html5lib.treebuilders.getTreeBuilder("lxml")
                                 , namespaceHTMLElements=False)

def checkLogin(responseTree = None):
    if responseTree == None:
        response = requests.get(LOGIN_URL, headers=headers, cookies=cookie_jar)
        responseTree = htmlParser.parse(response.content)

    # check for login 
    return len(responseTree.xpath('//input[@id="signinpasswd"]')) == 0

def login(login, password):
    response = requests.post(LOGIN_URL, {'login': login, 'passwd': password, 'remember': 'on'}, headers=headers, cookies=cookie_jar)
    return checkLogin(htmlParser.parse(response.content))

if len(alp.args()) == 0: #check for auth state
    if not checkLogin():
        print "Not authenticated"
    else:
        print "Authenticated"
elif not checkLogin():
    # result = login(alp.args()[0], alp.args[1])
    result = login(alp.args()[0], alp.args()[1])
    if result:
        cookie_jar.save(cookie_file, ignore_discard=True)
        print "Authentication succeeded"
    else:
        print "Authentication failed"
else:
    print "Authenticated"