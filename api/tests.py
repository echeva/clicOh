from django.test import TestCase
from .models import Product
from rest_framework.test import RequestsClient, APITestCase, APIClient
from rest_framework import status
import json
from django.contrib.auth.models import User
from django.db.utils import IntegrityError


# Create your tests here.
class ProductTestCase(APITestCase):
    client = APIClient()
    user = ''
    access_token = ''

    def setUp(self):
        # Implementar autenticación basada en tokens (JWT)
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user.is_superuser = True
        self.user.save()

        response = self.client.post(
            '/api/token/', {
                'username': 'testuser',
                'password': '12345'
            },
            format='json'
        )

        result = json.loads(response.content)
        self.access_token = result['access']

        Product.objects.create(name="Coca Cola", price="245.55", stock=180)
        Product.objects.create(name="Harina 000", price="45.90", stock=100)
        Product.objects.create(name="Azúcar", price="75.00", stock=230)
        Product.objects.create(name="Yerba Playadito", price="445.50", stock=10)

    def test_product_get(self):
        # Listar todos los productos
        products = Product.objects.all()
        self.assertEqual(len(products), 4)
        response = self.client.get('/api/products/')
        self.assertEqual(len(response.data), 4)
        Product.objects.create(name="Leche", price="55", stock=100)
        response = self.client.get('/api/products/')
        self.assertEqual(len(response.data), 5)

    def test_product_get_by_id(self):
        # Consultar un producto
        response = self.client.get('/api/products/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'name': 'Coca Cola', 'price': '245.55', 'stock': 180})
        response = self.client.get('/api/products/2/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 2, 'name': 'Harina 000', 'price': '45.90', 'stock': 100})
        response = self.client.get('/api/products/7/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_product_post(self):
        # Registrar un producto
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

        response = self.client.post('/api/products/', {'name': "Leche", 'price': "55.00", 'stock': 100}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get('/api/products/5/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 5, 'name': "Leche", 'price': "55.00", 'stock': 100})

        response = self.client.post('/api/products/', {'name': "Agua"}, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_product_patch(self):
        # Editar un producto
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

        response = self.client.post('/api/products/', {'name': "Agua"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.patch('/api/products/2/', {'name': "Agua"}, format='json')
        self.assertEquals(response.data, {'id': 2, 'name': 'Agua', 'price': '45.90', 'stock': 100})

        response = self.client.patch('/api/products/2/', {'price': "50.50"}, format='json')
        self.assertEquals(response.data, {'id': 2, 'name': 'Agua', 'price': '50.50', 'stock': 100})

        response = self.client.patch('/api/products/7/', {'name': "Agua"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.patch('/api/products/2/', {'price': "-30"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        response = self.client.get('/api/products/')
        self.assertEqual(len(response.data), 4)

        # Modificar stock de un producto
        response = self.client.get('/api/products/2/')
        self.assertEqual(response.data['stock'], 100)
        response = self.client.patch('/api/products/2/', {'stock': "130"}, format='json')
        self.assertEqual(response.data, {'id': 2, 'name': 'Agua', 'price': '50.50', 'stock': 130})

        response = self.client.patch('/api/products/2/', {'stock': "-30"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_delete(self):
        # Eliminar un producto
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

        response = self.client.delete('/api/products/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get('/api/products/')
        self.assertEqual(len(response.data), 3)

        response = self.client.delete('/api/products/5/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
