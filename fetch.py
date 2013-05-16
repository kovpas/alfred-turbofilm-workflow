import json

import alp
from alp.request import requests

import html5lib
from lxml.html import tostring
from conf import *

htmlParser = html5lib.HTMLParser(tree=html5lib.treebuilders.getTreeBuilder("lxml")
                                 , namespaceHTMLElements=False)

def checkLogin(responseTree = None):
    if responseTree == None:
        response = requests.get(LOGIN_URL, headers=headers, cookies=cookie_jar)
        responseTree = htmlParser.parse(response.content)

    # check for login 
    return len(responseTree.xpath('//input[@id="signinpasswd"]')) == 0

def fetchSeries():
    if len(cached_series) > 0:
        return cached_series

    response = requests.get(MY_SERIES_URL, headers=headers, cookies=cookie_jar)
    responseTree = htmlParser.parse(response.content)
    seriesDivs = responseTree.xpath('//div[contains(@id, "seriesbox")]')
    series = []
    for seriesDiv in seriesDivs:
        href = seriesDiv.xpath('div[@class="myseriest"]/a')[0].attrib['href']
        enName = seriesDiv.xpath('div[@class="myseriest"]/a/span/text()')[0].strip()
        ruName = seriesDiv.xpath('div[@class="myseriest"]/a/span/text()')[1].strip()
        serId = href.replace('/Series/', '')
        episodeDivs = seriesDiv.xpath('a/span[contains(@class,"myseriesblock")]/..')
        unwatchedEpisodes = []
        for episodeDiv in episodeDivs:
            epHref = episodeDiv.attrib['href']
            enEpName = episodeDiv.xpath('span/span/span[@class="myseriesbten"]/text()')[0].strip()
            ruEpName = episodeDiv.xpath('span/span/span[@class="myseriesbtru"]/text()')[0].strip()
            unwatchedEpisodes.append({'href': epHref, 'en':enEpName, 'ru':ruEpName})
        series.append({"href":href, "en":enName, "ru":ruName, "id": serId, 'unwatchedEpisodes':unwatchedEpisodes})

    with open(cache_file, 'wb') as fp:
        json.dump(series, fp, sort_keys=False, indent=4, separators=(',', ': '))

    return series


seriesName = "" if len(alp.args()) == 0 else alp.args()[0]
alp.log(seriesName)
series = fetchSeries()
items = []

if len(seriesName) == 0: # fetch series
    for ser in series:
        iDict = dict(title=ser['en'] + ' ' + ser['ru'], subtitle=ser['href'], uid=ser['id'], valid=False, autocomplete=ser['id'])
        items.append(alp.Item(**iDict))
else: 
    series = [item for item in series if seriesName.lower() in item["id"].lower()]
    if len(series) == 1 and series[0]['id'] == seriesName:
        alp.log(series[0]['unwatchedEpisodes'])
        for episode in series[0]['unwatchedEpisodes']:
            title = episode['en']
            title += ('' if episode['en'] == episode['ru'] else (' / ' + episode['ru']))
            iDict = dict(title=title, subtitle=episode['href'], uid=episode['href'], valid=True, arg=TURBOFILM_URL + episode['href'])
            items.append(alp.Item(**iDict))
        pass
    else:
        for ser in series:
            iDict = dict(title=ser['en'] + ' ' + ser['ru'], subtitle=ser['href'], uid=ser['id'], valid=False, autocomplete=ser['id'])
            items.append(alp.Item(**iDict))

alp.feedback(items)
