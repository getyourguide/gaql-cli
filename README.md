# GAQL CLI

[![PyPI version](https://badge.fury.io/py/gaql.svg)](https://badge.fury.io/py/gaql)
![PyPI downloads](https://img.shields.io/pypi/dm/gaql)

A CLI for running [GoogleAds queries](https://developers.google.com/google-ads/api/docs/query/overview).

## Usage
### Installing

- `pip install gaql`
- `pipx install gaql` (recommended)

### Querying
The default mode. Runs either as a REPL, or as a one off command

```bash
- gaql [ACCOUNT_ID] - run in REPL mode
- gaql [ACCOUNT_ID] [WORDS*] - run a single query. Note depending on your shell you may need to quote some queries if you run like this.

flags:
--help show the help message; basically the below
-f|--format <csv|json|jsonl|proto> specify an output format
-o|--output <file> specify an output file. Based on the extension, format is inferred. Non REPL usage only
```

Examples, using 1-000-000-000 as our demo account id:
```bash
# opens a REPL with json lines as the output format
gaql -f jsonl 1-000-000-000

# runs the query against the given account, outputting to the terminal the results as json lines
gaql -f jsonl 1-000-000-000 'SELECT campaign.id FROM campaign'

# runs the query against the given account, outputting to 'campaigns.jsonl' the result as json lines
gaql -o campaigns.jsonl 1-000-000-000 'SELECT campaign.id FROM campaign'
```

**tip**: by default `LIMIT 100` will be added to your queries. To override this behavior, simply define your own `LIMIT X`.

**tip**: the autocomplete will return only valid fields for the selected entity if you fill out the `FROM <entity>` part
first.

### Other tools
Used for useful common queries. Currently only supports getting all accounts under an MCC, to help when managing multiple accounts. The MCC is taken from the `login_customer_id` field.
- `gaql-tools queries clients`

## Notes
- credentials come from the environment > the google .yaml file > a user provided credential file
- credentials, settings, and history are stored in `./config/gaql/*`. The credential file will only be present if you create it through a prompt (i.e you aren't using the ENV, or the YAML file Google specifies)

## Ideas / TODO
- tables as an output format
- autocomplete for account ids (with caching)

## Development
We're using [poetry](https://github.com/python-poetry/poetry) for local development, package management, and publishing. `pyenv` is
recommended for Python version management, and `pipx` for installation.

Build commands:

```
make develop - install a development version. run via `poetry run gaql <args>`
make publish - build and distribute to PyPi
make clean   - remove the existing build files
make format  - run black over the code
make lint    - lint and format the code
```

## Security
For sensitive security matters please contact security@getyourguide.com.

## Legal
gaql-cli is licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for the full text.
