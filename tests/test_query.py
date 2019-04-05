"""
Test module for query parser
"""

import pytest

from context import gaql
from gaql.errors import ParseSelectException
from gaql.services import _parse_select


def test_extract_select_attrs():
    """ Test extracting attributes from query """
    query = ("""
SELECT campaign.id, campaign.name, ad_group.id, ad_group.name,
ad_group_criterion.criterion_id,
ad_group_criterion.keyword.text,
ad_group_criterion.keyword.match_type,
metrics.impressions, metrics.clicks, metrics.cost_micros
FROM keyword_view WHERE segments.date DURING LAST_7_DAYS
AND campaign.advertising_channel_type = "SEARCH"
AND ad_group.status = "ENABLED"
AND ad_group_criterion.status IN ("ENABLED", "PAUSED")
ORDER BY metrics.impressions DESC
LIMIT 50
""")

    expected = ['campaign.id', 'campaign.name',
                'ad_group.id', 'ad_group.name',
                'ad_group_criterion.criterion_id',
                'ad_group_criterion.keyword.text',
                'ad_group_criterion.keyword.match_type',
                'metrics.impressions', 'metrics.clicks', 'metrics.cost_micros']

    result = list(_parse_select(query))
    assert result == expected


@pytest.mark.xfail(raises=ParseSelectException)
def test_no_select_parse():
    """ Test extracting attributes from empty query """
    query = (' FROM ')
    _parse_select(query)
    assert False


@pytest.mark.xfail(raises=ParseSelectException)
def test_no_from_parse():
    """ Test extracting attributes from empty query """
    query = (' SELECT ')
    _parse_select(query)
    assert False
