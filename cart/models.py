'''
This file contains the database models for this app
'''

from django.db import models

class Product(models.Model):
	title = models.CharField(default=None,max_length=100)
	price = models.FloatField(default=0)
	inventory_count = models.IntegerField(default=0)

class Cart(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	purchased = models.BooleanField(default=False)

class CartProductMap(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)