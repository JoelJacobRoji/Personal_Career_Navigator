"""
Job Matcher - Analyze dream job requirements and match with user profile
"""

import re
from typing import Dict, List, Set, Any
from pathlib import Path



# Import config
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import Config


class JobMatcher:
    """Match user profile with dream job requirements"""
    
    def __init__(self):
        print("🔧 Initializing Job Matcher...")
        self.tech_skills_lower = {skill.lower() for skill in Config.TECH_SKILLS}
        self.job_skill_templates = {
            "data scientist": {
                "Python", "Pandas", "NumPy", "Matplotlib",
                "Scikit-learn", "Machine Learning",
                "Statistics", "SQL", "Deep Learning",
                "NLP", "EDA", "Data Visualization"
            },
            "machine learning engineer": {
                "Python", "TensorFlow", "PyTorch",
                "Scikit-learn", "Deep Learning",
                "Machine Learning", "NLP"
            },
            "frontend developer": {
                "HTML", "CSS", "JavaScript",
                "Angular", "React", "Bootstrap"
            }
        }
        print("✅ Job Matcher initialized\n")
    
    def extract_job_requirements(self, job_description: str) -> Dict[str, Any]:
        """Extract requirements from job description text"""
        print(f"📋 Analyzing dream job: {job_description[:50]}...")
        
        # Extract required skills
        required_skills = set()
        description_lower = job_description.lower()

        # If input is very short, treat as job title only
        if len(job_description.split()) <= 5:
            for title, skills in self.job_skill_templates.items():
                if title in description_lower:
                    required_skills = skills
                    print("ℹ Using predefined skill template for job title")
                    break

        for skill in Config.TECH_SKILLS:
            if skill.lower() in description_lower:
                required_skills.add(skill)
        print(f"Required Skills Extracted: {required_skills}")

        # Fallback if required_skills is empty and job is data scientist
        DATA_SCIENTIST_SKILLS = {
            "Python", "Pandas", "NumPy", "Matplotlib",
            "Scikit-learn", "Machine Learning",
            "Statistics", "SQL", "Deep Learning",
            "NLP", "EDA", "Data Visualization"
        }
        if not required_skills and "data scientist" in job_description.lower():
            required_skills = DATA_SCIENTIST_SKILLS
        
        # Extract years of experience
        experience_patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s+)?experience',
            r'experience.*?(\d+)\+?\s*(?:years?|yrs?)',
            r'minimum.*?(\d+)\+?\s*(?:years?|yrs?)'
        ]
        
        years_required = 0
        for pattern in experience_patterns:
            match = re.search(pattern, description_lower)
            if match:
                years_required = max(years_required, int(match.group(1)))
        
        # Extract education requirements
        education_required = []
        edu_patterns = [
            r'(Bachelor|Master|PhD|B\.Tech|M\.Tech|MBA)[\s\w]*(?:in\s+)?([A-Za-z\s]+)',
        ]
        
        for pattern in edu_patterns:
            matches = re.finditer(pattern, job_description, re.IGNORECASE)
            for match in matches:
                education_required.append({
                    "degree": match.group(1).strip(),
                    "field": match.group(2).strip() if len(match.groups()) > 1 else ""
                })
        
        # Categorize skills by importance (appears multiple times = more important)
        skill_frequency = {}
        for skill in required_skills:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            count = len(re.findall(pattern, description_lower))
            skill_frequency[skill] = count
        
        # Sort by frequency (most mentioned = most important)
        critical_skills = sorted(skill_frequency.items(), key=lambda x: x[1], reverse=True)
        
        requirements = {
            "job_title": self.extract_job_title(job_description),
            "required_skills": sorted(list(required_skills)),
            "critical_skills": [skill for skill, _ in critical_skills[:10]],  # Top 10
            "years_experience_required": years_required,
            "education_required": education_required,
            "total_skills_required": len(required_skills)
        }
        
        print(f"✅ Extracted {len(required_skills)} required skills")
        print(f"✅ Experience required: {years_required} years")
        print(f"✅ Top critical skills: {', '.join(requirements['critical_skills'][:5])}\n")
        
        return requirements
    
    def extract_job_title(self, job_description: str) -> str:
        """Extract job title from description"""
        lines = job_description.split('\n')
        
        # Job title usually in first few lines or contains keywords
        for line in lines[:5]:
            line = line.strip()
            if any(keyword in line.lower() for keyword in 
                   ['engineer', 'developer', 'analyst', 'manager', 'architect', 
                    'scientist', 'specialist', 'lead', 'senior', 'junior']):
                return line
        
        # Fallback: return first non-empty line
        for line in lines:
            if line.strip():
                return line.strip()
        
        return "Unknown Position"
    
    def calculate_match_score(self, user_profile: Dict, job_requirements: Dict) -> Dict[str, Any]:
        """Calculate how well user matches the job"""
        print("🎯 Calculating job match score...")
        
        user_skills = set(user_profile.get('skills', {}).get('technical_skills', []))
        required_skills = set(job_requirements.get('required_skills', []))
        critical_skills = set(job_requirements.get('critical_skills', []))
        
        # Skills match
        matching_skills = user_skills & required_skills
        missing_skills = required_skills - user_skills
        matching_critical = user_skills & critical_skills
        missing_critical = critical_skills - user_skills
        
        # Calculate percentages
        skills_match_percentage = (len(matching_skills) / len(required_skills) * 100) if required_skills else 0
        critical_match_percentage = (len(matching_critical) / len(critical_skills) * 100) if critical_skills else 0
        
        # Experience match
        user_experience = user_profile.get('experience', {}).get('years', 0)
        required_experience = job_requirements.get('years_experience_required', 0)
        experience_match = (user_experience >= required_experience)
        
        # Overall match score (weighted)
        overall_score = (
            skills_match_percentage * 0.5 +           # 50% weight on all skills
            critical_match_percentage * 0.3 +         # 30% weight on critical skills
            (100 if experience_match else 0) * 0.2    # 20% weight on experience
        )
        
        match_analysis = {
            "overall_match_score": round(overall_score, 2),
            "skills_match_percentage": round(skills_match_percentage, 2),
            "critical_skills_match_percentage": round(critical_match_percentage, 2),
            "matching_skills": sorted(list(matching_skills)),
            "missing_skills": sorted(list(missing_skills)),
            "missing_critical_skills": sorted(list(missing_critical)),
            "experience_match": experience_match,
            "user_experience_years": user_experience,
            "required_experience_years": required_experience,
            "recommendation": self.get_recommendation(overall_score)
        }
        
        print(f"✅ Overall Match Score: {overall_score:.2f}%")
        print(f"✅ Skills Match: {skills_match_percentage:.2f}%")
        print(f"✅ Missing Skills: {len(missing_skills)}")
        print(f"✅ Recommendation: {match_analysis['recommendation']}\n")
        
        return match_analysis
    
    def get_recommendation(self, score: float) -> str:
        """Get recommendation based on match score"""
        if score >= 80:
            return "🟢 Excellent Match - Apply Now!"
        elif score >= 60:
            return "🟡 Good Match - Build 2-3 missing skills"
        elif score >= 40:
            return "🟠 Fair Match - 30-day roadmap recommended"
        else:
            return "🔴 Consider building foundational skills first"
