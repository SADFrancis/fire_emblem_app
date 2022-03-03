from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from .models import Character
from .serializers import CharacterSerializer
from core.settings import REALMS, GAME_TITLES
#import core
#from django.contrib.postgres.fields.jsonb import KeyTextTransform


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/realms/',
            'method': 'GET',
            'body': None,
            'description': 'Returns each Realm name'
        },
        {
            'Endpoint': '/realms/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns all resplendent units sharing a design theme of a specific realm'
        },        
        {
            'Endpoint': '/characters/',
            'method': 'GET/POST',
            'body': None,
            'description': 'Returns an array of characters and allows to create one'
        },
        {
            'Endpoint': '/characters/<str:Name>',
            'method': 'GET',
            'body': None,
            'description': 'Returns all resplendent characters with (case insensitve) Name (characters/Ishtar)'
        },        
        {
            'Endpoint': '/characters/latest',
            'method': 'GET',
            'body': None,
            'description': 'Returns most recently revealed unit published on site'
        },
        # {
        #     'Endpoint': '/characters/updatelatestarchived',
        #     'method': 'GET,POST',
        #     'body': None,
        #     'description': 'Gets most recently archived unit, and is used to update game_origin of the most recently archived unit'
        # },
        {
            'Endpoint': '/titles/',
            'method': 'GET',
            'body': None,
            'description': 'Returns dictionary of game titles'
        },
        {
            'Endpoint': '/titles/<str:key>',
            'method': 'GET',
            'body': None,
            'description': 'Returns all archived characters from the game title of a corresponding key (/titles/FE1). Current and future units are omitted due to lack of data.  '
        },
        {
            'Endpoint': '/year/',
            'method': 'GET',
            'body': None,
            'description': 'Returns all characters, to setup for year filtering'
        },
        {
            'Endpoint': '/year/<str:year>',
            'method': 'GET',
            'body': None,
            'description': 'Returns all characters of a specified year'
        },
        {
            'Endpoint': '/year/<str:year>/<str:month>',
            'method': 'GET',
            'body': None,
            'description': 'Returns all characters of a specified year and month (/year/2020/2)'
        },
    ]

    return Response(routes)


# class RealmList(generics.ListAPIView):
#     queryset = Character.objects.filter(data__realm =  )
#     serializer_class = CountrySerializer

# class CountryDetail(generics.RetrieveAPIView):
#     queryset = Country.objects.all()
#     serializer_class = CountrySerializer

class CharacterList(generics.ListCreateAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

    # def get_queryset(self):
    #     return self.queryset.filter(owner=self.request.name)

class CharacterDetail(generics.RetrieveAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

def realms(request):
    return JsonResponse(REALMS,safe = False)

def game_titles(request):
    return JsonResponse(GAME_TITLES,safe=False)

@api_view(['GET'])
def characterList(request):
    characters = Character.objects.filter(release_date__year=request.GET['year'])
    serializer = CharacterSerializer(characters, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def characterDetail(request,Name):
    characters = Character.objects.filter(name__icontains=Name)
    serializer = CharacterSerializer(characters, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def realmList(request,key):
    characters = Character.objects.filter(realm=REALMS[key])
    serializer = CharacterSerializer(characters, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def yearList(request,year):
    characters = Character.objects.filter(release_date__year=year)
    serializer = CharacterSerializer(characters, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def monthOfYearList(request,year,month):
    characters = Character.objects.filter(release_date__year=year).filter(release_date__month=month)
    serializer = CharacterSerializer(characters, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def titleList(request,key):
    characters = Character.objects.filter(game_origin=GAME_TITLES[key])
    serializer = CharacterSerializer(characters, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def LatestDetail(request):
    character = Character.objects.last()
    serializer = CharacterSerializer(character)
    return Response(serializer.data)

@api_view(['GET','POST'])
def UpdateLatestArchived(request):
    if request.method == 'GET':
        characters = Character.objects.filter(game_origin="")
        serializer = CharacterSerializer(instance = characters.first())
    else:
            characters = Character.objects.filter(game_origin="")
            serializer = CharacterSerializer(instance = characters.first(), data=request.data)
            if serializer.is_valid():
                serializer.save()
    return Response(serializer.data)