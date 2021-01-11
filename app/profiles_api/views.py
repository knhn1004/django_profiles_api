from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from .serializers import HelloSerializer
from rest_framework.authentication import TokenAuthentication

from profiles_api import serializers, models, permissions


class HelloApiView(APIView):
    """ Test API View """
    serializer_class = HelloSerializer

    def get(self, request, format=None):
        """ Returns a list of APIView features """
        an_apiview = [
            'uses http methods as function (get, post, patch, put, delete)',
            'is similart oa traditional django view',
            'gives you the most control over your application logic',
            'is mapped manually to urls'
        ]
        return Response({'message': 'hello!', 'an_apiview': an_apiview})

    def post(self, request):
        """ Create a hlloe message with our name """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'

            return Response({'message': message})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """ Handle updating an object """
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """ Handle an partial update of an object """
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """ Delete an object """
        return Response({'method': 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """ Test API ViewSet """
    serializer_class = HelloSerializer

    def list(self, request):
        """ Return a hello message """

        a_viewset = [
            'uses actions (list, create, retrieve, update, partial_update)',
            'automatically maps to urls using Routers',
            'provides more functionality with less code'
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """ Create a new hello message """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """ Handle getting an object by its id """
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """ Handle updating an object by its id """
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """ Handle updating part of an object """
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """ Handle removing an object """
        return Response({'http_method': 'DELETE'})


class UserProfileViewset(viewsets.ModelViewSet):
    """ Handle creating and updating profiles """
    serializer_class = serializers.UserProfileSerializer

    # with queryset, we don't have to setup basename in urls
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)

    # adding search query filter
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)
