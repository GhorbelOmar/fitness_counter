from fastapi import FastAPI, Body
from app.models import RepCountRequest
from app.rep_counter import count_reps as count_reps_logic
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/count-reps")
async def count_reps(payload: RepCountRequest = Body(...)):
    logger.info(f"Received request with {len(payload.data)} data points")
    rep_count = count_reps_logic(payload)
    return {"rep_count": rep_count}
