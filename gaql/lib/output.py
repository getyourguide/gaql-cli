"""Output GoogleAdsRows in different formats"""
import collections
import inspect
from json import dump

from google.protobuf.json_format import MessageToJson, MessageToDict
from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter

from gaql.lib.functional import chain
from gaql.lib.lexer import GaqlLexer


def flatten(d, parent_key=''):
    """recursively flatten a nested dictionary of reasonable depth"""
    items = []
    for k, v in d.items():
        key = parent_key + '.' + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, key).items())
        else:
            items.append((key, v))
    return dict(items)


def print_gaql(query, lexer=GaqlLexer()):
    print(highlight(inspect.cleandoc(query), lexer, Terminal256Formatter()))


def write_csv(stream, rows):
    import csv
    import json

    convert_row = chain(MessageToJson, json.loads, flatten)

    rows = iter(rows)
    first_row = next(rows, None)

    if first_row:
        first_row = convert_row(first_row)
        writer = csv.DictWriter(stream, first_row.keys())
        writer.writeheader()
        writer.writerow(first_row)
        for row in rows:
            row = convert_row(row)
            writer.writerow(row)


def to_dict(row):
    return MessageToDict(row, preserving_proto_field_name=True)


def write_json(stream, rows):
    for row in rows:
        print(MessageToJson(row), file=stream)


def write_json_lines(stream, rows):
    for row in rows:
        dump(to_dict(row), fp=stream, separators=(',', ':'))
        stream.write('\n')


def write_proto(stream, rows):
    for row in rows:
        print(row, file=stream)


def write_rows(rows, state):
    if state.format == 'json':
        write_json(state.output, rows)
    elif state.format == 'jsonl':
        write_json_lines(state.output, rows)
    elif state.format == 'csv':
        write_csv(state.output, rows)
    else:
        write_proto(state.output, rows)
