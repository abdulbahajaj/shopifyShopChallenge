# Shopify intern challenge.
This is the barebones of an online marketplace. It is implemented using Django, Python, graphene and SQLlite.

This program exposes a GraphQL API at localhost/graphql.

## How to run the program:
1) Create a virtual environment with python 3.7 by running "virtualenv -p python3 {environmentName}" in your terminate.
2) Activate the environment by running "source {environmentName}/bin/activate"
3) Pull this repo
4) Go to the folder containing the repo in your terminal
5) Run "pip install requirements.txt"
6) Run "python manage.py runserver" to run the server
7) The graphql api should be now available in 0.0.0.0/graphql

Global ids are formated as follows: "NodeType_InternalID". For example ProductType_1 or CartType_1.
This API supports two node types ProductType and CartType.

You can also download this public docker image and run it. It exposed port 8000.
https://cloud.docker.com/u/abdulbahajaj/repository/docker/abdulbahajaj/graphqlshop

I have also deployed it to digitalocean's Kubernetes at the following link

http://157.230.75.162/graphql


## Default data
Currently the following products are in the shop:
```json
[
  {"title": "Cheese", "price": 4.3, "inventory_count": 10}, 
  {"title": "Milk", "price": 6.3, "inventory_count": 13}, 
  {"title": "Tomato", "price": 9.4, "inventory_count": 23}, 
  {"title": "Banana", "price": 10.4, "inventory_count": 43}, 
  {"title": "Potato", "price": 13.4, "inventory_count": 45}, 
  {"title": "Bread", "price": 5.8, "inventory_count": 85}, 
  {"title": "Bagels", "price": 7.8, "inventory_count": 77}, 
  {"title": "Chokos", "price": 4.8, "inventory_count": 47}, 
  {"title": "Mushrooms", "price": 2.8, "inventory_count": 17}, 
  {"title": "Yams", "price": 8.8, "inventory_count": 13}
]
```
It also has one cart with Milk and Cheese in it




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
example: http://157.230.75.162/graphql?query=%7B%0A%20%20allProducts(availableOnly%3A%20false)%20%7B%0A%20%20%20%20id%0A%20%20%20%20title%0A%20%20%20%20price%0A%20%20%20%20inventoryCount%0A%20%20%7D%0A%7D%0A&operationName=null

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

















