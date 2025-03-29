from django.urls import path
from rest_framework.routers import DefaultRouter


from sw_task.categories.api.views import CategoryViewSet

from sw_task.categories.views import CategoryView
from sw_task.categories.views import HomeView


router = DefaultRouter()
router.register("v2/categories", CategoryViewSet, basename="categories-v2")

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("categories/", CategoryView.as_view(), name="categories"),
    *router.urls
]
