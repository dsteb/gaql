"""
    HTTP handlers for Query
"""
from flask import (
    Blueprint, render_template, request,
)

from . import services

bp = Blueprint('auth', __name__, url_prefix='/query')

_DEFAULT_PAGE_SIZE = 1000


@bp.route('/', methods=('GET', 'POST'))
def query_view():
    """GET/POST HTTP handler for query route"""
    if request.method == 'POST':
        query = request.form['query']
        customer_id = request.form['customer-id']

        df = services.run_query_to_df(customer_id, query)

        return render_template('query/view.html', table=_to_html(df),
                               customer_id=customer_id, query=query)

    return render_template('query/view.html')


def _to_html(df):
    return df.to_html(classes=['table', 'table-bordered', 'table-striped',
                               'table-hover'], index=False)
