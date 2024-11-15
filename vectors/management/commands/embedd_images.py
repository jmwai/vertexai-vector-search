from sentence_transformers import SentenceTransformer
from django.core.management.base import BaseCommand
from vectors.models import Product
from django.core.files import File
import os
import json
import csv
from django.conf import settings
from PIL import Image
from io import BytesIO
import requests

model = SentenceTransformer('clip-ViT-B-32')

class Command(BaseCommand):
    help = 'Load products into the database'

    def handle(self, *args, **options):
        products = os.path.join(settings.BASE_DIR, 'products.csv')
        with open(products, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for line in reader:
                code = line[0]
                try:
                    product = Product.objects.get(code=code)
                except Product.DoesNotExist:
                    continue
                if not product.image:
                    try:

                        url = line[2]
                        response = requests.get(url)
                        image = Image.open(BytesIO(response.content)).convert('RGB')
                        embedding = model.encode([image], convert_to_tensor=True)
                        product.image_embedding = embedding[0]
                        product.image = File(BytesIO(response.content), name=f"{code}.jpg")
                        product.save()
                        print(f"Code: {code}, Embedding: {embedding}")
                    except Exception as e:
                        print(f"Error: {e}")
                        


               
