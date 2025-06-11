import random
import string
from sqlalchemy.orm import Session
from app.models.url import URL
from app.schemas.url import URLCreate 

# create url services
def generate_short_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))\
    
def create_short_url(db: Session, url: URLCreate) -> URL:
    while True:
        short_code = generate_short_code()

        existing = db.query(URL).filter(URL.short_code == short_code).first()
        if not existing:
            break

    db_url = URL(
        original_url = str(url.original_url),
        short_code = short_code
    )

    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url
def get_url_by_short_code(db: Session, short_code: str) -> URL:
    """Get URL by short code"""
    return db.query(URL).filter(
        URL.short_code == short_code,
        URL.is_active == True
    ).first()

def increment_clicks(db: Session, url: URL):
    """Increment click count"""
    url.clicks += 1
    db.commit()