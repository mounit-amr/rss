from datetime import datetime, timedelta    
from fastapi import APIRouter,BackgroundTasks

from database import get_connection
from config import CACHE_TIME

router = APIRouter()

@router.get("/news")
async def getnews(backgroundtask: BackgroundTasks):
    now = datetime.utcnow()
    