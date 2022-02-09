import decimal
import random
import string
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from db_manager.models import Category, Product
from django.conf import settings
from django.db import connection
settings.DEBUG = True


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('category_count', type=int, help=u'Количество категорий')
        parser.add_argument('product_count', type=int, help=u'Количество продукта в категории')
    with transaction.atomic():
        def handle(self, *args, **kwargs):
            product_choices = ('in_stock', 'out_of_stock')
            category_count = kwargs['category_count']
            product_count = kwargs['product_count']
            insert_list = []
            for i in range(category_count):
                name = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
                insert_list.append(Category(name=name))
            Category.objects.bulk_create(insert_list)
            insert_list_product = []
            for category_model in insert_list:
                for i in range(product_count):
                    name = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
                    category = category_model
                    price = decimal.Decimal(random.randrange(155, 389))/100
                    status = random.choice(product_choices)
                    remains = random.randint(0, 100)
                    insert_list_product.append(Product(name=name, category=category, price=price, status=status, remains=remains))
            Product.objects.bulk_create(insert_list_product)
