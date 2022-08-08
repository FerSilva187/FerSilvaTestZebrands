import json
from random import randint
from django.test import TestCase
import requests
from django.conf import settings
from django.contrib.auth.models import User
from core.models import Profile
from testZebrands.utils import random_password

class ProductTestCase(TestCase):
    url = f"{settings.BASE_URL}/api/v1/products"

    def test_create_product(self):
        print(settings.BASE_URL)
        url = f"http://127.0.0.1:8000/api/v1/products/?api_key={12345}"
        body =  {
            "name": "TESTNAME1",
            "sku": "TESTSKU1 %s" % randint(1, 500000),
            "description": "TESTDESCRIPTION",
            "price": "99.00",
            "brand": "TESTBRAND"
        }
        headers = {'content-type': 'application/json'}

        response = requests.post(url, data=json.dumps(body), headers=headers)
        assert response.status_code == 200

    
    def test_list_product(self):
        print(settings.BASE_URL)
        url = f"http://127.0.0.1:8000/api/v1/products/get/?api_key={12345}"
        headers = {'content-type': 'application/json'}

        response = requests.get(url, headers=headers)
        assert response.status_code == 200

