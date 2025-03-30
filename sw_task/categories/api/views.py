from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from sw_task.categories.models import Category
from sw_task.categories.api.serializers import (
    CategoryListSerializer, 
    CategoryCreateSerializer,
)
from sw_task.categories.service import CategoriesService

class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    # Define queryset and serializer for category
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        # Use a different serializer for create action
        if self.action == "create":
            return CategoryCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        # Retrieve categories based on parent_id filter
        parent_id = self.request.GET.get("parent_id")
        categories = (
            CategoriesService().get_subcategories(parent_id, ())
            if parent_id
            else CategoriesService().get_categories()
        )
        return categories
    
    def perform_create(self, serializer):
        # Save newly created objects
        self.created_objects = serializer.save()
    
    def create(self, request, *args, **kwargs):
        # Handle category creation and return serialized response
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            CategoryListSerializer(self.created_objects, many=True).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(
        detail=False, 
        methods=["POST"], 
        url_path="delete-all-children"
    )
    def delete_all_children(self, request, *args, **kwargs):
        CategoriesService().delete_all_subcategories()
        return Response(status=status.HTTP_204_NO_CONTENT)
