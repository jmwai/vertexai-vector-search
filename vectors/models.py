from django.db import models
from pgvector.django import VectorField

# Create your models here.
class Product(models.Model):
    """
    product has:
     - title
     - description
     - price
     - code
     - image
     - title_embedding
     - image_embedding
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    code = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/', null=True)
    title_embedding = VectorField(dimensions=384, null=True)
    image_embedding = VectorField(dimensions=512, null=True)
    
    def __str__(self):
        return self.title