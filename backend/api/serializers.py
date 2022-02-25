from rest_framework import serializers
from .models import Character
# from .models import Country
# class CountrySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Country
#         fields = '__all__' 

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__' 
