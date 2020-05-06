from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.response import Response
from .models import Client, Category, Department, Unit, Project, Site, Requisition
from .serializers import ClientSerializer, CategorySerializer, DepartmentSerializer, UnitSerializer, ProjectSerializer, \
    SiteSerializer, RequisitionSerializer, RequisitionUpdateSerializer, RequisitionCreateSerializer
from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    http_method_names = ['get', ]
    pagination_class = None


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get', ]
    pagination_class = None


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    http_method_names = ['get', ]
    pagination_class = None


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    http_method_names = ['get', ]
    pagination_class = None


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    http_method_names = ['get', ]
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['department', 'client', ]


class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    http_method_names = ['get', ]
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project', ]


class RequsitionViewSet(viewsets.ModelViewSet):
    queryset = Requisition.objects.all()
    serializer_class = RequisitionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['site', 'site__project']

    def create(self, request, *args, **kwargs):
        serializer = RequisitionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = RequisitionUpdateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


GOPON_NUMBER = "THISISOURGOPONNUMBER"


@csrf_exempt
@require_http_methods(["GET"])
def take_payload(request):
    print(request.headers['Authorization'])
    print(request.GET)
    data = {
        'name': 'Vitor',
        'location': 'Finland',
        'is_active': True,
        'count': 28
    }
    return JsonResponse(data)
