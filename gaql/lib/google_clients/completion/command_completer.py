import re

from prompt_toolkit.completion import Completion

from gaql.lib.formatter import FORMAT_NAMES


class CommandCompleter:
    """Completes generic commands without complex values"""
    COMMANDS = ["\\account", "\\format", "\\limit"]
    def complete(self, document, start, end, word):
        if len(document.text) + start == 0:
            for command in filter(lambda command: command.startswith(word.lower()), CommandCompleter.COMMANDS):
                yield Completion(command, start_position=start)
        elif re.match('\\\\format ', document.text, re.IGNORECASE):
            for name in FORMAT_NAMES:
                yield Completion(name, start_position=start)
