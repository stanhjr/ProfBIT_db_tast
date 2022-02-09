import time
from django.views import View
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from db_manager.models import Category, Product


class CategoryView(View):
    http_method_names = ['get', ]

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        time.sleep(2)
        product = Product.objects.filter(category_id=pk).all()
        if not product:
            return redirect('category-url', pk='1')

        category_name = Category.objects.get(id=pk).name
        paginator = Paginator(product, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'index.html', {'page_obj': page_obj, 'category_name': category_name})

