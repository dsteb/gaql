"""
    HTTP handlers for Query
"""
import math

from flask import Blueprint, render_template, request

from . import services

bp = Blueprint('auth', __name__, url_prefix='/query')


DEFAULT_PAGE_SIZE = 50


@bp.route('/', methods=('GET', 'POST'))
def query_view():
    """GET/POST HTTP handler for query route"""
    if request.method == 'POST':
        query = request.form['query']
        customer_id = request.form['customer-id']
        page = int(request.form['page'])

        df = services.run_query_to_df(customer_id, query)
        total_items = len(df)
        df = _slice(df, page, DEFAULT_PAGE_SIZE)
        paginator = _get_pagination(df, page, DEFAULT_PAGE_SIZE, total_items)

        return render_template('query/view.html', table=_to_html(df),
                               customer_id=customer_id, query=query,
                               pagination=paginator)

    return render_template('query/view.html')


def _to_html(df):
    return df.to_html(classes=['table', 'table-bordered', 'table-striped',
                               'table-hover'])


def _slice(df, page, page_size):
    start, end = _page_to_positions(page, page_size)
    return df[start:end]


def _page_to_positions(page, page_size):
    start = page_size * (page - 1)
    return start, start + page_size


def _get_pagination(df, page, page_size, total_items):
    total_pages = math.ceil(total_items / page_size)
    visible = len(df) > 0
    if total_pages <= 1:
        visible = False
        pages = []
    elif total_pages == 2:
        pages = [1, 2]
    elif page <= 1:
        pages = [1, 2, 3]
    elif page >= total_pages:
        pages = [total_pages - 2, total_pages - 1, total_pages]
    else:
        pages = [page - 1, page, page + 1]

    return {
        'visible': visible,
        'has_previous': page > 1,
        'has_next': page < total_pages,
        'page': page,
        'pages': pages
    }