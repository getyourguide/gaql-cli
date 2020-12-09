import pathlib

DEFAULT_LIMIT = 100
USER_HOME = pathlib.Path.home()

CONFIG_DIR = USER_HOME / '.config/gaql/'
CREDENTIAL_FILE = CONFIG_DIR / 'credentials.json'
HISTORY_FILE = CONFIG_DIR / 'history'
ACCOUNTS_FILE = CONFIG_DIR / 'accounts.json'
