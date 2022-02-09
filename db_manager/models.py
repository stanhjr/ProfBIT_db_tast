from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    ...


class Category(models.Model):
    name = models.CharField(unique=True, max_length=120)


class Product(models.Model):
    name = models.CharField(unique=True, max_length=120)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    status = models.CharField(choices=[('in_stock', 'In stock'), ('out_of_stock', 'Out of stock')], max_length=30)
    remains = models.PositiveIntegerField()
