from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import router
from backend.database.database import initialize_database

app = FastAPI(
    title="Cloud Linux AI Monitor",
    description="ML-based anomaly detection and monitoring API for Linux servers",
    version="1.0.0"
)

# Initialize SQLite database and tables when the API starts
initialize_database()

# Allow the React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Cloud Linux AI Monitor API is running",
        "status": "online"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
