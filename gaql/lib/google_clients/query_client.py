from gaql import DEFAULT_LIMIT
from gaql.lib.google_clients.completion.account import Account
from gaql.lib.google_clients.google_ads_service import GoogleAdsServiceInstance


class QueryClient:
    def __init__(
            self,
            initial_account: Account,
            default_limit: int = DEFAULT_LIMIT
    ):
        self._ads_service = None
        self.account = initial_account
        self.limit = default_limit

    def set_account(self, account: Account):
        if isinstance(account, Account):
            self.account = account

    def set_limit(self, limit: int):
        if isinstance(limit, int) and limit > 0:
            self.limit = limit

    def parse_query(self, query):
        base_query = query.replace(';', '')
        if 'limit' in base_query.lower():
            return base_query
        else:
            return base_query + ' LIMIT ' + str(self.limit)

    def query(self, query: str):
        response = GoogleAdsServiceInstance.get_instance().search_stream(
            self.account.account_id, query
        )
        for batch in response:
            for row in batch.results:
                yield row
