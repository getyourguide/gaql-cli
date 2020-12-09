import re
from typing import Iterable

from prompt_toolkit.completion import Completer, Completion

import logging

from gaql.lib.google_clients.completion.accounts_completer import AccountCompleter
from gaql.lib.google_clients.completion.command_completer import CommandCompleter
from gaql.lib.google_clients.completion.google_completer import GoogleCompleter


class GaqlCliCompleter(Completer):
    def __init__(self, google_completer: GoogleCompleter, account_completer: AccountCompleter, command_completer: CommandCompleter):
        self.google_completer = google_completer
        self.account_completer = account_completer
        self.command_completer = command_completer

    def get_completions(self, document, complete_event) -> Iterable[Completion]:
        start, end = document.find_boundaries_of_current_word(WORD=True)

        # only autocomplete if we're at the end of the word, as the completion framework doesn't handle overwrites well
        if end != 0:
            return
        else:
            word = document.text[document.cursor_position + start : document.cursor_position + end]
            if document.text.startswith("\\"):
                if re.match('\\\\account ', document.text, re.IGNORECASE):
                    logging.debug("context: account")
                    yield from self.account_completer.complete(document, start, end, word)
                else:
                    yield from self.command_completer.complete(document, start, end, word)
            elif re.match('select ', document.text, re.IGNORECASE):
                logging.debug("context: select")
                yield from self.google_completer.complete(document, start, end, word)
            logging.debug("context: none")
