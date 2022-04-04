import google.ads.googleads.client
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.filters import is_searching

from gaql import DEFAULT_LIMIT, HISTORY_FILE
from gaql.lib.google_clients.completion.google_completer import GoogleCompleter
from gaql.lib.lexer import GaqlLexer
from gaql.lib.output import write_rows, print_gaql

_SESSION = None


def setup_session(completion):
    global _SESSION
    bindings = KeyBindings()
    lexer = PygmentsLexer(GaqlLexer)

    @bindings.add('c-m', filter=~is_searching)
    def _(event):
        if ';' in event.current_buffer.text:
            event.current_buffer.validate_and_handle()
        else:
            event.current_buffer.insert_text('\n')

    _SESSION = PromptSession(
        multiline=True,
        key_bindings=bindings,
        lexer=lexer,
        history=FileHistory(HISTORY_FILE),
        completer=GoogleCompleter() if completion else None,
    )


def read_query():
    query = _SESSION.prompt('> ')
    return parse_query(query)


def parse_query(query, unlimited=False):
    base_query = query.replace(';', '')
    if unlimited or 'limit' in base_query.lower():
        return base_query
    else:
        return base_query + ' LIMIT ' + DEFAULT_LIMIT


def run_as_repl(run_query, state, completion):
    setup_session(completion)
    print('running in interactive mode, write some GAQL...')

    try:
        while True:
            query = read_query()
            if query:
                print_gaql(query, _SESSION.lexer.pygments_lexer)
                try:
                    rows = run_query(query)
                    write_rows(rows, state)
                except google.ads.googleads.errors.GoogleAdsException as ex:
                    handle_google_ads_error(ex)
    except (EOFError, KeyboardInterrupt):
        print('\nBye!')


def handle_google_ads_error(ex):
    print(
        f'Request with ID "{ex.request_id}" failed with status'
        + f'{ex.error.code().name} and errors:'
    )
    for error in ex.failure.errors:
        print(f'\tError with message {error.message}')
