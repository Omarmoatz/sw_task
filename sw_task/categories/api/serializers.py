from rest_framework import serializers

from sw_task.categories.models import Category
from sw_task.categories.service import CategoriesService


# Serializer for listing categories
class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name"
        )

# Serializer for creating a category
class CategoryCreateSerializer(serializers.Serializer):
    parent_id = serializers.UUIDField()

    def create(self, validated_data):
        # Create subcategories under the given parent
        parent_id = validated_data.get("parent_id")
        created_categories = CategoriesService().create_subcategories(parent_id)
        return created_categories
    
    def to_representation(self, instance):
        # Convert instance to a list if needed
        if isinstance(instance, list):
           return CategoryListSerializer(instance, many=True).data
        return super().to_representation(instance)
