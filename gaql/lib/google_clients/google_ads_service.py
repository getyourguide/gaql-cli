from google.ads.google_ads.client import GoogleAdsClient
from gaql.lib.google_clients.config import load_credentials


class GoogleAdsServiceInstance:
    _instance: GoogleAdsClient = None

    @staticmethod
    def get_instance():
        if not GoogleAdsServiceInstance._instance:
            credentials = load_credentials()
            ads_client = GoogleAdsClient.load_from_dict(credentials)
            GoogleAdsServiceInstance._instance = ads_client.get_service(
                'GoogleAdsService', version='v6'
            )
        return GoogleAdsServiceInstance._instance
