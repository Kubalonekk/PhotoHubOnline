import graphene
from graphene_django.types import DjangoObjectType
from .models import *
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile           #określamy na jakim modelu będziemy pracować

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


class PostType(DjangoObjectType):
    class Meta:
        model = Post

class ObserwowaniType(DjangoObjectType):
    class Meta:
        model = Obserwowani

class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    viewer = graphene.Field(UserType, token=graphene.String(required=True))
    me = graphene.Field(UserType)
    all_users = graphene.List(UserProfileType) # musimy sie trzymać dokładniej tej zmiennej przy ustawianiu resolve
    post = graphene.Field(PostType,
                         id=graphene.Int(),
                         tytul=graphene.String())
    all_posts = graphene.List(PostType)
    all_obserwowani = graphene.List(ObserwowaniType)
    
    def resolve_users(self, info):
        return get_user_model().objects.all()

    @login_required
    def resolve_viewer(self, info, **kwargs):
        return info.context.user

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication Failure!')
        return user
    

    def resolve_post(self, info, **kwargs):
        id = kwargs.get('id') 
        tytul = kwargs.get('tytul')
        if id is not None:
            return Post.objects.get(pk=id)
        if tytul is not None:
            return Post.objects.get(tytul=tytul)
        return none

    def resolve_all_users(self, info, **kwargs):
        return UserProfile.objects.all()
    
    def resolve_all_posts(self, info, **kwargs):
        return Post.objects.all()
    
    def resolve_all_obserwowani(self, info, **kwargs):
        return Obserwowani.objects.all()