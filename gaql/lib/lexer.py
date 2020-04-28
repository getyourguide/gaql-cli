import re
from pygments.lexer import RegexLexer
from pygments.token import Text, Keyword


class GaqlLexer(RegexLexer):
    name = 'GAQL'
    aliases = 'gaql'
    filenames = ['*.gaql']

    flags = re.IGNORECASE
    tokens = {
        'root': [
            (r'\s+', Text),
            (
                r'\b(SELECT|FROM|LIMIT|WHERE|ORDER BY|BETWEEN|'
                r'LIKE|NOT LIKE|CONTAINS ANY|CONTAINS ALL|'
                r'CONTAINS NONE|IS NULL|IS NOT NULL|DURING|'
                r'AND|ASC|DESC|LAST_14_DAYS|LAST_30_DAYS|'
                r'LAST_7_DAYS|LAST_BUSINESS_WEEK|LAST_MONTH|'
                r'LAST_WEEK_MON_SUN|LAST_WEEK_SUN_SAT|THIS_MONTH|'
                r'THIS_WEEK_MON_TODAY|THIS_WEEK_SUN_TODAY|TODAY|'
                r'YESTERDAY)\b',
                Keyword,
            ),
        ]
    }
