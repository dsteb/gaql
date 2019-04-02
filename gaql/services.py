"""
    Service for running GAQL queries
"""
import logging

import pandas as pd

from . import google_ads_api

logger = logging.getLogger(__name__)


def run_query_to_df(customer_id, query):
    """ Run GAQL query and return pandas Dataframe """
    client = google_ads_api.get_client()
    obj_list = google_ads_api.run_query(client, customer_id, query)
    columns = list(_parse_select(query))

    data = list(map(_mapper_obj_to_list(columns), obj_list))

    return pd.DataFrame(data, columns=columns)


def _parse_select(query):
    """Get selected attributes from query
    Given "select adGroup.name, campaign.name"
    returns ["adGroup.name", "campaign.name"]
    """
    rightside = query.lower().split('select ')[1]
    attrs_str = rightside.split('from ')[0]
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


def _get_value(obj, attrs):
    """
        Given an object like { adGroup: { location: { name: "my-name" } } }
        and an attr list ["adGroup", "location", "name"]
        recursively calls itself with a head of attr list and sub-object
    """
    first = attrs[0]
    rest = attrs[1:]
    try:
        if rest:
            new_obj = getattr(obj, first)
            return _get_value(new_obj, rest)
        return _get_value_base(obj, first)
    except Exception as err:
        logger.error('Attrs=%s; first=%s; err=%s', attrs, first, err)
        raise err


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
