import logging
import os
import time
from typing import Optional

from prompt_toolkit.completion import Completion

from gaql import CONFIG_DIR
from gaql.lib.google_clients.completion.account import Account
from gaql.lib.google_clients.config import get_root_client
from gaql.lib.google_clients.query_client import QueryClient


class AccountCompleter:
    def __init__(self):
        root_account = get_root_client()
        self.query_client = QueryClient(Account("root", root_account))
        self.accounts_file = CONFIG_DIR / f"accounts_{root_account}.txt"
        self.accounts = []
        self.load_accounts_cache()

    def get_accounts(self):
        """finds accounts which match the given account_prefix"""
        query = f"""
            SELECT customer_client.id, customer_client.descriptive_name
            FROM customer_client
        """
        return [
            (result.customer_client.descriptive_name, result.customer_client.id)
            for result in self.query_client.query(query)
        ]

    def load_accounts_cache(self):
        seconds_in_one_day = 60 * 60 * 24

        def age_in_seconds():
            return time.time() - os.path.getmtime(self.accounts_file)

        if not self.accounts_file.exists() or age_in_seconds() > seconds_in_one_day:
            found_accounts = self.get_accounts()
            with open(self.accounts_file, 'w') as f:
                for (name, id) in found_accounts:
                    f.write(f"{name},{id}\n")

        accounts = []
        with open(self.accounts_file, 'r') as f:
            for line in f.readlines():
                name, id = line.split(",")
                accounts.append(Account(name=name, account_id=id.strip()))

        self.accounts = accounts

    def complete_id(self, account_id: str):
        return filter(lambda account: account.account_id.startswith(account_id), self.accounts)

    def get_accounts_by_name_matching_prefix(self, account_prefix: str):
        return filter(lambda account: account.name.startswith(account_prefix), self.accounts)

    def get_accounts_by_identifier(self, account_identifier: str):
        possible_account_id = account_identifier.replace('-', '')

        if account_identifier == "":
            yield from self.accounts
        elif possible_account_id.isnumeric():
            yield from self.complete_id(possible_account_id)
        else:
            yield from self.get_accounts_by_name_matching_prefix(possible_account_id)

    def get_account_from_identifier(self, account: str) -> Optional[Account]:
        if account.isnumeric():
            found_accounts = list(filter(lambda acc: acc.account_id == account, self.accounts))
            if len(found_accounts) == 0:
                found_accounts = [Account(account_id=account, name="unknown")]
        else:
            found_accounts = list(filter(lambda acc: acc.name == account, self.accounts))

        if len(found_accounts) == 1:
            return found_accounts[0]

    def complete(self, document, start, end, word):
        accounts = list(self.get_accounts_by_identifier(word))
        for account in accounts:
            logging.debug(account)

            if word.isnumeric():
                display_string = f"{account.account_id} ({account.name})"
                logging.debug(display_string)
                yield Completion(
                    text=account.account_id, start_position=start, display=display_string
                )
            else:
                yield Completion(text=account.name, display=account.name, start_position=start)
