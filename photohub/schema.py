import graphene
import graphql_jwt


from PhotoHubAPP.schema import Query as userprofile_query
from PhotoHubAPP.schema import Mutation as mutations


class Mutation(mutations, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class Query(userprofile_query, graphene.ObjectType):
    pass

schema = graphene.Schema(mutation=Mutation, query=Query)