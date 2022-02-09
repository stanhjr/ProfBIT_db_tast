import decimal
import random
import string
import gc
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from db_manager.models import Product
from django.conf import settings
settings.DEBUG = True


def queryset_generator(queryset, chunksize=1000):
    '''''
    Iterate over a Django Queryset ordered by the primary key

    This method loads a maximum of chunksize (default: 1000) rows in it's
    memory at the same time while django normally would load all rows in it's
    memory. Using the iterator() method only causes it to not preload all the
    classes.
    '''
    pk = 0
    last_pk = queryset.order_by('-pk')[0].pk
    queryset = queryset.order_by('pk')
    while pk < last_pk:
        for row in queryset.filter(pk__gt=pk)[:chunksize]:
            pk = row.pk
            yield row
        gc.collect()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        product_choices = ('in_stock', 'out_of_stock')
        with transaction.atomic():
            product_queryset = queryset_generator(Product.objects.all())
            for product in product_queryset:
                product.price = decimal.Decimal(random.randrange(155, 389)) / 100
                product.status = random.choice(product_choices)
                product.remains = random.randint(0, 100)
                product.save()


