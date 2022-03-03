from .models import Product, Order, OrderDetail
from rest_framework import serializers
from django.utils import timezone
from django.db import IntegrityError
from django.db import transaction


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']
        extra_kwargs = {'id': {'read_only': False}, 'name': {'read_only': True}, 'price': {'read_only': True}}


class OrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderDetail
        fields = ['id', 'quantity', 'product']


class OrderSerializer(serializers.ModelSerializer):
    details = OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'date_time', 'details', 'get_total', 'get_total_usd']

    def validate_details(self, details):
        if len(details) == 0:
            raise serializers.ValidationError("La orden debe contener al menos un producto.")
        products_set = set(detail['product']for detail in details)
        if len(products_set) != len(details):
            raise serializers.ValidationError("La orden tiene productos repetidos.")
        return details

    @transaction.atomic
    def create(self, validated_data):
        errors = []
        order_details = validated_data.pop('details')
        if self.validate_details(order_details):
            order = Order.objects.create(**validated_data)
            for detail in order_details:
                try:
                    product = Product.objects.get(pk=detail['product'].id)
                    product.decrease_stock(detail['quantity'])
                    product.save()
                    OrderDetail.objects.create(order=order, quantity=detail['quantity'],
                                               product=detail['product'])
                except Product.DoesNotExist:
                    errors.append({'error': f"El producto con id {detail['product']} no existe."})
                except IntegrityError:
                    errors.append({'error': f'El producto "{product.name}" no posee sufiente stock.'})

            if not errors:
                order.save()
            else:
                transaction.set_rollback(True)
                raise serializers.ValidationError(errors)
            return order
