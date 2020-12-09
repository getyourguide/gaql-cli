import inspect
import re

import google.ads.google_ads.client
from prompt_toolkit import PromptSession
from prompt_toolkit.filters import is_searching
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.lexers import PygmentsLexer
from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter

from gaql import HISTORY_FILE
from gaql.lib.formatter import Formatter, is_format
from gaql.lib.google_clients.completion.completer import GaqlCliCompleter
from gaql.lib.google_clients.query_client import QueryClient
from gaql.lib.lexer import GaqlLexer


class Toolbar:
    def __init__(self, query_client: QueryClient, formatter: Formatter):
        self.query_client = query_client
        self.formatter = formatter

    def render(self):
        text = f" account_id: {self.query_client.account}, format: {self.formatter.format.name}, default_limit: {self.query_client.limit}"
        return [('class:bottom-toolbar', text)]


class Repl:
    def __init__(
        self, completer: GaqlCliCompleter, query_client: QueryClient, formatter: Formatter
    ):
        self.completer = completer
        self.session = self.setup_session(Toolbar(query_client, formatter))
        self.lexer = GaqlLexer()
        self.terminal_formatter = Terminal256Formatter()
        self.query_client = query_client
        self.formatter = formatter

    def print_gaql(self, query):
        text = highlight(inspect.cleandoc(query), self.lexer, formatter=self.terminal_formatter)
        print(text)

    def setup_session(self, toolbar: Toolbar):
        bindings = KeyBindings()
        lexer = PygmentsLexer(GaqlLexer)

        @bindings.add('c-m', filter=~is_searching)
        def _(event):
            if event.current_buffer.text.startswith('\\'):
                event.current_buffer.validate_and_handle()
            elif ';' in event.current_buffer.text:
                event.current_buffer.validate_and_handle()
            else:
                event.current_buffer.insert_text('\n')

        return PromptSession(
            multiline=True,
            key_bindings=bindings,
            lexer=lexer,
            history=FileHistory(HISTORY_FILE),
            completer=self.completer,
            bottom_toolbar=toolbar.render,
        )

    def run_query(self, prompt):
        query = self.query_client.parse_query(prompt)
        self.print_gaql(query)
        try:
            rows = self.query_client.query(query)
            self.formatter.write_rows(rows)
        except google.ads.google_ads.errors.GoogleAdsException as e:
            self.handle_google_ads_error(e)

    def set_limit(self, command):
        def usage():
            print(f"Usage: \\LIMIT <value > 0>")

        elems = command.split(" ")
        if len(elems) == 2:
            _, limit = elems
            if limit.isnumeric() and int(limit) > 0 :
                self.query_client.set_limit(int(limit))
            else:
                usage()
        else:
            usage()


    def set_format(self, command):
        elems = command.split(" ")
        if len(elems) == 2:
            _, format = elems
            if is_format(format):
                self.formatter.set_format(format)
            else:
                print(f"'{format}' is not a recognised format. Choose from {self.formatter.formats()}")
        else:
            print(f"Usage: \\FORMAT <{self.formatter.formats()}>")


    def set_account(self, command):
        elems = command.split(" ")
        if len(elems) == 2:
            _, account_identifier = elems
            account = self.completer.account_completer.get_account_from_identifier(
                account_identifier
            )
            if account:
                self.query_client.set_account(account)
            else:
                print(f"Couldn't find an account with the name {account_identifier}")
        else:
            print(f"Usage: \\ACCOUNT <id|name>")

    def start(self):
        print('running in interactive mode, write some GAQL...')

        try:
            while True:
                command = self.session.prompt('> ')
                if command.startswith("\\"):
                    if re.match('\\\\account', command, re.IGNORECASE):
                        self.set_account(command)
                    elif re.match('\\\\format', command, re.IGNORECASE):
                        self.set_format(command)
                    elif re.match('\\\\limit', command, re.IGNORECASE):
                        self.set_limit(command)
                    else:
                        print("Command not recognised")
                else:
                    self.run_query(command)
        except (EOFError, KeyboardInterrupt):
            print('\nBye!')

    def handle_google_ads_error(self, ex):
        print(
            f'Request with ID "{ex.request_id}" failed with status'
            + f'{ex.error.code().name} and errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message {error.message}')
