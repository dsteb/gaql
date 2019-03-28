from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import google.ads.google_ads.client
import pandas as pd

bp = Blueprint('auth', __name__, url_prefix='/query')

_DEFAULT_PAGE_SIZE = 1000


@bp.route('/', methods=('GET', 'POST'))
def query_view():
    if request.method == 'POST':
        query = request.form['query']
        customer_id = request.form['customer-id']
        df = _execute_query(customer_id, query)

        return render_template('query/view.html', table=df.to_html(),
                               customer_id=customer_id, query=query)

    return render_template('query/view.html')


def _execute_query(customer_id, query):
    google_ads_client = google.ads.google_ads.client.GoogleAdsClient \
        .load_from_storage()

    return run_query(google_ads_client, customer_id, query, _DEFAULT_PAGE_SIZE)


def run_query(client, customer_id, query, page_size):
    """Run the query and print the result"""
    ga_service = client.get_service('GoogleAdsService', version='v1')

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

        return pd.DataFrame(values, columns=attrs)
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)


def _parse_select_attrs(query):
    """Get selected attributes from query"""
    rightside = query.lower().split('select ')[1]
    attrs_str = rightside.split('from ')[0]
    attrs = attrs_str.split(',')
    return list(map(lambda s: s.strip(), attrs))


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
