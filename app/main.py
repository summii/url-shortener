from fastapi import FastAPI
from app.config import settings
from app.core.database import Base, engine
from app.api.routes import urls

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

# Include the URL routes
app.include_router(urls.router, tags=["URLs"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the URL Shortener API!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
