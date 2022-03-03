# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime
import requests
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import transaction


# Create your models here.
class Product(models.Model):
    name = models.CharField(_("Nombre"), max_length=100)
    price = models.DecimalField(_("Precio"), max_digits=7, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.PositiveBigIntegerField(_("Unidades disponibles"), default=0, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = _("Producto")
        verbose_name_plural = _("Productos")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u"%s" % self.name

    def can_decrease_stock(self, quantity):
        return self.stock - quantity >= 0

    def decrease_stock(self, quantity):
        self.stock -= quantity

    def restore_stock(self, quantity):
        self.stock += quantity


class Order(models.Model):
    date_time = models.DateTimeField(_("Fecha"))

    @property
    def get_total(self):
        details = OrderDetail.objects.filter(order=self)
        return sum([detail.total_price for detail in details])

    @property
    def get_total_usd(self):
        response = requests.get("https://www.dolarsi.com/api/api.php?type=valoresprincipales")
        if response.status_code == 200:
            json = response.json()
            for item in json:
                if item['casa']['nombre'] == "Dolar Blue":
                    return self.get_total * Decimal(item['casa']['compra'].replace(',', '.'))
                
        return 0

    class Meta:
        verbose_name = _("Orden")
        verbose_name_plural = _("Ordenes")

    def __str__(self):
        return self.pk

    def __unicode__(self):
        return u"%s" % self.pk


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name="details", verbose_name="Orden", on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(_("Cantidad"), default=0, validators=[MinValueValidator(1)])
    product = models.ForeignKey(Product, verbose_name="Producto", on_delete=models.CASCADE)
    
    @property
    def total_price(self):
        return self.product.price * self.quantity
    
    class Meta:
        verbose_name = _("Detalle de una orden")
        verbose_name_plural = _("Detalles de una orden")

    def __str__(self):
        return self.pk

    def __unicode__(self):
        return u"%s" % self.pk

