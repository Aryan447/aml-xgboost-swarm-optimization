from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.v1.endpoints import router as api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Mount Frontend
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include API Router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    # serve the frontend
    return FileResponse('app/static/index.html')

@app.get("/health")
def health_check():
    return {"status": "ok"}
