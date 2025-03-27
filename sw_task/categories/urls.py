from django.urls import path

from sw_task.categories.views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]