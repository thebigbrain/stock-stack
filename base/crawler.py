# -*- coding:utf-8 -*-
import requests

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/79.0.3945.79 Safari/537.36'

session = requests.Session()
has_initialized = False


def pre_fetch():
    if has_initialized:
        return
    host_url = 'https://xueqiu.com/'
    session.headers.update({'User-Agent': USER_AGENT})
    session.get(host_url)


def crawl(url, params=None, headers=None):
    pre_fetch()

    if headers is None:
        headers = dict()
    session.headers.update(headers)

    return session.get(url=url, params=params)
