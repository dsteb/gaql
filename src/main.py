"""This example illustrates how to get campaign criteria.

Retrieves negative keywords in a campaign.
"""

from __future__ import absolute_import

import argparse
import logging
import sys

import google.ads.google_ads.client
import pandas as pd
import six

_DEFAULT_PAGE_SIZE = 1000

LOG = logging.getLogger(__name__)

def run_query(client, customer_id, page_size):
    """Run the query and print the result"""
    ga_service = client.get_service('GoogleAdsService', version='v1')

    query = ('SELECT campaign.id, campaign.name, ad_group.id, ad_group.name, '
             'ad_group_criterion.criterion_id, '
             'ad_group_criterion.keyword.text, '
             'ad_group_criterion.keyword.match_type, '
             'metrics.impressions, metrics.clicks, metrics.cost_micros '
             'FROM keyword_view WHERE segments.date DURING LAST_7_DAYS '
             'AND campaign.advertising_channel_type = \'SEARCH\' '
             'AND ad_group.status = \'ENABLED\' '
             'AND ad_group_criterion.status IN (\'ENABLED\', \'PAUSED\') '
             'ORDER BY metrics.impressions DESC '
             'LIMIT 50')

    response = ga_service.search(customer_id, query, page_size=page_size)

    try:
        attrs = _parse_select_attrs(query)
        values = []

        for row in response:
            row_values = []
            for attr in attrs:
                val = _get_attr_by_str(row, attr)
                row_values.append(val)
            values.append(row_values)

        df = pd.DataFrame(values, columns=attrs)

        print(df.head)

    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)


def _get_attr_by_str(obj, attr_str):
    try:
        attrs = _get_attr_name(attr_str).split('.')
        return _get_attrs(obj, attrs)
    except Exception as err:
        LOG.error('Attr=%s; err=%s', attr_str, err)
        raise err


def _get_attr_name(attr):
    last = attr.split('.')[-1]
    if last == 'match_type':
        return attr
    return attr + '.value'


def _get_attrs(obj, attrs):
    first = attrs[0]
    rest = attrs[1:]
    new_obj = getattr(obj, first)
    if rest:
        return _get_attrs(new_obj, rest)
    return new_obj


def _parse_select_attrs(query):
    """Get selected attributes from query"""
    rightside = query.lower().split('select ')[1]
    attrs_str = rightside.split('from ')[0]
    attrs = attrs_str.split(',')
    return list(map(lambda s: s.strip(), attrs))


def _strip(customer_id):
    """
    Customer id should contain only digits.
    Example "123-456-7890" => "1234567890"
    """
    return customer_id.replace('-', '').strip()


def main(page_size):
    """ Main method to initialize API and parse the args"""
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = google.ads.google_ads.client.GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(description=('Retrieves a campaign\'s negative keywords.'))
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=six.text_type, required=True, help='The Google Ads customer ID.')
    args = parser.parse_args()
    run_query(google_ads_client, _strip(args.customer_id), page_size)

if __name__ == '__main__':
    main(_DEFAULT_PAGE_SIZE)
