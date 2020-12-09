from enum import Enum
from json import dump

from google.protobuf.json_format import MessageToJson, MessageToDict

from gaql.lib.functional import chain
from gaql.lib.output import flatten

class OutputFormat(Enum):
    CSV = "csv"
    JSON = "json"
    JSONL = "jsonl"
    PROTO = "proto"


FORMAT_NAMES = [enum.name for enum in OutputFormat]
def is_format(format: str) -> bool:
    return format.upper() in FORMAT_NAMES

def get_format(format: str) -> OutputFormat:
    return OutputFormat[format.upper()]

class Formatter:
    def __init__(self, stream, format: OutputFormat):
        self.stream = stream
        self.format = format

    def set_format(self, format: str):
        if not is_format(format):
            raise Exception(f"Attempted to set an unrecognised format {format}")
        self.format = get_format(format)

    def formats(self):
        return ', '.join(FORMAT_NAMES)

    def proto_to_dict(self, row):
        return MessageToDict(row, preserving_proto_field_name=True)

    def write_csv(self, rows):
        import csv
        import json

        convert_row = chain(MessageToJson, json.loads, flatten)

        rows = iter(rows)
        first_row = next(rows, None)

        if first_row:
            first_row = convert_row(first_row)
            writer = csv.DictWriter(self.stream, first_row.keys())
            writer.writeheader()
            writer.writerow(first_row)
            for row in rows:
                row = convert_row(row)
                writer.writerow(row)

    def write_json(self, rows):
        for row in rows:
            print(MessageToJson(row, preserving_proto_field_name=True), file=self.stream)

    def write_json_lines(self, rows):
        for row in rows:
            dump(self.proto_to_dict(row), fp=self.stream, separators=(',', ':'))
            self.stream.write('\n')

    def write_proto(self, rows):
        for row in rows:
            print(row, file=self.stream)

    def write_rows(self, rows):
        if self.format == OutputFormat.JSON:
            self.write_json(rows)
        elif self.format == OutputFormat.JSONL:
            self.write_json_lines(rows)
        elif self.format == OutputFormat.CSV:
            self.write_csv(rows)
        else:
            self.write_proto(rows)
