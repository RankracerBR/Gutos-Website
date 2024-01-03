from unittest.mock import MagicMock
from django.test import TestCase
from .models import CustomUser
from core import views
import unittest


#Run the verification with python manage.py test
# Create your tests here.

class TestSearchImages(unittest.TestCase):
    def test_search_images_with_query(self): 

        request = MagicMock()
        request.method = 'GET'
        request.GET.get.return_value = 'dog'  # Query de exemplo

        with unittest.mock.patch('requests.get') as mocked_get:
            mocked_get.return_value.json.return_value = {
                'items': ['image1', 'image2']
            }
            result = views.Search_images(request)
            self.assertIsNotNone(result)
            # Adicione mais asserções para verificar se o comportamento é o esperado

    def test_search_images_no_query(self):
        request = MagicMock()
        request.method = 'GET'
        request.GET.get.return_value = None  # Simula nenhuma query

        result = views.Search_images(request)
        self.assertIsNone(result)
        
##Depois fazer testes no front-end

