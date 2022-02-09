from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.cache import cache
from django.forms.models import model_to_dict


class ModelDiffMixin(object):
    """
    A model mixin that tracks model fields' values and provide some useful api
    to know what fields have been changed.
    """

    def __init__(self, *args, **kwargs):
        super(ModelDiffMixin, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        if self.has_changed:
            print(f"Product {self.id} changed")
            for field in self.changed_fields:
                print(field, self.diff.get(field))
        super(ModelDiffMixin, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])


class MyUser(AbstractUser):
    ...


class Category(models.Model):
    name = models.CharField(unique=True, max_length=120)


class Product(ModelDiffMixin, models.Model):
    name = models.CharField(unique=True, max_length=120)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    status = models.CharField(choices=[('in_stock', 'In stock'), ('out_of_stock', 'Out of stock')], max_length=30)
    remains = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        cache.clear()
        super(Product, self).save(*args, **kwargs)
