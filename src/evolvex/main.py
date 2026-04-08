from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from src.evolvex.crew import Evolvex
from datetime import datetime
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


class ResearchRequest(BaseModel):
    query: str


@app.get("/")
def serve_ui():
    return FileResponse(os.path.join("src", "evolvex", "index.html"))


@app.post("/research")
def research(data: ResearchRequest):

    inputs = {
        "topic": data.query,
        "current_year": datetime.now().year
    }

    try:

        crew = Evolvex().crew()
        result = crew.kickoff(inputs=inputs)

        return {
            "result": result.raw
        }

    except Exception as e:

        logger.exception("Crew execution failed")

        return {
            "result": "Error running research agent"
        }