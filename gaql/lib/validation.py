import re

import click


def read_account_id(value):
    if not re.match('\\d{3}-?\\d{3}-?\\d{4}$', value):
        raise click.BadParameter('account id must be a 10-digit number or ???-???-????')

    return int(value.replace('-', ''))
