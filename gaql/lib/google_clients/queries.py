from gaql import DEFAULT_LIMIT
from gaql.lib.google_clients.config import setup_ads_service, setup_fields_service
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def google_ads_query(client, account_id):
    service = setup_ads_service(client) 

    def do_query(query):
        search_request = client.get_type("SearchGoogleAdsStreamRequest")
        search_request.customer_id = account_id
        search_request.query = query
        response = service.search_stream(search_request)
        for batch in response:
            for row in batch.results:
                yield row._pb

    return do_query


def google_fields_query(client):
    service = setup_fields_service(client)

    def do_query(query):
        return service.search_google_ads_fields(query, page_size=int(DEFAULT_LIMIT))

    return do_query
