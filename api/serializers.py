from .models import Product, Order, OrderDetail
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class OrderDetailsSerializer(serializers.ModelSerializer):
    product = ProductReadOnlySerializer(read_only=True)

    class Meta:
        model = OrderDetail
        fields = ['id', 'quantity', 'product']


class OrderSerializer(serializers.ModelSerializer):
    details = OrderDetailsSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'date_time', 'details', 'get_total', 'get_total_usd']

    def validate(self, data):
        details = data.pop('details')
        if len(details) == 0:
            raise serializers.ValidationError("La orden debe contener al menos un producto.")
        
        return data