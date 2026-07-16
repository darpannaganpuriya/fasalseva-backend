from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routes import auth, predictions, storage, weather, schemes, user
from app.services.ml_service import load_models_on_startup
from app.utils.logging import setup_logging

setup_logging()

app = FastAPI(title="FasalSeva AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(user.router, prefix="/api/user", tags=["user"])
app.include_router(predictions.router, prefix="/api/predict", tags=["predictions"])
app.include_router(storage.router, prefix="/api/storage", tags=["storage"])
app.include_router(weather.router, prefix="/api/weather", tags=["weather"])
app.include_router(schemes.router, prefix="/api/schemes", tags=["schemes"])


@app.on_event("startup")
def startup_event() -> None:
    init_db()
    load_models_on_startup()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

