from rest_framework.viewsets import ReadOnlyModelViewSet

from dj_rql.drf.backend import RQLFilterBackend

from ..models import Product
from .filters import ProductFilters
from .serializers import ProductSerializer


class ProductView(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = (RQLFilterBackend,)
    rql_filter_class = ProductFilters
    queryset = Product.objects.all()
