from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import pdfs, chat, projects
from app.db.store import load_db

# FastAPI app
app = FastAPI(title="RAG Policy API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(pdfs.router)
app.include_router(chat.router)
app.include_router(projects.router)


@app.on_event("startup")
def startup_event():
    load_db()
