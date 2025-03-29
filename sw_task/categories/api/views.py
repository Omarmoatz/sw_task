from rest_framework.response import Response
from rest_framework import viewsets, mixins

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

    def get_serializer(self, *args, **kwargs):
        if self.action == "create":
            return CategoryCreateSerializer
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        parent_id = self.request.GET.get("parent_id")
        categories = (
            CategoriesService().get_subcategories(parent_id, ())
            if parent_id
            else CategoriesService().get_categories()
        )
        return categories
    