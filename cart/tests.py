# Create your tests here.
from django.test import TestCase
from . import actions
from . import models
from django.test.client import RequestFactory
from django.test import Client
import json

def send_graphQL_query(test,query):
	'''
	sends a graphql query to the graphql endpont and returns a response

	:param TestCase test: a TestCase object from the test
	:param str query: a graphQL query
	
	:return dict: the graphQL response from the query
	'''

	response = Client().post('/graphql',SERVER_PORT=8080,data=dict(query=query))
	test.assertEqual(response.status_code,200)
	return json.loads(response.content).get('data')

class ProductTestCase(TestCase):
	'''
		test functionalities that are related to prducts using internal functions
	'''

	def setUp(self):
		'''
			creates 3 products
		'''

		actions.create_product(
			title="testProduct1",
			price=100.4, 
			inventory_count=100000)
		actions.create_product(
			title="testProduct2",
			price=0.5, 
			inventory_count=99191919)
		actions.create_product(
			title="testProduct3",
			price=99999999, 
			inventory_count=0)

	def test_product_creation(self):
		'''
			Tests product creation functionalities
			- Retrieves the products from the database
			- Makes sure that the created products have the correct values
		'''

		product1 = models.Product.objects.get(title="testProduct1")
		product2 = models.Product.objects.get(title="testProduct2")
		product3 = models.Product.objects.get(title="testProduct3")

		self.assertEqual(product1.price, 100.4)
		self.assertEqual(product2.price, 0.5)
		self.assertEqual(product3.price, 99999999)

		self.assertEqual(product1.inventory_count, 100000)
		self.assertEqual(product2.inventory_count, 99191919)
		self.assertEqual(product3.inventory_count, 0)

	def test_product_deletion(self):
		'''
			Tests product deletion
			- Deletes a product
			- Retrieves products from the database to make sure that the product is deleted
			- Makes sure that there are only two products in the databse
			- Makes sure that the correct product was deleted by checking the values of the remaining products
		'''

		product1 = models.Product.objects.get(title="testProduct1")
		product2 = models.Product.objects.get(title="testProduct2")
		product3 = models.Product.objects.get(title="testProduct3")

		actions.delete_product(id=product3.id)
		all_products = models.Product.objects.all()
		self.assertEqual(len(all_products), 2)
		for product in all_products:
			self.assertIn(product.title , ['testProduct1','testProduct2'])
			self.assertIn(product.id , [1,2])
			self.assertIn(product.price , [100.4,0.5])
			self.assertIn(product.inventory_count, [100000,99191919])

class ProductGraphQLTestCase(TestCase):
	'''
		test functionalities that are related to prducts using GraphQL
	'''

	def setUp(self):
		'''
			creates 3 products
			- One of the products have no inventory
		'''

		actions.create_product(
			title="testProduct1",
			price=100.4, 
			inventory_count=100000)
		actions.create_product(
			title="testProduct2",
			price=0.5, 
			inventory_count=99191919)
		actions.create_product(
			title="testProduct3",
			price=99999999, 
			inventory_count=0)

	def test_product_creation(self):
		'''
			Tests product creation with GraphQL
			- Sends a graphQL mutation for product creation to the graphQL endpoint
			- Makes sure that the response has the correct status
			- Makes sure that the response returned a product object
			- Makes sure that the product object has the correct values
			- Retrieves product directly from the database to make sure that the product was actually created
			- Verifies that there are now 4 products in the database
			- Makes sure that the database stored the correct values
		'''


		query = '''
			mutation{
				createProduct(
					title: "title"
					inventoryCount: 10
					price: 10
				){
					status
					description
					product{
						id
						title
						price
						inventoryCount
					}
				}
			}
		'''
		response = send_graphQL_query(test=self, query=query).get('createProduct',None)
		self.assertNotEqual(response, None)
		self.assertNotEqual(response.get('status'), None)
		product = response.get('product',None)
		self.assertNotEqual(product, None)
		self.assertEqual(product.get('id'),'ProductType_4')
		self.assertEqual(product.get('title'),'title')
		self.assertEqual(product.get('price'),10.0)
		self.assertEqual(product.get('inventoryCount'),10)

		all_products = models.Product.objects.all()
		self.assertEqual(len(all_products), 4)

		created_product = all_products[3]
		self.assertEqual(created_product.id,4)
		self.assertEqual(created_product.title,'title')
		self.assertEqual(created_product.price,10.0)
		self.assertEqual(created_product.inventory_count,10)


	def test_all_products(self):
		'''
			Tests retrieving all of the products using graphQL
			- Performs a graphQL query to retrieve all the products.
			- Makes sure that there are three products in the response
			- Verifies that the values of the product in the response are correct
		'''

		query = '''
				{
					allProducts(availableOnly: false){
						id
						title
						price
						inventoryCount
					}
				}
			'''
		response = send_graphQL_query(test = self, query = query)
		all_products = response.get('allProducts',None)
		self.assertIsNot(all_products,None)

		self.assertEqual(len(all_products),3)

		for product in all_products:
			self.assertIn(product.get('title', None) , ['testProduct1','testProduct2','testProduct3'])
			self.assertIn(product.get('id', None) , ['ProductType_1','ProductType_2','ProductType_3'])
			self.assertIn(product.get('price', None) , [100.4,0.5,99999999])
			self.assertIn(product.get('inventoryCount', None) , [100000,99191919,0])

	def test_all_products_available_only(self):
		'''
			Tests retrieving all of the products with available inventory only using graphQL
			- Makes sure that only two products are retrieved
			- Makes sure the correct two products are retrieved by checking the values in the response
		'''

		query = '''
				{
					allProducts(availableOnly: true){
						id
						title
						price
						inventoryCount
					}
				}
			'''
		response = send_graphQL_query(test = self, query = query)
		all_products = response.get('allProducts',None)
		self.assertIsNot(all_products,None)
		self.assertEqual(len(all_products),2)

		for product in all_products:
			self.assertIn(product.get('title', None) , ['testProduct1','testProduct2'])
			self.assertIn(product.get('id', None) , ['ProductType_1','ProductType_2'])
			self.assertIn(product.get('price', None) , [100.4,0.5])
			self.assertIn(product.get('inventoryCount', None) , [100000,99191919])

	def test_product_deletion(self):
		'''
			Test deleting products using GraphQL
			- Creates a deleteProduct mutation and sends it the the graphQL endpoint
			- makes sure that a product was deleted by retrieving database records and ensuring that there are nwo two products
			- Makes sure that the correct product was deleted by checking the values of the products that currently exist in the database
		'''

		query = '''
			mutation{
				deleteProduct(id: "ProductType_3"){
					status
					description
				} 
			}
		'''

		response = send_graphQL_query(test = self, query = query)

		all_products = models.Product.objects.all()
		self.assertEqual(len(all_products), 2)
		for product in all_products:
			self.assertIn(product.title , ['testProduct1','testProduct2'])
			self.assertIn(product.id , [1,2])
			self.assertIn(product.price , [100.4,0.5])
			self.assertIn(product.inventory_count, [100000,99191919])


class CartTestCase(TestCase):
	'''
		test functionalities that are related to carts using internal functions
	'''

	def setUp(self):
		'''
			Creates 3 carts
		'''

		actions.create_cart()
		actions.create_cart()
		actions.create_cart()

	def test_cart_creation(self):
		'''
			Tests cart creation
			- retrieves carts from the database and makes sure that they are actually created
			- Makes sure that the newly created carts are not purchased by checking that cart.purchased is False
		'''
		all_carts = models.Cart.objects.all()
		self.assertEqual(len(all_carts),3)
		[self.assertEqual(cart.purchased, False) for cart in all_carts]

	def test_cart_deletion(self):
		'''
			Tests cart deletion
			- deletes a cart
			- makes sure that there are two carts in the database now
			- deletes another cart
			- makes sure that tehre are only one cart in the database
			- deletes a third cart and makes sure that there are no carts in the database
		'''

		all_carts = models.Cart.objects.all()

		actions.delete_cart(id = all_carts[2].id)
		all_carts = models.Cart.objects.all()
		self.assertEqual(len(all_carts),2)

		actions.delete_cart(id = all_carts[1].id)
		all_carts = models.Cart.objects.all()
		self.assertEqual(len(all_carts),1)		

		actions.delete_cart(id = all_carts[0].id)
		all_carts = models.Cart.objects.all()
		self.assertEqual(len(all_carts),0)		

class CartGraphQLTestCase(TestCase):
	'''
		Test functionalities that are related to prducts using GraphQL
	'''

	def setUp(self):
		'''
		 - creates a cart using a graphQL mutation
		'''
		query = '''
			mutation{
				createCart{
					status
					description
					cart{
						id
						products{
							id
							price
							title
							inventoryCount
						}
					}
				}
			}

		'''

		self.response = send_graphQL_query(test=self, query=query)
	def test_cart_creation(self):
		'''
			Tests cart creation
			- Makes sure that the graphQL response has the correct status
			- Makes sure that the graphQL response return a Cart object
			- Makes sure that the cart object has a products field
			- Makes sure that there are no products in the cart at creation
			- Makes sure that the cart is actually created by retrieving it directly from the database
		'''

		self.response = self.response.get('createCart',None)
		self.assertNotEqual(self.response, None)
		self.assertEqual(self.response.get('status'), 'success')
		cart = self.response.get('cart', None)
		self.assertNotEqual(cart, None)
		self.assertEqual(len(cart.get('products')), 0)

		all_carts = models.Cart.objects.all()
		self.assertEqual(len(all_carts), 1)
		self.assertEqual(all_carts[0].purchased, False)

	def test_cart_deletion(self):
		'''
			Tests cart deletion
			- creates another cart
			- Performs a grapQL mutation to delete a cart
			- Makes sure that the graphQL response has the correct status
			- Makes sure that the cart is deleted by making sure that the database has only one cart now
			- makes sure that the correct cart is deleted

		'''

		created_cart = actions.create_cart().get('cart')

		query = '''
			mutation{
				deleteCart(id: "CartType_1"){
					status
					description
				}
			}
		'''
		response = send_graphQL_query(test=self, query=query)
		response = response.get('deleteCart',None)
		self.assertNotEqual(response, None)
		self.assertEqual(response.get('status'), 'success')

		all_carts = models.Cart.objects.all()
		self.assertEqual(len(all_carts), 1)
		self.assertEqual(all_carts[0].id, created_cart.id)

class CartProductMapTestCase(TestCase):
	'''
		Test functionalities related to CartProductMap using internal functions
	'''

	def setUp(self):
		'''
			- Creates 4 products
			- Creates a cart
			- puts three out of the 4 products in the cart
		'''
		actions.create_product(
			title="testProduct1",
			price=100.4, 
			inventory_count=10)
		actions.create_product(
			title="testProduct2",
			price=0.5, 
			inventory_count=10)
		actions.create_product(
			title="testProduct3",
			price=99999999, 
			inventory_count=10)
		actions.create_product(
			title="testProduct4",
			price=99999999, 
			inventory_count=10)

		actions.create_cart()

		self.all_products = models.Product.objects.all()[1:]
		cart = models.Cart.objects.all()[0]

		[actions.add_product_to_cart(product_id=product.id,cart_id=cart.id)
			for product in self.all_products]

		self.cart = models.Cart.objects.all()[0]

	def test_add_product_to_cart(self):
		'''
			Tests adding a product to a cart
			- Retrieves the CartProductMap objects directly from the database
			- makes sure that there are three products in the cart
			- makes sure that the right products are in the cart
		'''

		all_cart_product_map = models.CartProductMap.objects.all()

		self.assertEqual(len(all_cart_product_map), 3)

		all_products_ids = [product.id for product in self.all_products]

		self.assertNotIn(
			False,
			[ cart_product_map.product.id in all_products_ids and self.cart.id == cart_product_map.cart.id
				for cart_product_map in all_cart_product_map]
		)

	def test_cart_remove_product(self):
		'''
			Tests removing a product from a cart
			- Counts the number of products in the cart and makes sure that they are 3
			- removes two products from the cart
			- Makes sure that the cart has only one product
			- removes the last product
			- makes sure that the cart now has no products in it
		'''

		all_cart_product_map = models.CartProductMap.objects.all()
		self.assertEqual(len(all_cart_product_map),3)
		[actions.remove_product_from_cart(product_id=product.id, cart_id=self.cart.id)
			for product in self.all_products[1:]]

		all_cart_product_map = models.CartProductMap.objects.all()
		self.assertEqual(len(all_cart_product_map),1)

		cart = all_cart_product_map[0]

		actions.remove_product_from_cart(product_id=cart.product.id, cart_id=cart.cart.id)
		all_cart_product_map = models.CartProductMap.objects.all()
		self.assertEqual(len(all_cart_product_map),0)


	def test_purchase_cart(self):
		'''
			Tests purchasing a cart
			- verify that the cart is not already purchased by verifying that cart.purchased is now False
			- performs a purchase operation
			- makes sure that the cart is purchased by verifying that cart.purchased is now True
			- Verifies that the inventory count for the products in the cart is decreased by one
			- Verifies that the inventory count for the product that wasn't in the cart is NOT decreased by one
		'''

		self.assertEqual(self.cart.purchased, False)
		[self.assertEqual(product.inventory_count, 10) for product in self.all_products]
		actions.purchase_cart(cart_id = self.cart.id)
		all_products = models.Product.objects.all()
		cart = models.Cart.objects.all()[0]

		self.assertEqual(cart.purchased, True)
		[self.assertEqual(product.inventory_count, 9) for product in all_products[1:]]
		self.assertEqual(all_products[0].inventory_count, 10)


class CartProductMapGraphQLTestCase(TestCase):
	'''
		Test functionalities related to CartProductMap using GraphQL
	'''

	def setUp(self):
		'''
			- creates a product and a cart
			- Puts the product in the cart using graphQL
		'''

		self.product = actions.create_product(
			title="testProduct1",
			price=100, 
			inventory_count=10).get('product')

		self.cart = actions.create_cart().get('cart')

		query = '''
			mutation{
				addProductToCart(
					productId: "ProductType_1",
					cartId: "CartType_1"
				) {
					status
					description
				}
			}

		'''
		self.response = send_graphQL_query(test=self, query=query).get('addProductToCart', None)
	def test_add_product_to_cart(self):
		'''
			Tests adding a product to a cart
			- makes sure that the product was put in the cart correctly
			- makes sure that the graphQL has the correct status
			- makes sure that the relationship between the product and the cart exist in the database
			- makes sure that the correct product was put in the currect cart
		'''
		self.assertNotEqual(self.response, None)
		self.assertEqual(self.response.get('status', None), 'success')
		all_cart_product_map = models.CartProductMap.objects.all()
		self.assertEqual(len(all_cart_product_map),1)
		self.assertEqual(self.cart.id, all_cart_product_map[0].cart.id)
		self.assertEqual(self.product.id, all_cart_product_map[0].product.id)
	def test_cart_remove_product(self):
		'''
			Tests removing a product from a cart
			- performs a product removal mutation
			- Makes sure that the response status is correct
			- makes sure that the connection between the cart and the product is removed from the database
		'''

		query = '''
			mutation{
				removeProductFromCart(
					cartId: "CartType_1"
					productId: "ProductType_1"
				){
					status
					description
				}
			}		
		'''
		response = send_graphQL_query(test=self, query=query).get('removeProductFromCart', None)
		self.assertNotEqual(response, None)
		self.assertEqual(response.get('status', None), 'success')

		all_cart_product_map = models.CartProductMap.objects.all()
		self.assertEqual(len(all_cart_product_map),0)
	def test_purchase_cart(self):
		'''
			Tests purchasing a cart
			- Performs a purchase operation
			- makes sure that the response status is correct
			- makes sure that the purchase status for the cart is correct ( turned cart.purchased from False to True)
			- Makes sure that the inventory count for the product is decreased
		'''

		query = '''
			mutation{
				purchaseCart(id: "CartType_1"){
					status
					description
				}
			}
		'''
		response = send_graphQL_query(test=self, query=query).get('purchaseCart', None)
		self.assertNotEqual(response, None)
		self.assertEqual(response.get('status'), 'success')

		all_carts = models.Cart.objects.all()
		product = models.Product.objects.all()[0]
		self.assertEqual(all_carts[0].purchased, True)

		self.assertEqual(product.inventory_count, 9)

		# test that the inventory count is going down



























































