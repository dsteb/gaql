"""
Google Ads API client

"""
import google.ads.google_ads.client

from flask import g

_DEFAULT_PAGE_SIZE = 1000


def get_client():
    """Get client instance"""
    if 'google_ads_api' not in g:
        g.google_ads_api = google.ads.google_ads.client.GoogleAdsClient \
                .load_from_storage()
    return g.google_ads_api


def run_query(client, customer_id, query, page_size=_DEFAULT_PAGE_SIZE):
    """Run the query and return the result"""
    ga_service = client.get_service('GoogleAdsService', version='v1')

    return ga_service.search(customer_id, query, page_size=page_size)
