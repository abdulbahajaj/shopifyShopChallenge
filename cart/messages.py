'''
This file defines all the responses that this API has

'''
STATUS = dict(
	success="success",
	error="error",
	not_Found="notFound",
)

def define_message(status, description):
	'''
		A way to define responses to requests and standarize them over all the application

		:param str status: the status of an operation. could be "success", "error", or "notFound"
		:param str description: elaborates more on the status of the operation.

		:return dict(status, description): a dictionary that contains the defined response
	'''
	return lambda: dict(
		status=status,
		description=description,
	)

'''
	Is returned when a given product id doesn't match any of our record
'''
product_not_found = define_message(
	status=STATUS['error'],
	description="The given product id has not been found"
)

'''
	Is returned to confirm that a product has been created
'''
product_created = define_message(
	status=STATUS['success'],
	description="Product has been created successfully"
)


'''
	Is returned to confirm that a product has been deleted
'''
product_deleted = define_message(
	status=STATUS['success'],
	description="Product has been deleted successfully"
)

'''
	Is returned to confirm that a cart has been created 
'''
cart_created = define_message(
	status=STATUS['success'],
	description="Cart has been created successfully"
)

'''
	Is returned to confirm that a cart has been deleted
'''
cart_deleted = define_message(
	status=STATUS['success'],
	description="Cart has been deleted successfully"
)

'''
	Is returned when a given cart id doesn't match any of our record
'''
cart_not_found = define_message(
	status=STATUS['error'],
	description="The given cart id has not been found"
)

'''
	Is returned to indicate that a product has been successfully added to a cart
'''
product_added_to_cart = define_message(
	status = STATUS['success'],
	description = "The given product has been successfully added to the cart"
)

'''
	Is returned to indicate that a product has been successfully removed from a cart
'''
product_removed_from_cart = define_message(
	status = STATUS['success'],
	description = "The given product has been successfully removed from the cart"
)

'''
	Is returned to indicate that a product has been successfully removed from a cart
'''
product_removed_from_cart = define_message(
	status = STATUS['success'],
	description = "The given product(s) has been successfully removed from the cart"
)

'''
	Is returned to indicate that a cart has been successfully purchased
'''
cart_successfully_purchased = define_message(
	status = STATUS['success'],
	description = "The cart has been purchased successfully"
)



























































