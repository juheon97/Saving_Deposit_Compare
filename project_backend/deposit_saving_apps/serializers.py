from dataclasses import field
from rest_framework import serializers
from .models import DepositOptions, DepositProducts, SavingOptions, SavingProducts
from django.contrib.auth import get_user_model

User = get_user_model()

class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = '__all__'

class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = '__all__'


class SavingProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProducts
        fields = '__all__'

class SavingOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOptions
        fields = '__all__'


class UserContainsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'age']

class DepositProductsSerializer(serializers.ModelSerializer):
    user_contains = UserContainsSerializer(many=True, read_only=True)
    
    class Meta:
        model = DepositProducts
        fields = '__all__'

class SavingProductsSerializer(serializers.ModelSerializer):
    user_contains = UserContainsSerializer(many=True, read_only=True)
    
    class Meta:
        model = SavingProducts
        fields = '__all__'

