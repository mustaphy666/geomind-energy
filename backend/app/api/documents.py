import os
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.retrieval_service import search_documents
from qdrant_client.models import PointStruct

from app.services.document_service import extract_text_from_pdf
from app.services.chunking_service import chunk_text
from app.services.embedding_service import embedding_service
from app.services.vector_service import (
    client,
    COLLECTION_NAME,
    initialize_collection,
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

initialize_collection()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    document_id = str(uuid.uuid4())

    file_path = os.path.join(
        UPLOAD_DIR,
        f"{document_id}.pdf"
    )

    contents = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    try:

        text = extract_text_from_pdf(
            file_path
        )

        chunks = chunk_text(text)

        points = []

        for index, chunk in enumerate(chunks):

            vector = embedding_service.embed(
                chunk
            )

            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "document_id": document_id,
                    "filename": file.filename,
                    "chunk_index": index,
                    "text": chunk,
                },
            )

            points.append(point)

        if points:

            client.upsert(
                collection_name=COLLECTION_NAME,
                points=points,
            )

    except Exception as e:

        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return {
        "document_id": document_id,
        "filename": file.filename,
        "characters": len(text),
        "chunks": len(chunks),
        "message": "Document processed successfully."
    }
@router.get("/search")
def search_document(
    query: str,
    document_id: str | None = None,
    limit: int = 5,
):

    results = search_documents(
        query=query,
        document_id=document_id,
        limit=limit,
    )

    return {
        "query": query,
        "results": [
            {
                "score": result.score,
                "document_id": result.payload.get("document_id"),
                "filename": result.payload.get("filename"),
                "chunk_index": result.payload.get("chunk_index"),
                "text": result.payload.get("text"),
            }
            for result in results
        ],
    }