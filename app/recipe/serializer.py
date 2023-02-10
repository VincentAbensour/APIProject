""" Serializer for the recipe app"""
from rest_framework import serializers
from core.models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes"""

    class Meta:
        model = Recipe
        fields = ['title','time','price','description','link']
        read_only_fields = ["id"]

class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for a single recipe"""

    class Meta(RecipeSerializer.Meta):
        fields = ['title','time','price','description','link', 'description']