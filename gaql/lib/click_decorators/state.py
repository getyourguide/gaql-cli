import os
import sys

import click

from gaql import FORMATS


class State(object):
    def __init__(self):
        self.output = sys.stdout
        self.format = None

    def finalize(self, query):
        self.__validate_output(query)
        self.format = self.__coerce_format()

    def __validate_output(self, query):
        if not self.output or self.output.name == '<stdout>':
            return

        if len(query) == 0:
            click.echo('[FATAL]: if output is set, a query must be provided', sys.stderr)
            sys.exit(1)

    def __coerce_format(self):
        """
        If a file format was provided, use that format, otherwise use the filename's format
        if it's a supported format. Otherwise, default to json
        """
        if self.format:
            return self.format

        filename = self.output.name
        if '.' in filename:
            ext = os.path.splitext(filename)[1][1:]
            if ext in FORMATS:
                return ext
        return 'json'


pass_state = click.make_pass_decorator(State, ensure=True)


def output_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(State)
        state.output = value
        return value

    return click.option(
        '-o',
        '--output',
        type=click.File('w'),
        help='allows outputting to a file',
        default='-',
        expose_value=False,
        callback=callback,
    )(f)


def format_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(State)
        state.format = value
        return value

    return click.option(
        '-f',
        '--format',
        type=click.Choice(['json', 'jsonl', 'csv', 'proto'], case_sensitive=False),
        help='the format to output rows in (defaults to json)',
        expose_value=False,
        callback=callback,
    )(f)


def common_options(f):
    f = output_option(f)
    f = format_option(f)
    return f
