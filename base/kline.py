# -*- coding:utf-8 -*-
import time
from pandas import Series
# from base.elastic import es
# from pprint import pprint
from base.crawler import crawl

KLINE_BASE_URL = 'https://stock.xueqiu.com/v5/stock/chart/kline.json'
DEFAULT_INDICATOR = 'kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance'


def get_kline(symbol='SH000016', period='week', direction='before', count=142, indicator=DEFAULT_INDICATOR, begin=None):
    begin = begin or int(time.time() * 1000)
    params = {
        'symbol': symbol,
        'begin': begin,
        'period': period,
        'type': direction,
        'count': -count,
        'indicator': indicator
    }
    r = crawl(url=KLINE_BASE_URL, params=params)
    data = r.json()['data']
    column = data['column']
    res = []
    for d in data['item']:
        body = Series(d, index=column)
        body.dropna(inplace=True)
        body['name'] = '上证50'
        body['symbol'] = data['symbol']
        body['kline_type'] = period
        body['updated_at'] = begin / 1000
        body['timestamp'] = body['timestamp'] / 1000
        res.append(dict(body))
        # timestamp = int(body['timestamp'])
        # _id = f'{period}_{timestamp}'
        # pprint(dict(body))
        # es.index(index='stock_kline', id=_id, body=dict(body))

    return res
