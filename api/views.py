from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProductSerializer, OrderSerializer
from .models import OrderDetail
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = ProductSerializer.Meta.model.objects.all()

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = OrderSerializer.Meta.model.objects.all()

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            instance = self.get_object()
            order_details = OrderDetail.objects.filter(order=pk)
            for detail in order_details:
                detail.product.restore_stock(detail.quantity)
                detail.product.save()
            self.perform_destroy(instance)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
