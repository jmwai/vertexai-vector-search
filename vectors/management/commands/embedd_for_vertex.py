import os
import csv
from PIL import Image
from io import BytesIO
import requests
from sentence_transformers import SentenceTransformer
from django.core.management.base import BaseCommand


from django.conf import settings



model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
image_model = SentenceTransformer('clip-ViT-B-32')

class Command(BaseCommand):
    help = 'Create embeddings for products'

    def handle(self, *args, **options):
        products = os.path.join(settings.BASE_DIR, 'products.csv')
        with open(products, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for line in reader:
                code = line[0]
                title = line[1]
                url = line[2]
                response = requests.get(url)
                image = Image.open(BytesIO(response.content)).convert('RGB')

                image_embedding = image_model.encode([image], convert_to_tensor=True)
                title_embedding = model.encode([title])

                print(f"Title: {title}, Embedding: {title_embedding}")
                #write to csv
                with open('embeddings.csv', mode='a') as file:
                    writer = csv.writer(file)
                    writer.writerow([code, title, image_embedding[0]])