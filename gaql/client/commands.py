import click

from gaql.lib.click_decorators.state import common_options, pass_state
from gaql.lib.google_clients.config import setup_client
from gaql.lib.google_clients.queries import google_ads_query
from gaql.lib.output import write_rows
from gaql.lib.repl import parse_query, run_as_repl
from gaql.lib.validation import validate_account_id


@click.command(context_settings=dict(max_content_width=120))
@click.argument('account_id', callback=validate_account_id)
@click.argument('query', nargs=-1)
@common_options
@pass_state
def cli(state, account_id, query):
    state.finalize(query)

    client = setup_client()
    query_method = google_ads_query(client, str(account_id))

    if len(query) == 0:
        run_as_repl(query_method, state, completion=True)
    else:
        rows = query_method(parse_query(' '.join(query)))
        write_rows(rows, state)
