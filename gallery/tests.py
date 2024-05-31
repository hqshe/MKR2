# gallery/tests.py

from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Category, Image
from django.utils import timezone

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(str(self.category), 'Test Category')

    def test_category_name_max_length(self):
        max_length = self.category._meta.get_field('name').max_length
        self.assertEqual(max_length, 20)
