"""View for the Recipe App"""
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe.serializer import RecipeSerializer, RecipeDetailSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    """View for the recipe"""
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes linked to the authenticated user"""
        return self.queryset.filter(user = self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeDetailSerializer
        else:
            return RecipeSerializer

'''class RecipeDetailViewSet(RecipeViewSet):
    """View for the recipe"""
    serializer_class = RecipeDetailSerializer'''