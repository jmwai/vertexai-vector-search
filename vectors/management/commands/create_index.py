import os
import uuid
from django.conf import settings
from django.core.management.base import BaseCommand
from google.cloud import aiplatform


PROJECT_ID = os.getenv('PROJECT_ID')

LOCATION = "europe-west1"

INDEX_NAME = settings.VERTEXAI_INDEX_NAME

INDEX_ENDPOINT_NAME = f"{INDEX_NAME}endpoint"

aiplatform.init(project=PROJECT_ID, location=LOCATION)

BUCKET_URI = "gs://devfest-embeddings/embeddings.csv"


class Command(BaseCommand):
    help = 'Upload embeddings to Vertex AI'

    def handle(self, *args, **options):
        # create Index

        my_index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
            display_name=INDEX_NAME,
            contents_delta_uri=BUCKET_URI,
            dimensions=384, #Vector dimension
            approximate_neighbors_count=10, #Number of approximate neighbors
        )
        print(my_index)

        # create Index Endpoint

        my_index_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
            display_name=INDEX_ENDPOINT_NAME,
            public_endpoint_enabled=True
        )
        print(my_index_endpoint)

        # deploy the Index to the Index Endpoint

        my_index_endpoint.deploy_index(
            index=my_index, deployed_index_id=INDEX_ENDPOINT_NAME
        )
