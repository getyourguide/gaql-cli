from gaql.lib.google_clients.config import get_root_client, setup_client
from gaql.lib.google_clients.queries import google_ads_query
from gaql.lib.output import write_rows, print_gaql


def clients_cmd(state):
    client = setup_client()
    query_method = google_ads_query(client, get_root_client())

    query = """SELECT
            customer.id,
            customer_client.descriptive_name,
            customer_client.id
        FROM
            customer_client
        LIMIT 1000"""
    print_gaql(query)
    rows = query_method(query)
    write_rows(rows, state)
