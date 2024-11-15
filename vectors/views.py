from django.shortcuts import render
from django.conf import settings
from sentence_transformers import SentenceTransformer
from vectors.models import Product
from vectors.serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from pgvector.django import L2Distance
from PIL import Image


# Create your views here.
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
image_model = SentenceTransformer('clip-ViT-B-32')

INDEX_NAME = settings.VERTEXAI_INDEX_NAME
INDEX_ENDPOINT_NAME = f"{INDEX_NAME}-endpoint"

class ProductListView(APIView):
    def get(self, request):
        query = request.GET.get('query')
        if query:
            # embedd the query
            # query neighbors in Vertex AI
            # extract product codes from the response
            # filter products by codes
            query_embedding = model.encode(query)
            response = INDEX_ENDPOINT_NAME.find_neighbors(
                    deployed_index_id = INDEX_ENDPOINT_NAME,
                    queries = [query_embedding],
                    num_neighbors = 10
                )
            print(response)
            product_codes = []
            for idx, neighbor in enumerate(response[0]):
                product_codes.append(neighbor['code'])
            
            products = Product.objects.filter(code__in=product_codes)           
        else:
            products = Product.objects.none()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    


class DProductListView(APIView):
    def get(self, request):
        query = request.GET.get('query')
        if query:
            query_embedding = model.encode(query)
            print(f"Query: {query}, Embedding: {query_embedding}")
            products = Product.objects.order_by(L2Distance('title_embedding', query_embedding))[:10]           
        else:
            products = Product.objects.none()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

def image_search(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        text = request.POST.get('search')
        if text:
            text_embedding = image_model.encode(text, convert_to_tensor=True)
            products = Product.objects.order_by(L2Distance('image_embedding', text_embedding[0]))[:10]
        elif image:
            image = Image.open(image).convert('RGB')
            embedding = image_model.encode([image], convert_to_tensor=True)
            products = Product.objects.order_by(L2Distance('image_embedding', embedding[0]))[:10]
    else:
        products = Product.objects.none()
    return render(request, 'image_search.html', {'products': products})
