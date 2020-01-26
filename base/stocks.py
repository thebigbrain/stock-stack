# -*- coding:utf-8 -*-
from base.crawler import crawl

base_url = 'https://stock.xueqiu.com/v5/stock/finance/cn'
i_url = f'{base_url}/indicator.json'
income_url = f'{base_url}/income.json'
balance_url = f'{base_url}/balance.json'
cash_url = f'{base_url}/cash_flow.json'


class ReportKind(object):
    INDICATOR = 'indicator'
    INCOME = 'income'
    BALANCE = 'balance'
    CASH = 'cash'


class ReportType(object):
    ALL = 'all'
    Q2 = 'Q2'   # Quarterly Report
    Q1 = 'Q1'   # Interim Report
    Q3 = 'Q3'   # Three Quarterly Report
    Q4 = 'Q4'   # Annual Report

    @staticmethod
    def name_to_type(name):
        if str(name).endswith('年报'):
            return ReportType.Q4

        if str(name).endswith('三季报'):
            return ReportType.Q3

        if str(name).endswith('中报'):
            return ReportType.Q2

        if str(name).endswith('一季报'):
            return ReportType.Q1


def get_report_base(url, kind, symbol, count=25, is_detail=True, timestamp=None):
    params = {
        'symbol': symbol,
        'type': ReportType.ALL,
        'is_detail': is_detail,
        'count': count,
        'timestamp': timestamp
    }
    r = crawl(url, params=params)
    data = r.json()['data']

    data['symbol'] = symbol
    data['report_kind'] = kind

    details = data['list']

    del data['list']

    return data, details


def get_main_indicator(**kwargs):
    return get_report_base(url=i_url, kind=ReportKind.INDICATOR, **kwargs)


def get_income(**kwargs):
    return get_report_base(url=income_url, kind=ReportKind.INCOME, **kwargs)


def get_balance(**kwargs):
    return get_report_base(url=balance_url, kind=ReportKind.BALANCE, **kwargs)


def get_cash_flow(**kwargs):
    return get_report_base(url=cash_url, kind=ReportKind.CASH, **kwargs)


def save_to_es_one(es, symbol, d, data):
    d.update(data)
    d['report_type'] = ReportType.name_to_type(d['report_name'])
    doc_id = '_'.join([symbol, data['report_kind'], str(d['report_date'])])
    es.index(index='stocks', id=doc_id, body=d)


def save_to_es(es, symbol, data, details):
    for d in details:
        save_to_es_one(es, symbol, d, data)


def get_reports(es, symbol):
    save_to_es(es, symbol, *get_main_indicator(symbol=symbol))
    save_to_es(es, symbol, *get_income(symbol=symbol))
    save_to_es(es, symbol, *get_balance(symbol=symbol))
    save_to_es(es, symbol, *get_cash_flow(symbol=symbol))