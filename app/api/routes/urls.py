from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.url import URLCreate, URLResponse
from app.services import url_service
from app.config import settings

router = APIRouter()
@router.post("/shorten", response_model=URLResponse)
def create_short_url(url: URLCreate, db: Session = Depends(get_db)):
    db_url = url_service.create_short_url(db, url)

    short_url = f"{settings.BASE_URL}/{db_url.short_code}"
    return URLResponse(
        id=db_url.id,
        short_code=db_url.short_code,
        short_url=short_url,
        original_url=db_url.original_url,
        is_active=db_url.is_active,
        clicks=db_url.clicks,
        created_at=db_url.created_at
    )

@router.get("/{short_code}")
def redirect_to_original_url(short_code: str, db: Session = Depends(get_db)):
    url = url_service.get_url_by_short_code(db, short_code)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    url_service.increment_clicks(db, url)
    return RedirectResponse(url=url.original_url)

@router.get("/stats/{short_code}", response_model=URLResponse)
def get_url_stats(short_code: str, db: Session = Depends(get_db)):
    url = url_service.get_url_by_short_code(db, short_code)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    short_url = f"{settings.BASE_URL}/{url.short_code}"
    
    return URLResponse(
        id=url.id,
        short_code=url.short_code,
        short_url=short_url,
        original_url=url.original_url,
        is_active=url.is_active,
        clicks=url.clicks,
        created_at=url.created_at
    )
