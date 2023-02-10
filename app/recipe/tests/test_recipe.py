"""Test for the Recipe app"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Recipe
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from recipe.serializer import RecipeSerializer, RecipeDetailSerializer

RECIPE_URL = reverse('recipe:recipe-list')

def url_detailed_recipe(id):
    """Get url for a specific recipe endpoint"""
    return reverse('recipe:recipe-detail', args=[id])

def helper_create_recipe(user,**args):
    """Create a recipe for test"""

    default_values = {
            'user' : user,
            'title' : 'testrecipe',
            'time' : 5,
            'price' : 5.50,
            'description' : 'test recipe description',
            'link' : 'link',
            }
    default_values.update(**args)
    recipe = Recipe.objects.create(**default_values)
    return recipe

class PublicRecipeTest(TestCase):
    """Test unauthenticated requests for the Recipe API"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_mandatory(self):
        """Test that auth is mandotory to make requests"""

        response = self.client.get(RECIPE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class AuthRecipeTest(TestCase):
    """Test authenticated requests for the Recipe API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email = "test@example.com",
            password = "test1234",
            firstname = "testfirst",
            lastname = "testlast",
        )
        self.client.force_authenticate(self.user)

    def test_get_recipes_list(self):
        """Test access of recipe's list"""
        helper_create_recipe(user=self.user)
        helper_create_recipe(user=self.user)

        response = self.client.get(RECIPE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        recipes = Recipe.objects.all().order_by('-id')
        serilizer = RecipeSerializer(recipes, many=True)
        self.assertEqual(response.data, serilizer.data)

    def test_list_only_for_user(self):
        """Test access of recipe's list for a specific user"""
        second_user = get_user_model().objects.create_user(
            email = "test2@example.com",
            password = "test21234",
            firstname = "test2first",
            lastname = "test2last",
        )
        self.client.force_authenticate(self.user)

        helper_create_recipe(user=self.user)
        helper_create_recipe(user=self.user)

        helper_create_recipe(user=second_user)

        response = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.filter(user=self.user).order_by('-id')
        serilizer = RecipeSerializer(recipes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serilizer.data)

    def test_get_detailed_recipe(self):
        """Test access of specific recipe for an auth user"""
        helper_create_recipe(user=self.user)

        recipe = Recipe.objects.get(user=self.user)
        url = url_detailed_recipe(recipe.id)
        response = self.client.get(url)

        serilizer = RecipeDetailSerializer(recipe)

        self.assertEqual(response.data, serilizer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)