import graphene
import cart.schema

class Query(
	cart.schema.Query,
	graphene.ObjectType):
	pass

class Mutation(
	cart.schema.Mutation, 
	graphene.ObjectType):
	pass


schema = graphene.Schema(query=Query,mutation=Mutation)