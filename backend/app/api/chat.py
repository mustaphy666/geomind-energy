from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.retrieval_service import search_documents
from app.services.llm_service import llm_service


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


class ChatRequest(BaseModel):

    question: str
    document_id: str | None = None


@router.post("")
def chat(request: ChatRequest):

    results = search_documents(
        query=request.question,
        document_id=request.document_id,
        limit=5,
    )

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No relevant information found."
        )

    context_parts = []

    for result in results:

        text = result.payload.get("text", "")

        context_parts.append(text)

    context = "\n\n---\n\n".join(
        context_parts
    )

    answer = llm_service.generate(
        question=request.question,
        context=context,
    )

    return {
        "question": request.question,
        "answer": answer,
        "sources": [
            {
                "filename": result.payload.get("filename"),
                "chunk_index": result.payload.get("chunk_index"),
                "score": result.score,
            }
            for result in results
        ],
    }