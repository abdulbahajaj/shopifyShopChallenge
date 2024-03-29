# Shopify intern challenge.
This is the barebones of an online marketplace. It is implemented using Django, Python, graphene and SQLlite.

This program exposes a GraphQL API at localhost/graphql.

Global ids are formated as follows: "NodeType_InternalID". For example ProductType_1 or CartType_1.
This API supports two node types ProductType and CartType.

## How to run the program:
1) Create a virtual environment with python 3.7 by running "virtualenv -p python3 {environmentName}" in your terminal.
2) Activate the environment by running "source {environmentName}/bin/activate"
3) Pull this repo
4) Go to the folder containing the repo in your terminal
5) Run "pip install requirements.txt"
6) Run "python manage.py runserver" to run the server
7) The graphql api should be now available in 0.0.0.0/graphql

You can also download this public docker image and run it. It exposed port 8000.
https://cloud.docker.com/u/abdulbahajaj/repository/docker/abdulbahajaj/graphqlshop

I have also deployed it to digitalocean's Kubernetes at the following link

http://157.230.75.162/graphql


## How to run tests
1) Create a virtual environment with python 3.7 by running "virtualenv -p python3 {environmentName}" in your terminal.
2) Activate the environment by running "source {environmentName}/bin/activate"
3) Pull this repo
4) Go to the folder containing the repo in your terminal
5) Run "pip install requirements.txt"
6) Run "python manage.py test" to run the tests


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
  {"title": "Eggplant", "price": 23.0, "inventory_count": 0}
  {"title": "Okra", "price": 23.0, "inventory_count": 0}
]
```
It also has one cart with Milk and Cheese in it




## It supports the following queries.

Note: to run some of the examples you might have to press "Prettify"

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
example: http://157.230.75.162/graphql?query=%7B%0A%20%20allProducts(availableOnly%3A%20true)%20%7B%0A%20%20%20%20id%0A%20%20%20%20title%0A%20%20%20%20price%0A%20%20%20%20inventoryCount%0A%20%20%7D%0A%7D%0A&operationName=null

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
example: http://157.230.75.162/graphql?query=%7B%0A%20%20allCarts%7B%0A%20%20%20%20edges%7B%0A%20%20%20%20%20%20node%7B%0A%20%20%20%20%20%20%20%20id%0A%20%20%20%20%20%20%20%20created%0A%20%20%20%20%20%20%20%20purchased%0A%20%20%20%20%20%20%20%20totalDollarAmount%0A%20%20%20%20%20%20%20%20products%7B%0A%20%20%20%20%20%20%20%20%20%20id%0A%20%20%20%20%20%20%20%20%20%20title%0A%20%20%20%20%20%20%20%20%20%20inventoryCount%0A%20%20%20%20%20%20%20%20%20%20price%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A&operationName=null

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
example: http://157.230.75.162/graphql?query=mutation%20%7B%0A%20%20createProduct(title%3A%20%22Witloof%22%2C%20inventoryCount%3A%2010%2C%20price%3A%202)%20%7B%0A%20%20%20%20status%0A%20%20%20%20description%0A%20%20%20%20product%20%7B%0A%20%20%20%20%20%20id%0A%20%20%20%20%20%20title%0A%20%20%20%20%20%20price%0A%20%20%20%20%20%20inventoryCount%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A&operationName=undefined

### Deletes a product
```graphql
mutation{
  deleteProduct(id: {str product_id}){
    status
    description
  } 
}
```
example: http://157.230.75.162/graphql?query=mutation%7B%0A%20%20deleteProduct(id%3A%20%22ProductType_12%22)%7B%0A%20%20%20%20status%0A%20%20%20%20description%0A%20%20%7D%20%0A%7D%0A&operationName=undefined

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
example: http://157.230.75.162/graphql?query=mutation%7B%0A%20%20createCart%7B%0A%20%20%20%20status%0A%20%20%20%20description%0A%20%20%20%20cart%7B%0A%20%20%20%20%20%20id%0A%20%20%20%20%20%20products%7B%0A%20%20%20%20%20%20%20%20id%0A%20%20%20%20%20%20%20%20price%0A%20%20%20%20%20%20%20%20title%0A%20%20%20%20%20%20%20%20inventoryCount%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A&operationName=undefined


### Deletes a cart
```graphql
mutation{
  deleteCart(id: {str cart_id}){
    status
    description
  }
}
```
example: http://157.230.75.162/graphql?query=mutation%7B%0A%20%20deleteCart(id%3A%20%22CartType_2%22)%7B%0A%20%20%20%20status%0A%20%20%20%20description%0A%20%20%7D%0A%7D%0A&operationName=undefined

### Adds a product to a cart
```graphql
mutation{
  addProductToCart(
    productId: "ProductType_1",
    cartId: "CartType_1"
  ){
    status
    description
  }
}
```
example: http://157.230.75.162/graphql?query=mutation%7B%0A%20%20addProductToCart(%0A%20%20%20%20productId%3A%20%22ProductType_1%22%2C%0A%20%20%20%20cartId%3A%20%22CartType_1%22%0A%20%20)%7B%0A%20%20%20%20status%0A%20%20%20%20description%0A%20%20%7D%0A%7D%0A&operationName=undefined

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
example: http://157.230.75.162/graphql?query=mutation%7B%0A%20%20removeProductFromCart(%0A%20%20%20%20cartId%3A%20%22CartType_1%22%0A%20%20%20%20productId%3A%20%22ProductType_1%22%0A%20%20)%7B%0A%20%20%20%20status%0A%20%20%20%20description%0A%20%20%7D%0A%7D%0A&operationName=undefined

### Purchase a cart
```graphql
mutation{
  purchaseCart(id: {str cart_id}){
    status
    description
  }
}
```
example: http://157.230.75.162/graphql?query=mutation%20%7B%0A%20%20purchaseCart(id%3A%20%22CartType_1%22)%20%7B%0A%20%20%20%20status%0A%20%20%20%20description%0A%20%20%7D%0A%7D%0A&operationName=undefined















