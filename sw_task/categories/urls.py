from django.urls import path

from sw_task.categories.views import CategoryView
from sw_task.categories.views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("categories/", CategoryView.as_view(), name="categories"),
]