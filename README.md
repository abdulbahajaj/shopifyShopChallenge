# Shopify intern challenge.
This is the barebones of an online marketplace. It is implemented using Django, Python, graphene and SQLlite.

This program exposes a GraphQL API at /graphql

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
  allProducts(availableOnly: false) {
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
	deleteCart(id: ){
    status
    description
  }
}
```

### Adds a product to a cart
```graphql
mutation{
	deleteCart(id: "CartType_1"){
    status
    description
  }
}
```

### Removes a product from a cart
```graphql
mutation{
	removeProductFromCart(
    cartId: "CartType_1"
    productId: "ProductType_1"
  ){
    status
    description
  }
}
```

### Purchase a cart
```graphql
mutation{
  purchaseCart(id: "CartType_3"){
    status
    description
  }
}
```

















