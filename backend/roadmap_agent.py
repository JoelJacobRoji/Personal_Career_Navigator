import json
from google import genai
import os
from dotenv import load_dotenv
from market_agent import get_market_requirements, analyze_skill_gaps

# Load API Key
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_30_day_roadmap(gap_analysis_json, time_commitment="10 hours/week"):
    """
    ROADMAP PLANNER AGENT
    Takes the gap analysis JSON and generates a 30-day learning path as JSON.
    """
    print("\n[Agent 3] Generating 30-Day Vibe-Check Roadmap...")
    
    critical_skills = gap_analysis_json.get("critical_missing_skills", [])
    upgrade_skills = gap_analysis_json.get("skills_to_upgrade", [])
    target_skills = critical_skills + upgrade_skills
    
    if not target_skills:
        return {"message": "You already have all the required skills for this role!"}

    prompt = f"""
    You are an expert Career AI Co-pilot. The user needs to learn these skills: {', '.join(target_skills)}.
    They can commit {time_commitment}.
    
    Create a highly actionable 30-day learning roadmap. 
    
    Output ONLY a raw JSON object (do not include markdown blocks like ```json). 
    Use this EXACT structure:
    {{
      "roadmap": [
        {{
          "week": 1,
          "theme": "Foundations of X",
          "focus_skills": ["Skill 1", "Skill 2"],
          "actionable_task": "What they need to do",
          "resource_suggestion": "Where to learn it",
          "vibe_check": "How to prove they learned it"
        }},
        ... (Generate objects for week 2, 3, and 4)
      ],
      "adaptability_note": "How this agent adapts if they fail week 1."
    }}
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    
    try:
        return json.loads(response.text.strip())
    except json.JSONDecodeError:
        return {"error": "Failed to parse Roadmap JSON", "raw": response.text}
# --- FULL PIPELINE EXECUTION ---
if __name__ == "__main__":
    
    # 1. Load the mock JSON profile your friend will eventually generate
    with open("data/mock_profile.json", "r") as file:
        user_profile = json.load(file)
        
    dream_role_input = "Enterprise Full Stack Engineer"
    
    # 2. Run the Market Intelligence Pipeline
    market_data = get_market_requirements(dream_role_input)
    
    # 3. Run the Gap Analysis Pipeline
    gaps = analyze_skill_gaps(user_profile, market_data)
    
    # 4. Run the Roadmap Planner
    final_roadmap = generate_30_day_roadmap(gaps, time_commitment="15 hours/week")
    
    print("\n=======================================================")
    print("🚀 FINAL 30-DAY ADAPTIVE ROADMAP GENERATED")
    print("=======================================================\n")
    print(final_roadmap)