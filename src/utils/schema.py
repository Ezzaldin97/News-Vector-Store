from pydantic import BaseModel 
from typing import Dict, Optional, List

class NewsData(BaseModel):
    title: str
    description: str
    content: str
    url: Optional[str] = None
    image: Optional[str] = None
    publishedAt: Optional[str] = None
    source: Dict[str, str]

class CollectionVector(BaseModel):
    id: str
    embeddings: List[float]
    payload: Dict[str, str]