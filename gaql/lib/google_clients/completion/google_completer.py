import re
from prompt_toolkit.completion import Completer, Completion

from gaql.lib.google_clients.completion.autocompletions import COMPLETIONS
from gaql.lib.google_clients.completion.trie import Trie


class GoogleCompleter:
    """Provides autocompletion lookup got GoogleSearch fields
    TODO: the structure of words is grouped by a single entity prefix (e.g segment.x, campaign.y). We could probably
          split words up based on this structure instead of using a Trie.
    """

    _ALL = 'all'
    _FROM_REGEX = re.compile('FROM (\w+)')

    def __init__(self):
        self.autocompletion = COMPLETIONS

        self.previous_word = ''
        self.resource_trie = Trie()
        for key in self.autocompletion:
            self.resource_trie.insert(key)

        self.entity_completers = {}
        self.initialize_trie(self._ALL)

    def initialize_trie(self, entity):
        from gaql.lib.google_clients.completion.trie import Trie

        if entity in self.autocompletion:
            fields = self.autocompletion[entity]
            trie = Trie()
            for field in fields:
                trie.insert(field)
            self.entity_completers[entity] = trie

    def lookup(self, context, stub):
        if not context:
            context = self._ALL
        context = context.lower()

        if context in self.entity_completers:
            return self.entity_completers[context].autocomplete(stub)
        elif context in self.autocompletion:
            self.initialize_trie(context)
            return self.entity_completers[context].autocomplete(stub)
        else:
            return ['']

    def complete(self, document, start, end, word):
        context = self._FROM_REGEX.search(document.text)

        if context:
            word_is_context = (
                document.cursor_position >= context.start()
                and document.cursor_position <= context.end()
            )
            context = context.group(1)
        else:
            word_is_context = False

        if word_is_context:
            for result in self.resource_trie.autocomplete(word):
                yield Completion(result, start_position=start)
        else:
            for result in self.lookup(context, word):
                yield Completion(result, start_position=start)
