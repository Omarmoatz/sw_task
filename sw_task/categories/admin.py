from django.contrib import admin

from sw_task.categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent"]
    search_fields = ["name"]
    raw_id_fields = ["parent"]
