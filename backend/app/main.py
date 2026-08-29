from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.documents import router as documents_router
from app.api.chat import router as chat_router
from app.api.welllogs import router as welllogs_router
from app.api.petrophysics import router as petrophysics_router
app = FastAPI(
    title="GeoMind AI",
    version="0.1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents_router) 
app.include_router(chat_router)
app.include_router(welllogs_router)
app.include_router(
    petrophysics_router
)
@app.get("/")
def root():
    return {
        "message": "Welcome to GeoMind AI 🚀"
    }
