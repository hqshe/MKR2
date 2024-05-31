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

class ImageModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.image = Image.objects.create(
            title='Test Image',
            image='path/to/image.jpg',
            created_date=timezone.now().date(),
            age_limit=18
        )
        self.image.categories.add(self.category)

    def test_image_creation(self):
        self.assertEqual(self.image.title, 'Test Image')
        self.assertEqual(self.image.image, 'path/to/image.jpg')
        self.assertEqual(self.image.age_limit, 18)
        self.assertEqual(str(self.image), 'Test Image')

    def test_image_category_relationship(self):
        self.assertIn(self.category, self.image.categories.all())

    def test_image_title_max_length(self):
        max_length = self.image._meta.get_field('title').max_length
        self.assertEqual(max_length, 255)

    def test_image_auto_now_add(self):
        self.assertIsNotNone(self.image.created_date)
        self.assertEqual(self.image.created_date, timezone.now().date())

    def test_image_age_limit_positive(self):
        with self.assertRaises(ValidationError):
            invalid_image = Image(
                title='Invalid Image',
                image='path/to/image.jpg',
                created_date=timezone.now().date(),
                age_limit=-1
            )
            invalid_image.full_clean()  # This will trigger validation

    def test_image_multiple_categories(self):
        category2 = Category.objects.create(name='Second Category')
        self.image.categories.add(category2)
        self.assertIn(category2, self.image.categories.all())
        self.assertEqual(self.image.categories.count(), 2)