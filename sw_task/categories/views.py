from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest
import json

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



class CategoryView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        """Fetch categories"""
        parent_id = request.GET.get('parent_id')
        categories = (
            CategoriesService().get_subcategories(parent_id, ())
            if parent_id
            else CategoriesService().get_categories()
        )
        data = [{'id': ctg.id, 'name': ctg.name} for ctg in categories]
        return JsonResponse({'categories': data})

    @csrf_exempt
    def post(self, request: HttpRequest, *args, **kwargs):
        """Automatically create subcategories with names based on parent"""
        try:
            print("/*"*100)
            data = json.loads(request.body)
            parent_id = data.get("parent_id")

            print(parent_id)

            created_categories = CategoriesService().create_subcategories(parent_id)
            print(created_categories)

            response = [{'id': ctg.id, 'name': ctg.name} for ctg in created_categories]
            return JsonResponse({'categories': response}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
