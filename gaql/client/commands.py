import click

from gaql.lib.click_decorators.state import common_options, pass_state
from gaql.lib.formatter import Formatter
from gaql.lib.google_clients.completion.accounts_completer import AccountCompleter
from gaql.lib.google_clients.completion.command_completer import CommandCompleter
from gaql.lib.google_clients.completion.completer import GaqlCliCompleter
from gaql.lib.google_clients.completion.google_completer import GoogleCompleter
from gaql.lib.google_clients.query_client import QueryClient
from gaql.lib.repl import Repl


def complete_accounts(ctx, args, incomplete):
    completer = AccountCompleter()
    for account in completer.get_accounts_by_identifier(incomplete):
        yield account.name


@click.command(context_settings=dict(max_content_width=120))
@click.argument('account', autocompletion=complete_accounts)
@click.argument('query', nargs=-1)
@common_options
@pass_state
def cli(state, account, query):
    state.finalize(query)
    account_completer = AccountCompleter()
    account = account_completer.get_account_from_identifier(account)
    query_client = QueryClient(account)
    formatter = Formatter(state.output, state.format)

    if len(query) == 0:
        completer = GaqlCliCompleter(
            google_completer=GoogleCompleter(),
            account_completer=account_completer,
            command_completer=CommandCompleter()
        )
        Repl(completer, query_client, formatter).start()
    else:
        rows = query_client.query(query_client.parse_query(' '.join(query)))
        formatter.write_rows(rows)
