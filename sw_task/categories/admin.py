from sw_task.categories.models import Category
from django.contrib import admin


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent"]
    search_fields = ["name"]
    raw_id_fields = ["parent"]
    
