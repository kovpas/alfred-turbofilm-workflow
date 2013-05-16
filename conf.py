import os
import alp
import json
import time
from tempfile import gettempdir
from cookielib import LWPCookieJar


CACHE_TIME = 60
TURBOFILM_URL = 'https://turbofilm.tv'
LOGIN_URL = TURBOFILM_URL + '/Signin'
MY_SERIES_URL = TURBOFILM_URL + '/My/Series'

cookie_file = '.turbofilm.cookies.txt'
cache_file = '.turbofilm.cache.txt'
cookie_jar = LWPCookieJar(cookie_file)
cached_series = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31',
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    # 'Accept-Encoding': 'gzip,deflate,sdch',
    # 'Accept-Language':'en-US,en;q=0.8',
    # 'Cache-Control':'max-age=0',
    # 'Connection':'keep-alive',
    # 'Host':'turbofilm.tv',
    # 'Origin':'https://turbofilm.tv',
    # 'Referer':'https://turbofilm.tv/Signin'
}

def __initCookies():
    if cookie_file:
        try:
            cookie_jar.load(cookie_file, ignore_discard=True)
        except IOError:
            pass

def __initCache():
    if cache_file:
        try:
            if time.time() - os.path.getctime(cache_file) > CACHE_TIME:
                os.remove(cache_file)
            else:
                with open(cache_file) as cache_fp:
                    cached_series.extend(json.load(cache_fp))
                alp.log('Cached series found')
                alp.log(cached_series)
        except Exception:
            pass

__initCookies()
__initCache()