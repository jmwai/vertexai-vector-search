from sentence_transformers import SentenceTransformer
from django.core.management.base import BaseCommand
from vectors.models import Product
from django.core.files import File
import os
import json
import csv
from django.conf import settings

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

class Command(BaseCommand):
    help = 'Load products into the database'

    def handle(self, *args, **options):
        products = os.path.join(settings.BASE_DIR, 'products.csv')
        with open(products, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for line in reader:
                
                title = line[1]
                title_embedding = model.encode([title])
                print(dir(title_embedding))
                print(f"Title: {title}, Embedding: {title_embedding}")
                product = Product()
                product.title = title
                product.code = line[0]
                product.price = line[4]
                product.description = line[5]
                product.title_embedding = title_embedding[0]
                product.save()

               
