from functools import reduce


class Trie(object):
    def __init__(self):
        self.children = {}
        self.terminator = False

    def add(self, char):
        self.children[char] = Trie()

    def insert(self, word):
        node = self
        for char in word:
            if char not in node.children:
                node.add(char)
            node = node.children[char]
        node.terminator = True

    def contains(self, word):
        node = self
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.terminator

    def all_suffixes(self, prefix):
        results = []
        if self.terminator:
            results.append(prefix)
        if not self.children:
            return results
        return (
            reduce(
                lambda a, b: a + b,
                [node.all_suffixes(prefix + char) for (char, node) in self.children.items()],
            )
            + results
        )

    def autocomplete(self, prefix):
        node = self
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return list(node.all_suffixes(prefix))
