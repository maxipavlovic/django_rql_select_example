from rest_framework.routers import SimpleRouter

from .api.views import ProductView

router = SimpleRouter()
router.register(r'products', ProductView, basename='products')

urlpatterns = router.urls
