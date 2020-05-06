from django.urls import path, include
from rest_framework import routers
from .views import ClientViewSet, UnitViewSet, DepartmentViewSet, CategoryViewSet, ProjectViewSet, SiteViewSet, \
    RequsitionViewSet, take_payload

router = routers.DefaultRouter()
router.register('clients', ClientViewSet)
router.register('units', UnitViewSet)
router.register('departments', DepartmentViewSet)
router.register('categories', CategoryViewSet)
router.register('projects', ProjectViewSet)
router.register('sites', SiteViewSet)
router.register('requistions', RequsitionViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('communication/', take_payload)
]
