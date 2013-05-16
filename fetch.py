import json
import re

import alp
from alp.request import requests
from alp.request.bs4 import BeautifulSoup

from conf import *

def checkLogin(responseTree = None):
    if responseTree == None:
        response = requests.get(LOGIN_URL, headers=headers, cookies=cookie_jar)
        responseTree = BeautifulSoup(response.content)

    # check for login 
    return responseTree.find('input', id="signinpasswd") == None

def fetchSeries():
    if len(cached_series) > 0:
        return cached_series

    response = requests.get(MY_SERIES_URL, headers=headers, cookies=cookie_jar)
    responseTree = BeautifulSoup(response.content)
    seriesDivs = responseTree.find_all('div', id=re.compile("seriesbox"))
    series = []
    for seriesDiv in seriesDivs:
        href = seriesDiv.select('div.myseriest > a')[0]['href']
        enName = seriesDiv.select('div.myseriest > a > span')[0].string.strip()
        ruName = seriesDiv.select('div.myseriest > a > span')[1].string.strip()
        serId = href.replace('/Series/', '')
        episodeDivs = seriesDiv.find_all('span', attrs={'class':re.compile("myseriesblock")})
        unwatchedEpisodes = []
        for episodeDiv in episodeDivs:
            aParent = episodeDiv.parent
            epHref = aParent['href']
            enEpName = episodeDiv.select('span.myseriesbten')[0].string.strip()
            ruEpName = episodeDiv.select('span.myseriesbtru')[0].string.strip()
            hasHQ = len(episodeDiv.select('span.myserieshq')) > 0
            hasENSound = len(episodeDiv.select('span.myseriesesound')) > 0
            hasRUSound = len(episodeDiv.select('span.myseriesrsound')) > 0
            hasENSubs = len(episodeDiv.select('span.myseriesesub')) > 0
            hasRUSubs = len(episodeDiv.select('span.myseriesrsub')) > 0
            unwatchedEpisodes.append({'href': epHref, 'en':enEpName, 'ru':ruEpName
                                    ,'hasHQ':hasHQ, 'hasENSound':hasENSound, 'hasRUSound':hasRUSound
                                    , 'hasRUSubs':hasRUSubs, 'hasENSubs':hasENSubs})
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
            subtitle = ""
            subtitle += "hd " if episode['hasHQ'] else ""
            if episode['hasENSound'] or episode['hasRUSound']:
                subtitle += "sound: "
                subtitle += "ru, " if episode['hasRUSound'] else ""
                subtitle += "en " if episode['hasENSound'] else ""
            if subtitle.endswith(', '):
                subtitle = subtitle[:-2] + ' '
            if episode['hasENSubs'] or episode['hasRUSubs']:
                subtitle += "subs: "
                subtitle += "ru, " if episode['hasRUSubs'] else ""
                subtitle += "en" if episode['hasENSubs'] else ""
            if subtitle.endswith(', '):
                subtitle = subtitle[:-2]
            iDict = dict(title=title, subtitle=subtitle, uid=episode['href'], valid=True, arg=TURBOFILM_URL + episode['href'])
            items.append(alp.Item(**iDict))
        pass
    else:
        for ser in series:
            iDict = dict(title=ser['en'] + ' ' + ser['ru'], subtitle=ser['href'], uid=ser['id'], valid=False, autocomplete=ser['id'])
            items.append(alp.Item(**iDict))

alp.feedback(items)
