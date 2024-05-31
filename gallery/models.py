from django.db import models

class Category(models.model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name