from qdrant_client.models import ScoredPoint
from qdrant_client import models
from app.services.vector_service import (
    client,
    COLLECTION_NAME,
)
from app.services.embedding_service import embedding_service


def search_documents(
    query: str,
    document_id: str | None = None,
    limit: int = 5,
) -> list[ScoredPoint]:

    query_vector = embedding_service.embed(query)

    query_filter = None

    if document_id:
        query_filter = {
            "must": [
                {
                    "key": "document_id",
                    "match": {
                        "value": document_id
                    },
                }
            ]
        }

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter=models.Filter(
            must=[models.FieldCondition(
                key="document_id",
                match=models.MatchValue(value=document_id)
            )] if document_id else []
        ),
        limit=limit,
    ).points

    return results