from django.test import TestCase
from .models import Product, Order, OrderDetail
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from django.db import transaction

# Create your tests here.
# class ProductTestCase(APITestCase):
#     client = APIClient()
#     user = ''
#     access_token = ''
#
#     def setUp(self):
#         # Implementar autenticación basada en tokens (JWT)
#         self.user = User.objects.create_user(username='testuser', password='12345')
#         self.user.is_superuser = True
#         self.user.save()
#
#         response = self.client.post(
#             '/api/token/', {
#                 'username': 'testuser',
#                 'password': '12345'
#             },
#             format='json'
#         )
#
#         result = json.loads(response.content)
#         self.access_token = result['access']
#
#         Product.objects.create(name="Coca Cola", price="245.55", stock=180)
#         Product.objects.create(name="Harina 000", price="45.90", stock=100)
#         Product.objects.create(name="Azúcar", price="75.00", stock=230)
#         Product.objects.create(name="Yerba Playadito", price="445.50", stock=10)
#
#     def test_product_get(self):
#         # Listar todos los productos
#         products = Product.objects.all()
#         self.assertEqual(len(products), 4)
#         response = self.client.get('/api/products/')
#         self.assertEqual(len(response.data), 4)
#         Product.objects.create(name="Leche", price="55", stock=100)
#         response = self.client.get('/api/products/')
#         self.assertEqual(len(response.data), 5)
#
#     def test_product_get_by_id(self):
#         # Consultar un producto
#         response = self.client.get('/api/products/1/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, {'id': 1, 'name': 'Coca Cola', 'price': '245.55', 'stock': 180})
#         response = self.client.get('/api/products/2/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, {'id': 2, 'name': 'Harina 000', 'price': '45.90', 'stock': 100})
#         response = self.client.get('/api/products/7/')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#     def test_product_post(self):
#         # Registrar un producto
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
#         response = self.client.get('/api/products/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 4)
#
#         response = self.client.post('/api/products/', {'name': "Leche", 'price': "55.00", 'stock': 100}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         response = self.client.get('/api/products/5/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, {'id': 5, 'name': "Leche", 'price': "55.00", 'stock': 100})
#
#         response = self.client.post('/api/products/', {'name': "Agua"}, format='json')
#         self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_product_patch(self):
#         # Editar un producto
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
#         response = self.client.get('/api/products/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 4)
#
#         response = self.client.post('/api/products/', {'name': "Agua"}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#         response = self.client.patch('/api/products/2/', {'name': "Agua"}, format='json')
#         self.assertEquals(response.data, {'id': 2, 'name': 'Agua', 'price': '45.90', 'stock': 100})
#
#         response = self.client.patch('/api/products/2/', {'price': "50.50"}, format='json')
#         self.assertEquals(response.data, {'id': 2, 'name': 'Agua', 'price': '50.50', 'stock': 100})
#
#         response = self.client.patch('/api/products/7/', {'name': "Agua"}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#         response = self.client.patch('/api/products/2/', {'price': "-30"}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#         response = self.client.get('/api/products/')
#         self.assertEqual(len(response.data), 4)
#
#         # Modificar stock de un producto
#         response = self.client.get('/api/products/2/')
#         self.assertEqual(response.data['stock'], 100)
#         response = self.client.patch('/api/products/2/', {'stock': "130"}, format='json')
#         self.assertEqual(response.data, {'id': 2, 'name': 'Agua', 'price': '50.50', 'stock': 130})
#
#         response = self.client.patch('/api/products/2/', {'stock': "-30"}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_product_delete(self):
#         # Eliminar un producto
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
#         response = self.client.get('/api/products/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 4)
#
#         response = self.client.delete('/api/products/1/', format='json')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#
#         response = self.client.get('/api/products/')
#         self.assertEqual(len(response.data), 3)
#
#         response = self.client.delete('/api/products/5/', format='json')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class OrderTestCase(APITestCase):
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

        product_1 = Product.objects.create(name="Coca Cola", price="245.55", stock=180)
        product_2 = Product.objects.create(name="Harina 000", price="45.90", stock=100)
        product_3 = Product.objects.create(name="Azúcar", price="75.00", stock=230)
        product_4 = Product.objects.create(name="Yerba Playadito", price="445.50", stock=10)

        order_1 = Order.objects.create(date_time=timezone.now())
        OrderDetail.objects.create(product=product_1, quantity=5, order=order_1)
        OrderDetail.objects.create(product=product_4, quantity=4, order=order_1)

        order_2 = Order.objects.create(date_time=timezone.now())
        OrderDetail.objects.create(product=product_2, quantity=50, order=order_2)
        OrderDetail.objects.create(product=product_3, quantity=40, order=order_2)

        order_3 = Order.objects.create(date_time=timezone.now())
        OrderDetail.objects.create(product=product_2, quantity=15, order=order_3)
        OrderDetail.objects.create(product=product_3, quantity=20, order=order_3)
        OrderDetail.objects.create(product=product_1, quantity=20, order=order_3)
        OrderDetail.objects.create(product=product_4, quantity=2, order=order_3)

        order_4 = Order.objects.create(date_time=timezone.now())
        OrderDetail.objects.create(product=product_2, quantity=5, order=order_4)

    # def test_order_get(self):
    #     # Listar todas las ordenes
    #     orders = Order.objects.all()
    #     self.assertEqual(len(orders), 4)
    #     response = self.client.get('/api/orders/')
    #     self.assertEqual(len(response.data), 4)
    #     product = Product.objects.create(name="Aceite", price="90.0", stock=270)
    #     order = Order.objects.create(date_time=timezone.now())
    #     order_detail = OrderDetail.objects.create(product=product, quantity=15, order=order)
    #     response = self.client.get('/api/products/')
    #     self.assertEqual(len(response.data), 5)
    #
    # def test_order_get_by_id(self):
    #     # Consultar una orden y sus detalles
    #     response = self.client.get('/api/orders/1/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['id'], 1)
    #     self.assertEqual(len(response.data['details']), 2)
    #
    #     response = self.client.get('/api/orders/2/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['id'], 2)
    #     self.assertEqual(response.data['details'][0], {'id': 3, 'quantity': 50, 'product': 2})
    #     self.assertEqual(response.data['details'][1], {'id': 4, 'quantity': 40, 'product': 3})
    #
    #     response = self.client.get('/api/orders/7/')
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #
    # def test_order_post(self):
    #     # Registrar una orden (inclusive sus detalles). Debe actualizar el stock del producto
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
    #     response = self.client.get('/api/orders/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 4)
    #
    #     product_stock_1 = Product.objects.get(pk=1).stock
    #     product_stock_2 = Product.objects.get(pk=2).stock
    #
    #     response = self.client.post('/api/orders/',
    #                                 {"date_time": "2022-03-09T06:05:00Z",
    #                                  "details": [
    #                                      {"product": 1, "quantity": 4},
    #                                      {"product": 2, "quantity": 40}
    #                                  ]
    #                                  }
    #                                 , format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     response = self.client.get('/api/orders/5/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['id'], 5)
    #     self.assertEqual(response.data['date_time'], "2022-03-09T06:05:00Z")
    #     self.assertEqual(len(response.data['details']), 2)
    #
    #     # Debe actualizar el stock del producto
    #     product_1 = Product.objects.get(pk=1)
    #     product_2 = Product.objects.get(pk=2)
    #     self.assertEqual(product_stock_1 - 4, product_1.stock)
    #     self.assertEqual(product_stock_2 - 40, product_2.stock)
    #
    # def test_order_post_failed(self):
    #     """ A la hora de crear una orden se debe validar:
    #         que la cantidad de cada producto sea mayor a 0
    #         que no se repitan productos en el mismo pedido"""
    #
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
    #     response = self.client.post('/api/orders/', {'date_time': ''}, format='json')
    #     self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    #     product_stock_1 = Product.objects.get(pk=1).stock
    #
    #     response = self.client.post('/api/orders/',
    #                                 {"date_time": "2022-03-09T06:05:00Z",
    #                                  "details": [
    #                                      {"product": 1, "quantity": 40},
    #                                      {"product": 1, "quantity": 40}
    #                                  ]}
    #                                 , format='json')
    #
    #     self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEquals(product_stock_1, Product.objects.get(pk=1).stock)
    #
    #     product_stock_1 = Product.objects.get(pk=1).stock
    #     product_stock_2 = Product.objects.get(pk=2).stock
    #
    #     response = self.client.post('/api/orders/',
    #                                 {"date_time": "2022-03-09T06:05:00Z",
    #                                  "details": [
    #                                      {"product": 1, "quantity": 40},
    #                                      {"product": 2, "quantity": 4000}
    #                                  ]}
    #                                 , format='json')
    #     self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEquals(product_stock_1, Product.objects.get(pk=1).stock)
    #     self.assertEquals(product_stock_2, Product.objects.get(pk=2).stock)

    def test_order_patch(self):
        # Editar una orden (inclusive sus detalles). Debe actualizar el stock del producto
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        # response = self.client.get('/api/orders/')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 4)
        #
        # response = self.client.post('/api/orders/', {"date_time": "2022-03-09T06:05:00Z"}, format='json')
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        #
        # response = self.client.patch('/api/orders/2/', {'date_time': "2021-02-09T06:05:00Z"}, format='json')
        # self.assertEquals(response.data["date_time"], "2021-02-09T06:05:00Z")

        response = self.client.patch('/api/orders/2/', {"date_time": "2022-03-09T06:05:00Z",
                                     "details": [
                                         {"product": 1, "quantity": 7},
                                         {"product": 2, "quantity": 7}
                                     ]
                                     }, format='json')
        # self.assertEquals(response.data, {'id': 2, 'name': 'Agua', 'price': '50.50', 'stock': 100})
        #
        # response = self.client.patch('/api/products/7/', {'name': "Agua"}, format='json')
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        #
        # response = self.client.patch('/api/products/2/', {'price': "-30"}, format='json')
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        #
        # response = self.client.get('/api/products/')
        # self.assertEqual(len(response.data), 4)
        #
        # # Modificar stock de un producto
        # response = self.client.get('/api/products/2/')
        # self.assertEqual(response.data['stock'], 100)
        # response = self.client.patch('/api/products/2/', {'stock': "130"}, format='json')
        # self.assertEqual(response.data, {'id': 2, 'name': 'Agua', 'price': '50.50', 'stock': 130})
        #
        # response = self.client.patch('/api/products/2/', {'stock': "-30"}, format='json')
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_delete(self):
        # Eliminar una orden. Restaura stock del producto
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

        order_details = OrderDetail.objects.filter(order=1)
        details = [(detail.product, detail.quantity) for detail in order_details]

        response = self.client.delete('/api/orders/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Restaura stock del producto
        for product_aux, quantity in details:
            product = Product.objects.get(pk=product_aux.id)
            self.assertEqual(product.stock, product_aux.stock + quantity)

        # Elimina los detalles
        order_details = OrderDetail.objects.filter(order=1)
        self.assertEqual(len(order_details), 0)

        response = self.client.get('/api/orders/')
        self.assertEqual(len(response.data), 3)

        response = self.client.delete('/api/orders/800/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
