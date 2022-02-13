from rest_framework import serializers
from .models import Country, Character

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__' 

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__' 
