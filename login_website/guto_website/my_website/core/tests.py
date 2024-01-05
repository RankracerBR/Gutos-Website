from unittest.mock import MagicMock
from django.test import TestCase
from .models import CustomUser, UserProfileHistory
from core import views
import unittest


#Run the verification with python manage.py test
# Create your tests here.

class CustomUserTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username = 'test_user',
            email='test@example.com',
            status='regular',
            description='Test Description'
        )

    def test_user_creation(self):
        """Test if a user is created properly"""
        self.assertEqual(self.user.username, 'test_user')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.status, 'regular')
        self.assertEqual(self.user.description, 'Test Description')


class UserProfileHistoryTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username= 'test_user',
            email =  'test@example.com',
            status = 'regular',
            description = 'Test Description'
        )

        self.history = UserProfileHistory.objects.create(
            user=self.user,
            last_name = 'Test_Last_Name',
            description = 'History Description'
        )


    def test_history_creation(self):
        """Test if a user profile history entry is created properly"""
        self.assertEqual(self.history.user, self.user)
        self.assertEqual(self.history.last_name, 'Test_Last_Name')
        self.assertEqual(self.history.description, 'History Description')


class TestSearchImages(unittest.TestCase):
    def test_search_images_with_query(self): 

        request = MagicMock()
        request.method = 'GET'
        request.GET.get.return_value = 'dog' 

        with unittest.mock.patch('requests.get') as mocked_get:
            mocked_get.return_value.json.return_value = {
                'items': ['image1', 'image2']
            }
            result = views.Search_images(request)
            self.assertIsNotNone(result)
            
    def test_search_images_no_query(self):
        request = MagicMock()
        request.method = 'GET'
        request.GET.get.return_value = None

        result = views.Search_images(request)
        self.assertIsNone(result)
        
##Depois fazer testes no front-end

