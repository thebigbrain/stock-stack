# -*- coding:utf-8 -*-
import csv
from flask import Flask, request, Response
from collection.mongo import db

app = Flask(__name__)


@app.route('/collection/<collection>')
def get_collections(collection):
    skip = request.args.get('skip') or 0
    _filter = request.args.get('filter') or {}

    total = db[collection].count_documents(_filter)
    limit = request.args.get('limit') or total

    cursor = db[collection] \
        .find(_filter) \
        .skip(int(skip)) \
        .limit(int(limit))

    data = []
    for doc in cursor:
        data.append(doc)

    return csv_response(data)


class Line(object):
    def __init__(self):
        self._line = None

    def write(self, line):
        self._line = line

    def read(self):
        return self._line


def iter_csv(data):
    line = Line()
    writer = csv.writer(line)
    for csv_line in data:
        writer.writerow(csv_line)
        yield line.read()


def csv_response(data, filename='data'):
    response = Response(iter_csv(data), mimetype='text/csv')
    response.headers['Content-Disposition'] = f'attachment; filename={filename}.csv'
    return response
