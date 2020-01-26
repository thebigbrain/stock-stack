# -*- coding:utf-8 -*-
from base.elastic import es
from base.stocks import get_reports


symbol = 'SH601166'


if __name__ == '__main__':
    get_reports(es, symbol)
