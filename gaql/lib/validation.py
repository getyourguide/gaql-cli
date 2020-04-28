import re

import click


def validate_account_id(ctx, param, value):
    if not re.match('\\d{3}-?\\d{3}-?\\d{4}$', value):
        raise click.BadParameter('account id must be a 10-digit number or ???-???-????')

    return int(value.replace('-', ''))
