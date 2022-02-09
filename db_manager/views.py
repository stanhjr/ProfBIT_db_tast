import time

from django.template import RequestContext
from django.views import View
from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.cache import cache
from django.db import connection
from django.core.cache.utils import make_template_fragment_key
from db_manager.models import Product, Category


class MyView(View):
    http_method_names = ['get', ]

    def get(self, request, *args, **kwargs):
        cat = make_template_fragment_key('cat')
        # prod = make_template_fragment_key('prod', [username])
        print(cache.get('prod'))


        # print(prod)
        # cache.delete(key)  # invalidates cached template fragment
        print(request.GET.get('foot '))
        print(request.GET)
        print(args)
        print(kwargs)
        time.sleep(2)
        category = Category.objects.all()
        paginator = Paginator(category, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'index.html', {'page_obj': page_obj})

