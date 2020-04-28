from gaql import DEFAULT_LIMIT
from gaql.lib.google_clients.config import setup_ads_service, setup_fields_service


def google_ads_query(client, account_id):
    service = setup_ads_service(client)

    def do_query(query):
        response = service.search_stream(account_id, query)
        for batch in response:
            for row in batch.results:
                yield row

    return do_query


def google_fields_query(client):
    service = setup_fields_service(client)

    def do_query(query):
        return service.search_google_ads_fields(query, page_size=int(DEFAULT_LIMIT))

    return do_query
