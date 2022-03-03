from django.test import TestCase
from .models import Product
from rest_framework.test import RequestsClient, APITestCase, APIClient
from rest_framework import status
import json


# Create your tests here.
class ProductTestCase(APITestCase):
    client = APIClient()
    response = client.post(
        '/api/token/', {
            'username': 'admin',
            'password': 'local'
        },
        format='json'
    )

    result = json.loads(response.content)
    access_token = result['access']
    client.credentials(HTTP_AUTHORIZATION='Token ' + result['access'])

    def setUp(self):
        Product.objects.create(name="Coca Cola", price="245.55", stock=180)
        Product.objects.create(name="Harina 000", price="45.90", stock=100)
        Product.objects.create(name="Azúcar", price="75.00", stock=230)
        Product.objects.create(name="Yerba Playadito", price="445.50", stock=10)

    def test_product_get(self):
        products = Product.objects.all()
        self.assertEqual(len(products), 4)
        response = self.client.get('/api/products/')
        self.assertEqual(len(response.data), 4)
        Product.objects.create(name="Leche", price="55", stock=100)
        response = self.client.get('/api/products/')
        self.assertEqual(len(response.data), 5)

    def test_product_get_by_id(self):
        response = self.client.get('/api/products/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'name': 'Coca Cola', 'price': '245.55', 'stock': 180})
        response = self.client.get('/api/products/2/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 2, 'name': 'Harina 000', 'price': '45.90', 'stock': 100})
        response = self.client.get('/api/products/7/')
        self.assertEqual(response.status_code, 404)

    def test_product_post(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(len(response.data), 4)
        response = self.client.post('/api/products/', {'name': "Leche", 'price': "55", 'stock': 100}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)