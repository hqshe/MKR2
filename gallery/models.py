from django.core.exceptions import ValidationError
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Image(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField()
    categories = models.ManyToManyField('Category')
    created_date = models.DateField(auto_now_add=True)
    age_limit = models.PositiveIntegerField()

    def clean(self):
        if self.age_limit < 0:
            raise ValidationError('Age limit cannot be negative.')

    def __str__(self):
        return self.title