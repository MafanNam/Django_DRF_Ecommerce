from rest_framework import viewsets
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from .models import Brand, Product, Category
from .serializers import BrandSerializer, ProductSerializer, CategorySerializer


class CategoryViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for viewing categories
    """

    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)

