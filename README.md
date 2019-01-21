# Shopify intern challenge
This is the barebones of an online marketplace. It is implemented using Django, Python, graphene and SQLlite.

This program exposes a GraphQL API at /graphql

## It supports the following queries

### Retrieves all products regardless of whether or not there is available inventory
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

### Retrieves all products with available inventory
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

### Retrieves all carts
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
