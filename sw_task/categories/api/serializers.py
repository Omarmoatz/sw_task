from rest_framework import serializers

from sw_task.categories.models import Category
from sw_task.categories.service import CategoriesService


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name"
        )



class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name"
        )

    def create(self, validated_data):
        parent_id = validated_data.get("parent_id")
        created_categories = CategoriesService().create_subcategories(parent_id)
        return created_categories