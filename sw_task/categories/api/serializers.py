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



class CategoryCreateSerializer(serializers.Serializer):
    parent_id = serializers.UUIDField()

    def create(self, validated_data):
        print("="*100)
        parent_id = validated_data.get("parent_id")
        created_categories = CategoriesService().create_subcategories(parent_id)
        print("="*100)

        print("created_categories", created_categories)
        return created_categories
    
    def to_representation(self, instance):
        print("instance", instance)
        print("is-instance list", isinstance(instance, list))

        if isinstance(instance, list):
           return CategoryListSerializer(instance, many=True).data
        return super().to_representation(instance)