from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os

from database import db, database_url, database_name

app = FastAPI(title="Aqua-AI Management Suite API", version="1.0.0")

# CORS: allow all for dev preview
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Aqua-AI backend is running", "version": "1.0.0"}

@app.get("/test")
def test_connection():
    backend_status = "ok"
    connection_status = "disconnected"
    collections: List[str] = []

    if db is not None:
        try:
            # ping the server
            db.client.admin.command("ping")
            connection_status = "connected"
            collections = sorted(db.list_collection_names())
        except Exception as e:
            connection_status = f"error: {e}"  # surface error in preview
    else:
        connection_status = "no database configured"

    return {
        "backend": backend_status,
        "database": "mongodb",
        "database_url": f"{database_url[:25]}..." if database_url else None,
        "database_name": database_name,
        "connection_status": connection_status,
        "collections": collections,
    }

# Health endpoint for uptime checks
@app.get("/healthz")
def healthz():
    return {"status": "ok"}
