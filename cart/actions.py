'''
	This document contains the actions that could be performed on the database.
'''

from . import messages
from . import models
from django.db.models import F, When, Case

def create_product(title, price, inventory_count):
	'''
	Creates a new product

	:param str title: the title of the product
	:param float title: the price of the product
	:param int title: the number of available product inventory

	:return dict: a dict containing information about the status of the operation and the newly created product.

	'''

	product = models.Product.objects.create(
		title=title,
		price=price,
		inventory_count=inventory_count
	)
	response = messages.product_created()
	response.update(dict(product=product))
	return response

def delete_product(id):
	'''
	Deletes a product

	:param int id: the id of the product that you wish to delete

	:return dict: a dict containing information about the status of the operation

	'''

	try:
		product = models.Product.objects.get(id=id)
		product.delete()
	except models.Product.DoesNotExist:
		return messages.product_not_found()
	return messages.product_deleted()

def create_cart():
	'''
	Creates a new cart

	:return dict: a dict containing information about the status of the operation and the newly created cart.
	'''

	cart = models.Cart.objects.create()
	response = messages.cart_created()
	response.update(dict(cart=cart))
	return response

def delete_cart(id):
	'''
	Deletes a cart

	:param int id: the id of the cart that you wish to delete

	:return dict: a dict indicating the status of this operation

	'''

	try:
		cart = models.Cart.objects.get(id=id)
		cart.delete()
	except models.Cart.DoesNotExist:
		return messages.cart_not_found()
	return messages.cart_deleted()

def add_product_to_cart(product_id, cart_id):
	'''
	adds a product to the cart

	:param int cart_id: the id of the cart that you wish to add a product to.
	:param int product_id: the id of the product that you wish to add to the cart.

	:return dict: a dictionary that informs you about the status of the operation
	'''

	try:
		cart = models.Cart.objects.get(id=cart_id)
	except models.Cart.DoesNotExist:
		return messages.cart_not_found()
	try:
		product = models.Product.objects.get(id=product_id)
	except models.Product.DoesNotExist:
		return messages.product_not_found()

	models.CartProductMap.objects.create(product=product, cart=cart)

	return messages.product_added_to_cart()	

def remove_product_from_cart(product_id, cart_id):
	'''
	removes a product to the cart

	:param int cart_id: the id of the cart that you wish to remove a product from.
	:param int product_id: the id of the product that you wish to remove from the cart.

	:return dict: a dictionary that informs you about the status of the operation
	'''

	try:
		cart = models.Cart.objects.get(id=cart_id)
	except models.Cart.DoesNotExist:
		return messages.cart_not_found()
	try:
		product = models.Product.objects.get(id=product_id)
	except models.Product.DoesNotExist:
		return messages.product_not_found()
	models.CartProductMap.objects.filter(cart=cart, product=product).delete()

	return messages.product_removed_from_cart()

def purchase_cart(cart_id):
	'''
	purchase the cart

	:param int cart_id: the id of the cart that you wish to purchase

	:return dict: a dictionary that informs you about the status of the operation
	'''
	try:
		cart = models.Cart.objects.get(id=cart_id)
	except models.Cart.DoesNotExist:
		return messages.cart_not_found()

	all_cart_product_maps = models.CartProductMap.objects.filter(cart=cart)
	for product_key_map in all_cart_product_maps:
		product = product_key_map.product
		product.inventory_count = (
			Case(
				When(
					inventory_count__gt=0,
					then= F('inventory_count') - 1
				),
		    	default=F('inventory_count')
		    )
		)
		product.save()

	cart.purchased = True
	cart.save()

	return messages.cart_successfully_purchased()




























































