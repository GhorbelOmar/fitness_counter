from fastapi import FastAPI, Body
from app.models import RepCountRequest
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/count-reps")
async def count_reps(payload: RepCountRequest = Body(...)):
    logger.info(f"Received request with {len(payload.data)} data points")
    # Mock implementation
    return {"rep_count": 42}
