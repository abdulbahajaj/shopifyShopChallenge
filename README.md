# Shopify intern challenge.
This is the barebones of an online marketplace. It is implemented using Django, Python, graphene and SQLlite.

This program exposes a GraphQL API at 0.0.0.0/graphql.

##To run the program:
1) Create a virtual environment with python 3.7 by running "virtualenv -p python3 {environmentName}" in your terminate.
2) Activate the environment by running "source {environmentName}/bin/activate"
3) Pull this repo
4) Go to the folder containing the repo in your terminal
5) run "pip install requirements.txt"
6) run "python manage.py runserver"



Global ids are formated as follows: "NodeType_InternalID". For example ProductType_1 or CartType_1.
This API supports two node types ProductType and CartType.

## It supports the following queries.

### Retrieves all products regardless of whether or not there is available inventory.
```graphql
{
  allProducts(availableOnly: false) {
    id
    title
    price
    inventoryCount
  }
}
```

### Retrieves all products with available inventory.
```graphql
{
  allProducts(availableOnly: true) {
    id
    title
    price
    inventoryCount
  }
}
```

### Retrieves all carts with the products that are in them.
```graphql
{
  allCarts{
    edges{
      node{
        id
        created
        purchased
        totalDollarAmount
        products{
          id
          title
          inventoryCount
          price     
        }
      }
    }
  }
}
```

## It supports the following mutations

### Creates a new product
```graphql
mutation {
  createProduct(title: {str product_title}, inventoryCount: {int inventory_count}, price: { float product_price }) {
    status
    description
    product {
      id
      title
      price
      inventoryCount
    }
  }
}
```

### Deletes a product
```graphql
mutation{
  deleteProduct(id: {str product_id}){
    status
    description
  } 
}
```

### Creates a new cart
```graphql
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
```

### Deletes a cart
```graphql
mutation{
  deleteCart(id: {str cart_id}){
    status
    description
  }
}
```

### Adds a product to a cart
```graphql
mutation{
  deleteCart(id: {str cart_id}){
    status
    description
  }
}
```

### Removes a product from a cart
```graphql
mutation{
  removeProductFromCart(
    cartId: {str cart_id}
    productId: {str product_id}
  ){
    status
    description
  }
}
```

### Purchase a cart
```graphql
mutation{
  purchaseCart(id: {str cart_id}){
    status
    description
  }
}
```

















