from dj_rql.filter_cls import RQLFilterClass
from dj_rql.qs import SelectRelated

from ..models import Product


class ProductFilters(RQLFilterClass):
    MODEL = Product
    SELECT = True
    FILTERS = (
        {
            'filter': 'id',
            'ordering': True,
        },
        {
            'filter': 'name',
            'search': True,
        },
        {
            'namespace': 'category',
            'filters': ('id', 'name'),
            'qs': SelectRelated('category'),
        },
        {
            'namespace': 'company',
            'filters': ('id', 'name'),
            'hidden': True,
            'qs': SelectRelated('company'),
        },
    )
