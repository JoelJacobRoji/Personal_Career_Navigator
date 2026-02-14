import json
import pandas as pd
from transformers import pipeline
from google import genai
import os
from dotenv import load_dotenv

# 1. Setup API Keys and Models using the NEW Google GenAI SDK
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Loading Hugging Face skill extractor... (This takes a few seconds)")
skill_extractor = pipeline(
    "token-classification", 
    model="jjzha/jobbert_skill_extraction", 
    aggregation_strategy="simple"
)

def get_market_requirements(dream_role):
    """MARKET INTELLIGENCE AGENT: Extracts required skills from job postings."""
    print(f"\n[Agent 1] Fetching market requirements for: {dream_role}")
    
    # Mocking the job description string for the hackathon prototype
    mock_job_description = """
    We are looking for an Enterprise Full Stack Engineer to build scalable systems. 
    You must have strong experience with React, Node.js, and TypeScript. 
    Backend knowledge of PostgreSQL, complex SQL queries, Docker, AWS, 
    and System Design is strictly required. Agile methodology is a plus.
    """
    
    # Extract entities using NLP
    extracted_entities = skill_extractor(mock_job_description)
    market_skills = list(set([ent['word'].strip() for ent in extracted_entities]))
    
    return {
        "dream_role": dream_role,
        "market_required_skills": market_skills
    }

def analyze_skill_gaps(user_profile_json, market_requirements_dict):
    """GAP ANALYSIS CRITIC: Compares user JSON against Market Intelligence."""
    print("[Agent 2] Running Gap Analysis Critic...")
    
    # Extract data from the local JSON file
    user_tech_skills = user_profile_json.get("skills", {}).get("technical_skills", [])
    user_soft_skills = user_profile_json.get("skills", {}).get("soft_skills", [])
    current_role = user_profile_json.get("personal_info", {}).get("current_role", "Unknown")
    
    # Extract data from your Market Agent
    dream_role = market_requirements_dict.get("dream_role", "Target Role")
    market_skills = market_requirements_dict.get("market_required_skills", [])
    
    # Prompt the LLM to find the gaps
    prompt = f"""
    You are an expert Career Gap Analyzer. Strictly compare a candidate's current skills 
    against the actual market requirements.
    
    Candidate's Current Role: {current_role}
    Candidate's Dream Role: {dream_role}
    Candidate's Verified Technical Skills: {', '.join(user_tech_skills)}
    Candidate's Verified Soft Skills: {', '.join(user_soft_skills)}
    Market Required Skills for {dream_role}: {', '.join(market_skills)}
    
    Perform a strict gap analysis. Output ONLY a raw JSON object with these exact keys:
    {{
      "validated_strengths": ["skills they already have that match the market perfectly"],
      "critical_missing_skills": ["high-priority missing skills they entirely lack"],
      "skills_to_upgrade": ["foundational skills they have, but need to be elevated to enterprise level"]
    }}
    Do not include markdown blocks like ```json.
    """
    
    # Use the new client generation method
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    
    try:
        return json.loads(response.text.strip())
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON. Check LLM output.", "raw_output": response.text}

# --- TEST EXECUTION ---
if __name__ == "__main__":
    
    # Step 1: Load the mock JSON profile from your local data folder
    with open("data/mock_profile.json", "r") as file:
        user_profile = json.load(file)
        
    dream_role_input = "Enterprise Full Stack Engineer"
    
    # Step 2: Run the Market Intelligence Pipeline
    market_data = get_market_requirements(dream_role_input)
    
    # Step 3: Run the Gap Analysis Pipeline
    gaps = analyze_skill_gaps(user_profile, market_data)
    
    # Print the final hand-off output
    print("\n✅ Final Gap Analysis Results (Ready for Roadmap Planner):")
    print(json.dumps(gaps, indent=2))