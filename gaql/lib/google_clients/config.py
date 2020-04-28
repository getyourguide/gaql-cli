import click
import json
import os
import sys

from gaql import CONFIG_DIR, CREDENTIAL_FILE


def configure():
    login_customer_id = input('login_customer_id: ').replace('-', '')

    secrets = {
        'developer_token': input('developer_token: '),
        'client_id': input('client_id: '),
        'client_secret': input('client_secret: '),
        'login_customer_id': login_customer_id,
        'refresh_token': input('refresh_token: '),
    }

    os.makedirs(CONFIG_DIR, exist_ok=True)

    with CREDENTIAL_FILE.open('w') as f:
        print(f'Wrote credentials to {CREDENTIAL_FILE}')
        f.write(json.dumps(secrets, indent=4))


def read_credentials_from_file():
    def read_credential_file_json():
        with CREDENTIAL_FILE.open('r') as f:
            return json.load(f)

    try:
        return read_credential_file_json()
    except FileNotFoundError:
        print(f"Configuration file not found at : {CREDENTIAL_FILE}", file=sys.stderr)
        should_configure = click.confirm('Configure it now?')
        if should_configure:
            configure()
            return read_credential_file_json()
        ERROR_MSG = (
            "Cannot continue without credentials. Please add credentials to your environment, home directory,"
            " or fill out the credentials prompt."
        )
        print(ERROR_MSG, file=sys.stderr)
        sys.exit(1)



def load_credentials():
    """Loads credentials with the following ordering: from env, Google's yaml file, a custom .json file in .config/gaql"""
    from google.ads.google_ads import config
    try:
        return config.load_from_env()
    except:
        try:
            return config.load_from_yaml_file()
        except:
            if not CREDENTIAL_FILE.exists():
                print(f"Couldn't load credentials from the environment, or from ~/google-ads.yaml. Trying {CREDENTIAL_FILE}")
            return config.load_from_dict(read_credentials_from_file())


def get_root_client():
    return load_credentials()['login_customer_id']


def setup_client():
    from google.ads.google_ads.client import GoogleAdsClient
    credentials = load_credentials()
    return GoogleAdsClient.load_from_dict(credentials)


def setup_ads_service(client):
    return client.get_service('GoogleAdsService', version='v3')


def setup_fields_service(client):
    return client.get_service('GoogleAdsFieldService', version='v3')
