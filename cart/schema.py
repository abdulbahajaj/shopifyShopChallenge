'''
	This document contains the GraphQL schema for this app
'''
import graphene
from graphene_django.types import DjangoObjectType
from . import models
from graphene_django.filter.fields import DjangoFilterConnectionField
from . import actions
from django.db.models import Sum

class CartNode(graphene.Node):
	class Meta:
		name = "Node"

	@staticmethod
	def to_global_id(type, id):
		'''
			converts local ids to global ids
			:param str type: the type of the object (e.g. CartType)
			:param str id: the local id of the object
			
			:param str type: the type of the object (e.g. CartType)

		'''

		return '{}_{}'.format(type, id)

	@staticmethod
	def to_local_id(global_id):
		'''
			converts global ids to local ids
			
			:param str global_id: the global id that you wish to convert to a local id

			:returns tuple(type, id): The type and local id of the global id

		'''
		type, id = global_id.split('_')
		id = int(id)
		return type, id

	@classmethod
	def get_node_from_global_id(cls,info, global_id, only_type=None):
		'''
			A hook that is used by graphene to automatically retrieve objects from their
			global id

		'''
		type, id = cls.to_local_id(global_id=global_id)
		if only_type:
			assert type == only_type._meta.name, 'Received not compatible node.'
		if type == 'CartType':
			return models.Cart.objects.get(id=id)
		if type == 'ProductType':
			return models.Product.objects.get(id=id)

class CartProductMapType(DjangoObjectType):
	class Meta:
		model = models.CartProductMap
		interfaces = (CartNode,)

''' Existing node types '''
class ProductType(DjangoObjectType):
	class Meta:
		model = models.Product
		filter_fields = dict(
			inventory_count=['exact'],
			title=['exact']
		)
		interfaces = (CartNode,)

class CartType(DjangoObjectType):
	class Meta:
		model = models.Cart
		filter_fields = dict()
		interfaces = (CartNode,)
	products = graphene.List(ProductType)
	total_dollar_amount = graphene.Int()

	def resolve_total_dollar_amount(self, args, **kwargs):
		result = models.CartProductMap.objects.filter(cart=self.id).aggregate(Sum('product__price'))
		result = result.get('product__price__sum')
		return result if result is not None else 0
	def resolve_products(self, args, **kwargs):
		return [
			cart_product_map.product 
			for cart_product_map in models.CartProductMap.objects.filter(cart=self.id)
		]

''' Query '''
class Query(graphene.AbstractType):
	''' The query schema for this app'''

	all_products = graphene.List(ProductType, available_only=graphene.Boolean())
	all_carts = DjangoFilterConnectionField(CartType)
	cart = CartNode.Field(CartType)

	def resolve_all_products(self, args, available_only = False, **kwargs):
		if available_only is True:
			return models.Product.objects.filter(inventory_count__gt=0)
		return models.Product.objects.all()

	def resolve_all_carts(self, args, **kwargs):
		return models.Cart.objects.all()

''' The mutations that are available for this app '''

class CreateCart(graphene.Mutation):
	class Input: pass

	status = graphene.String()
	description = graphene.String()
	cart = graphene.Field(lambda: CartType)

	@staticmethod
	def mutate(root, args,**kwargs):
		response = actions.create_cart()
		return CreateCart(**response)

class DeleteCart(graphene.Mutation):
	class Input:
		id = graphene.String()
	status = graphene.String()
	description = graphene.String()

	@staticmethod
	def mutate(root, args,**kwargs):
		global_id = kwargs.get('id')
		type, id = CartNode.to_local_id(global_id=global_id)
		response = actions.delete_cart(id=id)
		return CreateProduct(**response)

class PurchaseCart(graphene.Mutation):
	class Input:
		id = graphene.String()
	status = graphene.String()
	description = graphene.String()

	@staticmethod
	def mutate(root, args,**kwargs):
		global_id = kwargs.get('id')
		type, id = CartNode.to_local_id(global_id=global_id)
		response = actions.purchase_cart(cart_id=id)
		return CreateProduct(**response)

class CreateProduct(graphene.Mutation):
	class Input:
		title = graphene.String()
		price = graphene.Float()
		inventory_count = graphene.Int()
	status = graphene.String()
	description = graphene.String()
	product = graphene.Field(lambda: ProductType)

	@staticmethod
	def mutate(root, args,**kwargs):
		response = actions.create_product(
			title=kwargs.get('title'), 
			price=kwargs.get('price'), 
			inventory_count=kwargs.get('inventory_count'))
		print(response)
		return CreateProduct(**response)

class DeleteProduct(graphene.Mutation):
	class Input:
		id = graphene.String()
	status = graphene.String()
	description = graphene.String()

	@staticmethod
	def mutate(root, args,**kwargs):
		global_id = kwargs.get('id')
		type, id = CartNode.to_local_id(global_id=global_id)
		response = actions.delete_product(id=id)
		return CreateProduct(**response)

class AddProductToCart(graphene.Mutation):
	class Input:
		product_id = graphene.String()
		cart_id = graphene.String()

	status = graphene.String()
	description = graphene.String()

	@staticmethod
	def mutate(root, args,**kwargs):
		global_product_id = kwargs.get('product_id')
		type, product_id = CartNode.to_local_id(global_id=global_product_id)

		global_cart_id = kwargs.get('cart_id')
		type, cart_id = CartNode.to_local_id(global_id=global_cart_id)

		response = actions.add_product_to_cart(
			product_id=product_id,
			cart_id=cart_id
		)

		return AddProductToCart(**response)

class RemoveProductFromCart(graphene.Mutation):
	class Input:
		product_id = graphene.String()
		cart_id = graphene.String()
	status = graphene.String()
	description = graphene.String()
	@staticmethod
	def mutate(root, args,**kwargs):
		global_product_id = kwargs.get('product_id')
		type, product_id = CartNode.to_local_id(global_id=global_product_id)

		global_cart_id = kwargs.get('cart_id')
		type, cart_id = CartNode.to_local_id(global_id=global_cart_id)

		response = actions.remove_product_from_cart(
			product_id=product_id,
			cart_id=cart_id
		)
		return AddProductToCart(**response)

class Mutation(graphene.AbstractType):
	'''
		describes the mutation schema for this app
	'''
	create_product = CreateProduct.Field()
	delete_product = DeleteProduct.Field()
	create_cart = CreateCart.Field()
	delete_cart = DeleteCart.Field()
	add_product_to_cart = AddProductToCart.Field()
	remove_product_from_cart = RemoveProductFromCart.Field()
	purchase_cart = PurchaseCart.Field()




























































