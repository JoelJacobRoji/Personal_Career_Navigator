"""
Personal Career Navigator - Phase 1
Complete Profile Analysis with 4 Inputs:
1. Resume PDF
2. GitHub Username  
3. LinkedIn PDF
4. Dream Job Description
"""

import json
from pathlib import Path
from typing import Dict, Any

# Import all modules
from parsers.resume_parser import ResumeParser
from parsers.linkedin_parser import LinkedInParser
from parsers.github_analyzer import GitHubAnalyzer
from analyzers.job_matcher import JobMatcher
from config import Config


class CareerNavigator:
    """Main orchestrator for Career Navigator Phase 1"""
    
    def __init__(self):
        print("=" * 80)
        print("  🚀 PERSONAL CAREER NAVIGATOR - PHASE 1")
        print("  AI-Powered Career Analysis & Job Matching System")
        print("=" * 80)
        print()
        
        # Initialize all components
        self.resume_parser = ResumeParser()
        self.linkedin_parser = LinkedInParser()
        self.github_analyzer = GitHubAnalyzer()
        self.job_matcher = JobMatcher()
    
    def merge_profiles(self, resume_data: Dict, github_data: Dict, 
                       linkedin_data: Dict) -> Dict[str, Any]:
        """Merge data from all sources"""
        
        # Combine all technical skills
        all_skills = set()
        if resume_data.get("technical_skills"):
            all_skills.update(resume_data["technical_skills"])
        if github_data.get("skills_from_repos"):
            all_skills.update(github_data["skills_from_repos"])
        if linkedin_data.get("skills"):
            all_skills.update(linkedin_data["skills"])
        
        # Get best name (priority: LinkedIn > Resume > GitHub)
        name = (linkedin_data.get("name") or 
                resume_data.get("name") or 
                github_data.get("name") or 
                "Unknown")
        
        # Unified profile
        unified = {
            "personal_info": {
                "name": name,
                "email": resume_data.get("email", ""),
                "phone": resume_data.get("phone", ""),
                "location": (linkedin_data.get("location") or 
                            github_data.get("location") or ""),
                "headline": linkedin_data.get("headline", ""),
                "current_role": linkedin_data.get("current_role", ""),
                "current_company": linkedin_data.get("current_company", "")
            },
            "experience": {
                "years": max(
                    resume_data.get("years_of_experience", 0),
                    self._calculate_linkedin_experience(linkedin_data)
                ),
                "github_repos": github_data.get("public_repos", 0),
                "github_commits": github_data.get("activity", {}).get("total_commits", 0),
                "github_stars": github_data.get("activity", {}).get("total_stars", 0)
            },
            "skills": {
                "technical_skills": sorted(list(all_skills)),
                "programming_languages": github_data.get("languages", {}),
                "soft_skills": resume_data.get("soft_skills", []),
                "total_technical_skills": len(all_skills)
            },
            "education": (linkedin_data.get("education") or 
                         resume_data.get("education", [])),
            "certifications": linkedin_data.get("certifications", []),
            "github_profile": {
                "username": github_data.get("username", ""),
                "url": github_data.get("profile_url", ""),
                "top_repos": github_data.get("top_repositories", [])
            },
            "data_sources": {
                "resume": bool(resume_data),
                "github": bool(github_data),
                "linkedin": bool(linkedin_data)
            }
        }
        
        return unified
    
    def _calculate_linkedin_experience(self, linkedin_data: Dict) -> float:
        """Calculate years of experience from LinkedIn duration"""
        duration = linkedin_data.get("duration", "")
        if not duration:
            return 0
        
        # Parse duration like "Jan 2020 - Present" or "Jan 2020 - Dec 2023"
        import re
        match = re.search(r'(\d{4}).*?(?:Present|(\d{4}))', duration)
        if match:
            start_year = int(match.group(1))
            end_year = int(match.group(2)) if match.group(2) else 2026
            return end_year - start_year
        return 0
    
    def run(self, resume_path: str = None, github_username: str = None,
            linkedin_path: str = None, dream_job: str = None) -> Dict[str, Any]:
        """
        Run complete Career Navigator analysis
        
        Args:
            resume_path: Path to resume PDF
            github_username: GitHub username
            linkedin_path: Path to LinkedIn PDF export
            dream_job: Dream job description or title
        """
        
        print("\n" + "=" * 80)
        print("📊 STARTING COMPREHENSIVE CAREER ANALYSIS")
        print("=" * 80 + "\n")
        
        results = {}
        
        # STEP 1: Parse Resume
        print("STEP 1/4: Resume Analysis")
        print("-" * 80)
        if resume_path and Path(resume_path).exists():
            results["resume"] = self.resume_parser.parse_resume(resume_path)
        else:
            print("⚠️  No resume provided\n")
            results["resume"] = {}
        
        # STEP 2: Analyze GitHub
        print("STEP 2/4: GitHub Profile Analysis")
        print("-" * 80)
        if github_username:
            results["github"] = self.github_analyzer.analyze_profile(github_username)
        else:
            print("⚠️  No GitHub username provided\n")
            results["github"] = {}
        
        # STEP 3: Parse LinkedIn PDF
        print("STEP 3/4: LinkedIn Profile Analysis")
        print("-" * 80)
        if linkedin_path and Path(linkedin_path).exists():
            results["linkedin"] = self.linkedin_parser.parse_linkedin_pdf(linkedin_path)
        else:
            print("⚠️  No LinkedIn PDF provided\n")
            results["linkedin"] = {}
        
        # Merge profiles
        print("=" * 80)
        print("🔗 MERGING PROFILE DATA FROM ALL SOURCES")
        print("=" * 80 + "\n")
        
        unified_profile = self.merge_profiles(
            results["resume"],
            results["github"],
            results["linkedin"]
        )
        
        # Save unified profile
        profile_output = Config.OUTPUT_DIR / "extracted_profile.json"
        with open(profile_output, 'w', encoding='utf-8') as f:
            json.dump(unified_profile, f, indent=2, ensure_ascii=False)
        print(f"✅ Unified profile saved: {profile_output}\n")
        
        # STEP 4: Analyze Dream Job & Match
        print("STEP 4/4: Dream Job Analysis & Matching")
        print("-" * 80)
        
        job_analysis = None
        if dream_job:
            job_requirements = self.job_matcher.extract_job_requirements(dream_job)
            match_results = self.job_matcher.calculate_match_score(
                unified_profile, 
                job_requirements
            )
            
            job_analysis = {
                "job_requirements": job_requirements,
                "match_analysis": match_results
            }
            
            # Save job match analysis
            job_output = Config.OUTPUT_DIR / "job_match_analysis.json"
            with open(job_output, 'w', encoding='utf-8') as f:
                json.dump(job_analysis, f, indent=2, ensure_ascii=False)
            print(f"✅ Job match analysis saved: {job_output}\n")
        else:
            print("⚠️  No dream job description provided\n")
        
        # Print comprehensive summary
        self.print_summary(unified_profile, job_analysis)
        
        return {
            "profile": unified_profile,
            "job_analysis": job_analysis
        }
    
    def print_summary(self, profile: Dict, job_analysis: Dict = None):
        """Print comprehensive analysis summary"""
        print("\n" + "=" * 80)
        print("📈 COMPREHENSIVE CAREER ANALYSIS SUMMARY")
        print("=" * 80)
        # Personal Info
        print(f"\n👤 PERSONAL INFORMATION")
        print(f"   Name: {profile['personal_info']['name']}")
        print(f"   Email: {profile['personal_info']['email']}")
        print(f"   Phone: {profile['personal_info'].get('phone', '')}")  # Added phone
        print(f"   Location: {profile['personal_info']['location']}")
        print(f"   Current Role: {profile['personal_info']['current_role']}")
        print(f"   Company: {profile['personal_info']['current_company']}")
        # Experience
        print(f"\n💼 EXPERIENCE")
        print(f"   Years: {profile['experience']['years']}")
        print(f"   GitHub Repos: {profile['experience']['github_repos']}")
        print(f"   GitHub Commits: {profile['experience']['github_commits']}")
        print(f"   GitHub Stars: {profile['experience']['github_stars']}")
        # Skills
        print(f"\n🛠️  SKILLS PORTFOLIO")
        print(f"   Total Technical Skills: {profile['skills']['total_technical_skills']}")
        print(f"   Programming Languages: {len(profile['skills']['programming_languages'])}")
        print(f"   Soft Skills: {len(profile['skills']['soft_skills'])}")
        print(f"\n   Top 10 Technical Skills:")
        for i, skill in enumerate(profile['skills']['technical_skills'][:10], 1):
            print(f"      {i}. {skill}")
        if profile['skills']['soft_skills']:
            print(f"\n   Soft Skills:")
            for skill in profile['skills']['soft_skills']:
                print(f"      • {skill}")
        if profile['skills']['programming_languages']:
            print(f"\n   Programming Language Proficiency:")
            for lang, pct in list(profile['skills']['programming_languages'].items())[:5]:
                print(f"      • {lang}: {pct}%")
        # Education
        if profile.get('education'):
            print(f"\n🎓 EDUCATION")
            for edu in profile['education']:
                if isinstance(edu, dict):
                    degree = edu.get('degree', 'N/A')
                    field = edu.get('field', 'N/A')
                    university = edu.get('university', '')
                    if degree != 'N/A' or field != 'N/A':
                        print(f"   • {degree} in {field}")
                        if university:
                            print(f"     {university}")
        # Certifications
        if profile.get('certifications') and len(profile['certifications']) > 0:
            print(f"\n📜 CERTIFICATIONS ({len(profile['certifications'])})")
            for cert in profile['certifications'][:5]:
                print(f"   • {cert}")
        # Job Match Analysis
        if job_analysis:
            print(f"\n" + "=" * 80)
            print(f"🎯 DREAM JOB MATCH ANALYSIS")
            print("=" * 80)
            job_req = job_analysis['job_requirements']
            match = job_analysis['match_analysis']
            print(f"\n📋 Target Position: {job_req['job_title']}")
            print(f"   Required Skills: {job_req['total_skills_required']}")
            print(f"   Experience Required: {job_req['years_experience_required']} years")
            print(f"\n📊 MATCH SCORE: {match['overall_match_score']}%")
            print(f"   {match['recommendation']}")
            print(f"\n✅ Matching Skills ({len(match['matching_skills'])}):")
            for skill in match['matching_skills'][:10]:
                print(f"      • {skill}")
            if match['missing_skills']:
                print(f"\n❌ Missing Skills ({len(match['missing_skills'])}):")
                for skill in match['missing_skills'][:10]:
                    print(f"      • {skill}")
            if match['missing_critical_skills']:
                print(f"\n🔴 CRITICAL Missing Skills (Priority):")
                for skill in match['missing_critical_skills']:
                    print(f"      • {skill}")
        print("\n" + "=" * 80 + "\n")
        print("\n" + "=" * 80 + "\n")
    
    # Collect inputs
    print("Please provide the following inputs (press Enter to skip):\n")
    
    resume_path = input("1️⃣  Resume PDF path: ").strip()
    github_username = input("2️⃣  GitHub username: ").strip()
    linkedin_path = input("3️⃣  LinkedIn PDF path: ").strip()
    
    print("\n4️⃣  Dream Job Description (paste full job description or job title):")
    print("   (Type or paste, then press Enter twice to finish)\n")
    
    dream_job_lines = []
    while True:
        line = input()
        if line == "" and dream_job_lines and dream_job_lines[-1] == "":
            break
        dream_job_lines.append(line)
    
    dream_job = "\n".join(dream_job_lines).strip()
    
    # Run analysis

def main():
    navigator = CareerNavigator()

    print("Please provide the following inputs (press Enter to skip):\n")
    resume_path = input("1️⃣  Resume PDF path: ").strip()
    github_username = input("2️⃣  GitHub username: ").strip()
    linkedin_path = input("3️⃣  LinkedIn PDF path: ").strip()

    print("\n4️⃣  Dream Job Description (paste full job description or job title):")
    print("   (Type or paste, then press Enter twice to finish)\n")
    dream_job_lines = []
    while True:
        line = input()
        if line == "" and dream_job_lines and dream_job_lines[-1] == "":
            break
        dream_job_lines.append(line)
    dream_job = "\n".join(dream_job_lines).strip()

    # Run analysis
    results = navigator.run(
        resume_path=resume_path if resume_path else None,
        github_username=github_username if github_username else None,
        linkedin_path=linkedin_path if linkedin_path else None,
        dream_job=dream_job if dream_job else None
    )

    print("\n✅ Analysis complete! Check 'outputs/' folder for detailed results.")


if __name__ == "__main__":
    main()
