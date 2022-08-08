from enum import auto
from statistics import mode
from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):

    date_crated = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    user_created = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_created", on_delete=models.PROTECT, null=True)
    user_modified = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_modified", null=True, on_delete=models.PROTECT)

        
    class Meta:
        abstract = True

class Product(BaseModel):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    brand = models.CharField(max_length=255)
    times_consulted = models.IntegerField(default=0)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_key = models.TextField()