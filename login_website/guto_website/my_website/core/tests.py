from .models import CadastroUsuario
from unittest.mock import MagicMock
from django.test import TestCase
from core import views
import unittest


#Run the verification with python manage.py test
# Create your tests here.
class CadastroUsuarioModelTest(TestCase):
    def test_create_cadastro_usuario(self):
        usuario = CadastroUsuario(
            complete_name="Alice",
            complete_email="alice@example.com",
            complete_password='123',
            complete_description = 'Description'
        )
        
        #Salva o usuário
        usuario.save()
        
        saved_usuario = CadastroUsuario.objects.get(complete_email="alice@example.com")
        
        self.assertEqual(saved_usuario.complete_name, 'Alice')
        
        self.assertEqual(saved_usuario.complete_description, 'Description')
        
    
    def test_update_cadastro_usuario(self):
        usuario = CadastroUsuario(
            complete_name="Bob",
            complete_email="Bob@example.com",
            complete_password='1234',
            complete_description = 'Another Description'
        )
        
        usuario.save()
        
        #Atualiza a descrição
        usuario.complete_description = "Updated Description"
        usuario.save()
        
        updated_usuario = CadastroUsuario.objects.get(complete_email="Bob@example.com")
        
        self.assertEqual(updated_usuario.complete_description, "Updated Description")
        
    
    def test_delete_cadastro_usuario(self):
        usuario = CadastroUsuario(
            complete_name="Charlie",
            complete_email="Charlie@example.com",
            complete_password='1234',
            complete_description = 'A Description'
        )
        
        usuario.save()
        
        usuario.delete()
        
        with self.assertRaises(CadastroUsuario.DoesNotExist):
            CadastroUsuario.objects.get(complete_email="charlie@doesnt_exist_example.com")



class TestSearchImages(unittest.TestCase):
    def test_search_images_with_query(self): 

        request = MagicMock()
        request.method = 'GET'
        request.GET.get.return_value = 'dog'  # Query de exemplo

        with unittest.mock.patch('requests.get') as mocked_get:
            mocked_get.return_value.json.return_value = {
                'items': ['image1', 'image2']
            }
            result = views.search_images(request)
            self.assertIsNotNone(result)
            # Adicione mais asserções para verificar se o comportamento é o esperado

    def test_search_images_no_query(self):
        request = MagicMock()
        request.method = 'GET'
        request.GET.get.return_value = None  # Simula nenhuma query

        result = views.search_images(request)
        self.assertIsNone(result)
        
##Depois fazer testes no front-end