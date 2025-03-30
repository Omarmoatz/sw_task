from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny

from sw_task.categories.models import Category
from sw_task.categories.api.serializers import CategoryListSerializer, CategoryCreateSerializer
from sw_task.categories.service import CategoriesService


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "create":
            return CategoryCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        parent_id = self.request.GET.get("parent_id")
        categories = (
            CategoriesService().get_subcategories(parent_id, ())
            if parent_id
            else CategoriesService().get_categories()
        )
        return categories
    
    def perform_create(self, serializer):
        self.created_objects = serializer.save()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            CategoryListSerializer(self.created_objects, many=True).data,
            status= status.HTTP_201_CREATED
        )
    