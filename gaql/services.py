"""
    Service for running GAQL queries
"""
import logging

import google
import pandas as pd
from flask import flash
from werkzeug.contrib.cache import SimpleCache


from . import google_ads_api
from .errors import AttributeValueException
from .errors import ParseSelectException

logger = logging.getLogger(__name__)

cache = SimpleCache()


def run_query_to_df(customer_id, query):
    """ Run GAQL query and return pandas Dataframe """
    customer_id = customer_id.replace('-', '')
    cached_df = cache.get((customer_id, query))
    if cached_df is None:
        cached_df = _run_query(customer_id, query)
        if cached_df.empty:
            return cached_df
    cache.set((customer_id, query), cached_df, timeout=5*60)
    return cached_df


def _run_query(customer_id, query):
    client = google_ads_api.get_client()
    try:
        obj_list = google_ads_api.run_query(client, customer_id, query)
        columns = list(_parse_select(query))
        data = list(map(_mapper_obj_to_list(columns), obj_list))
        return pd.DataFrame(data, columns=columns)
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        for error in ex.failure.errors:
            err_msg = error.message
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    err_msg += f'\n\tOn field: \
                        {field_paqth_element.field_name}'
            flash(err_msg)
        logger.warning(ex)
    except google.api_core.exceptions.DeadlineExceeded as ex:
        flash('Google Ads API gateway timeout error')
        logger.warning(ex)
    except AttributeValueException as ex:
        flash(str(ex))
    except ParseSelectException as ex:
        flash(str(ex))
        logger.warning('Query=%s; Err=%s', query, ex)

    return pd.DataFrame()


def _parse_select(query):
    """Get selected attributes from query
    Given "select adGroup.name, campaign.name"
    returns ["adGroup.name", "campaign.name"]
    """
    lower_query = query.lower()
    if 'select' not in lower_query:
        raise ParseSelectException('"SELECT" not found in query')
    rightside = lower_query.split('select')[1]
    if 'from' not in rightside:
        raise ParseSelectException('"FROM" not found in query')
    attrs_str = rightside.split('from')[0]
    attrs = attrs_str.split(',')
    return map(lambda s: s.strip(), attrs)


def _mapper_obj_to_list(columns):
    return lambda x: _obj_to_list(x, columns)


def _obj_to_list(obj, columns):
    """
        Given an object like { adGroup: { name: "my-name" } }
        and columns ["adGroup.name"]
        returns ["my-name"]
    """
    return map(_mapper_column_to_value(obj), columns)


def _mapper_column_to_value(obj):
    return lambda x: _get_value_by_name(obj, x)


def _get_value_by_name(obj, attr):
    """
        Given an object like { adGroup: { name: "my-name" } }
        and an attr "adGroup.name"
        returns "my-name"
    """
    attrs = attr.split('.')
    return _get_value(obj, attrs)


def _get_value(obj, all_attrs):
    """
        Given an object like { adGroup: { location: { name: "my-name" } } }
        and an attr list ["adGroup", "location", "name"]
        recursively calls itself with a head of attr list and sub-object
    """
    def helper(obj, attrs):
        first = attrs[0]
        rest = attrs[1:]
        try:
            if rest:
                new_obj = getattr(obj, first)
                return helper(new_obj, rest)
            return _get_value_base(obj, first)
        except AttributeError as err:
            column = '.'.join(all_attrs)
            message = f'"{first}" can not be processed correctly in "{column}"'
            logger.error('%s; err=%s', message, err)
            raise AttributeValueException(message)

    return helper(obj, all_attrs)


def _get_value_base(obj, attr):
    """
        Given an Adwords resource
        and an attr name
        returns the value of the attr
    """
    value = getattr(obj, attr)
    if attr == 'match_type':
        return value
    return getattr(value, 'value')
