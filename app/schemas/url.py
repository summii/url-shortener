from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

# create pydantic schemas
class URLBase(BaseModel):
    original_url: HttpUrl

class URLCreate(URLBase):
    pass 

class URLResponse(URLBase):
    id: int
    short_code: str
    short_url: str
    original_url: str
    is_active: bool
    clicks: int
    created_at: datetime

    class Config:
        from_attributes = True