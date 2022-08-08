from rest_framework import serializers
from core.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "sku",
            "description",
            "price",
            "brand",
            "id",
            "times_consulted"
        ]


        read_only_fields =  (
            "id",
            "times_consulted",
        )

