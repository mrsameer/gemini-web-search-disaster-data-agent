from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.agent import DisasterAgent
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Disaster Data Agent")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = DisasterAgent()

class SearchRequest(BaseModel):
    query: str

@app.post("/api/search")
async def search_disasters(request: SearchRequest):
    try:
        results = agent.search_and_extract(request.query)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/export")
async def export_disasters(request: SearchRequest):
    try:
        results = agent.search_and_extract(request.query)
        json_str = json.dumps(results, indent=2)
        return Response(
            content=json_str,
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=disaster_data.json"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"}
