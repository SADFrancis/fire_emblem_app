from django.shortcuts import render
from rest_framework import generics
from .models import Country, Character
from .serializers import CountrySerializer, CharacterSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/country/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of countries'
        },
        {
            'Endpoint': '/country/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single country object'
        },
        {
            'Endpoint': '/characters/',
            'method': 'GET/POST',
            'body': None,
            'description': 'Returns an array of characters and allows to create one'
        },
        {
            'Endpoint': '/characters/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of characters'
        },
    ]

    return Response(routes)


class CountryList(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class CountryDetail(generics.RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class CharacterList(generics.ListCreateAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

class CharacterDetail(generics.RetrieveAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer