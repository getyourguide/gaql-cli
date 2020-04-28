import click

from gaql.lib.click_decorators.state import common_options, pass_state
from gaql.lib.google_clients.config import setup_client
from gaql.lib.google_clients.queries import google_fields_query
from gaql.lib.output import write_rows, print_gaql
from gaql.lib.repl import run_as_repl, parse_query
from gaql.tools.queries import clients_cmd


@click.group(context_settings=dict(max_content_width=120))
@common_options
@pass_state
def tools(state):
    pass


@tools.group()
@pass_state
def queries(state):
    """Saved common queries for GoogleAds"""
    state.finalize([])


@tools.command()
@click.argument('entity', required=True)
@pass_state
def fields_for(state, entity):
    """Query selectable fields for a specific entity"""
    state.finalize(entity)

    client = setup_client()
    query_method = google_fields_query(client)

    query = f"SELECT name, attribute_resources, selectable_with WHERE name = '{entity}'"

    print_gaql(query)
    rows = query_method(parse_query(query))
    write_rows(rows, state)


@tools.command()
@click.argument('query', nargs=-1)
@pass_state
def fields(state, query):
    """Make queries about field metadata for GoogleAds entities"""
    state.finalize(query)

    client = setup_client()
    query_method = google_fields_query(client)

    if len(query) == 0:
        run_as_repl(query_method, state, completion=False)
    else:
        rows = query_method(parse_query(' '.join(query)))
        write_rows(rows, state)


@queries.command()
@pass_state
def clients(state):
    """Returns all the clients"""
    clients_cmd(state)
