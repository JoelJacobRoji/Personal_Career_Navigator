from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any

# Import your awesome agents!
from market_agent import get_market_requirements, analyze_skill_gaps
from roadmap_agent import generate_30_day_roadmap

app = FastAPI(title="Career Co-Pilot API")

# Allow the React frontend (usually running on localhost:5173 for Vite) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For hackathon purposes, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the expected incoming data from React
class ProfileRequest(BaseModel):
    dream_role: str
    time_commitment: str
    user_profile: Dict[str, Any] # This is the JSON your friend parsed from the resume/github

@app.post("/generate-roadmap")
async def create_roadmap_endpoint(request: ProfileRequest):
    print(f"🚀 Received request for: {request.dream_role}")
    
    # 1. Market Intelligence
    market_data = get_market_requirements(request.dream_role)
    
    # 2. Gap Analysis
    gaps = analyze_skill_gaps(request.user_profile, market_data)
    
    # 3. Roadmap Generation
    roadmap_json = generate_30_day_roadmap(gaps, request.time_commitment)
    
    # Send the whole package back to React!
    return {
        "status": "success",
        "market_requirements": market_data,
        "gap_analysis": gaps,
        "roadmap_plan": roadmap_json
    }

# Run the server with: uvicorn api:app --reload