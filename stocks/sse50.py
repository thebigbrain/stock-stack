# -*- coding:utf-8 -*-
from base.stock_index import pub_weight
from base.kline import get_kline
from base.pg import db


def get_sse50_kline_week():
    symbol = 'SH000016'
    period = 'week'
    c = db.create_table(table_name='kline')
    data = get_kline(symbol=symbol, period=period, count=300)
    for d in data:
        c.upsert(d, ['symbol', 'kline_type', 'timestamp'])


if __name__ == '__main__':
    # pub_weight('sse50')
    get_sse50_kline_week()
