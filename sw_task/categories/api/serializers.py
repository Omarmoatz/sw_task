from rest_framework import serializers

from sw_task.categories.models import Category


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            "id",
            "name"
        )



