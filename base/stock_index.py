# -*- coding:utf-8 -*-
import pandas as pd
from base.elastic import es

weight_url = 'http://www.csindex.com.cn/uploads/file/autofile/closeweight/000016closeweight.xls'
cons_url = 'http://www.csindex.com.cn/uploads/file/autofile/cons/000016cons.xls'
perf_url = 'http://www.csindex.com.cn/uploads/file/autofile/perf/000016perf.xls'
ror_url = 'http://www.csindex.com.cn/zh-CN/indices/index-detail-download/000016'
indicator_url = 'http://www.csindex.com.cn/uploads/file/autofile/indicator/000016indicator.xls'


NAME_CODE_MAP = {
    'sse50': '000016'
}


def get_weight_url(code):
    return f'http://www.csindex.com.cn/uploads/file/autofile/closeweight/{code}closeweight.xls'


def read_xls(url):
    return pd.read_excel(url)


def pub(index_name, index_code, primary_key, url):
    d_frame = read_xls(url)

    print(d_frame.columns)
    for d in d_frame.iterrows():
        series = d[1]
        doc_id = f'{index_code}_{series[primary_key]}'
        es.create(index=index_name, id=doc_id, body=dict(series))


def pub_weight(index_code):
    pub(
        index_name='stock_index_weight',
        index_code=NAME_CODE_MAP[index_code],
        primary_key='成分券代码Constituent Code',
        url=get_weight_url(index_code)
    )
