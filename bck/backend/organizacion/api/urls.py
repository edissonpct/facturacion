from rest_framework.routers import DefaultRouter
from organizacion.api.views import EmpresaViewSet

router = DefaultRouter()
router.register('empresas',EmpresaViewSet, basename='empresa')
urlpatterns = router.urls