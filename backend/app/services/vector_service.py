from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


COLLECTION_NAME = "geomind_documents"

# Local Qdrant storage
client = QdrantClient(path="./qdrant_data")


def initialize_collection():
    collections = client.get_collections().collections

    existing_names = [collection.name for collection in collections]

    if COLLECTION_NAME not in existing_names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )