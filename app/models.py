# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime


# Create your models here.
class Product(models.Model):
    name = models.CharField(_("Nombre"), max_length=100)
    price = models.DecimalField(_("Precio"), max_digits=7, decimal_places=2)
    stock = models.PositiveBigIntegerField(_("Unidades disponibles"), default=0)

    class Meta:
        verbose_name = _("Producto")
        verbose_name_plural = _("Productos")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u"%s" % self.name


class Order(models.Model):
    date_time = models.DateTimeField(_("Fecha"))

    class Meta:
        verbose_name = _("Orden")
        verbose_name_plural = _("Ordenes")

    def __str__(self):
        return self.pk

    def __unicode__(self):
        return u"%s" % self.pk


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name="details", verbose_name="Orden", on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(_("Cantidad"), default=0)
    product = models.ForeignKey(Product, verbose_name="Producto", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Detalle de una orden")
        verbose_name_plural = _("Detalles de una orden")

    def __str__(self):
        return self.pk

    def __unicode__(self):
        return u"%s" % self.pk
