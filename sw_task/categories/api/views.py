from rest_framework.response import Response
from rest_framework import viewsets, mixins


from sw_task.categories.models import Category
from sw_task.categories.api.serializers import CategoryListSerializer
from sw_task.categories.service import CategoriesService


class CategoryViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


    def get_queryset(self):
        parent_id = self.request.GET.get("parent_id")
        categories = (
            CategoriesService().get_subcategories(parent_id, ())
            if parent_id
            else CategoriesService().get_categories()
        )
        return categories
    