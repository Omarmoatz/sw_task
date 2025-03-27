from django.shortcuts import render
from django.views import View
from sw_task.categories.service import CategoriesService

class HomeView(View):
    def get(self, request):
        """
        Render the page with top-level categories.
        create initial ones if none exist
        """
        CategoriesService().create_initial_categories()
        categories = CategoriesService().get_categories()
        return render(request, "pages/home.html", {"categories": categories})


