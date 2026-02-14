"""
LinkedIn Parser - Extract information from LinkedIn PDF exports
"""

import re
import PyPDF2
import pdfplumber
from typing import Dict, List, Set, Any
from pathlib import Path

import spacy

# Import config
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import Config


class LinkedInParser:
    """Parse LinkedIn profile PDF exports"""
    
    def __init__(self):
        print("🔧 Initializing LinkedIn Parser...")
        
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_lg")
            print("✅ LinkedIn Parser initialized\n")
        except Exception as e:
            print(f"❌ Error loading spaCy: {e}")
            raise
        
        self.tech_skills_lower = {skill.lower() for skill in Config.TECH_SKILLS}
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from LinkedIn PDF"""
        text = ""
        
        # Use pdfplumber (works better with LinkedIn PDFs)
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"⚠️  pdfplumber failed: {e}")
            
            # Fallback to PyPDF2
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as e2:
                print(f"❌ PyPDF2 also failed: {e2}")
        
        return text.strip()
    
    def extract_profile_section(self, text: str, section_name: str) -> str:
        """Extract specific section from LinkedIn PDF"""
        # LinkedIn PDFs have section headers like "Experience", "Education", "Skills"
        pattern = rf'{section_name}\s*\n(.*?)(?:\n[A-Z][a-z]+\s*\n|$)'
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""
    
    def extract_name(self, text: str) -> str:
        """Extract name from LinkedIn PDF (usually at top)"""
        lines = text.split('\n')
        # Name is typically in first few lines
        for line in lines[:5]:
            line = line.strip()
            if len(line) > 3 and len(line) < 50 and not any(char.isdigit() for char in line):
                # Check if it looks like a name (Title Case, no special chars)
                if line[0].isupper() and not any(x in line.lower() for x in ['http', 'www', '@']):
                    return line
        return "Unknown"
    
    def extract_headline(self, text: str) -> str:
        """Extract LinkedIn headline (appears after name)"""
        lines = text.split('\n')
        # Headline usually follows name within first 10 lines
        for i, line in enumerate(lines[:10]):
            if any(keyword in line.lower() for keyword in ['engineer', 'developer', 'analyst', 'manager', 'specialist', 'consultant']):
                return line.strip()
        return ""
    
    def extract_location(self, text: str) -> str:
        """Extract location"""
        # Pattern: City, State/Country or City, Country
        pattern = r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)*,\s[A-Z][a-z]+(?:\s[A-Z][a-z]+)*)'
        matches = re.findall(pattern, text)
        return matches[0] if matches else ""
    
    def extract_current_position(self, text: str) -> Dict[str, str]:
        """Extract current job position"""
        experience_section = self.extract_profile_section(text, "Experience")
        
        if not experience_section:
            return {"title": "", "company": "", "duration": ""}
        
        lines = experience_section.split('\n')
        
        # First position is usually current
        position = {
            "title": lines[0].strip() if len(lines) > 0 else "",
            "company": lines[1].strip() if len(lines) > 1 else "",
            "duration": ""
        }
        
        # Extract duration
        duration_pattern = r'(\w+ \d{4} - (?:Present|\w+ \d{4}))'
        duration_match = re.search(duration_pattern, experience_section)
        if duration_match:
            position["duration"] = duration_match.group(1)
        
        return position
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from LinkedIn PDF"""
        skills_section = self.extract_profile_section(text, "Skills")
        
        extracted_skills = set()
        
        # If dedicated skills section exists
        if skills_section:
            for skill in self.tech_skills_lower:
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, skills_section.lower()):
                    original_skill = next(s for s in Config.TECH_SKILLS if s.lower() == skill)
                    extracted_skills.add(original_skill)
        
        # Also search entire document
        text_lower = text.lower()
        for skill in self.tech_skills_lower:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                original_skill = next(s for s in Config.TECH_SKILLS if s.lower() == skill)
                extracted_skills.add(original_skill)
        
        return sorted(list(extracted_skills))
    
    def extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        cert_section = self.extract_profile_section(text, "Licenses & Certifications")
        
        if not cert_section:
            cert_section = self.extract_profile_section(text, "Certifications")
        
        certifications = []
        if cert_section:
            lines = cert_section.split('\n')
            for line in lines:
                line = line.strip()
                if line and len(line) > 5 and not line.isdigit():
                    certifications.append(line)
        
        return certifications
    
    def extract_education(self, text: str) -> List[Dict]:
        """Extract education details"""
        edu_section = self.extract_profile_section(text, "Education")
        
        education = []
        
        if edu_section:
            # Split by university (lines with common university patterns)
            lines = edu_section.split('\n')
            current_edu = {}
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Check if it's a degree line
                if any(deg in line for deg in ['Bachelor', 'Master', 'PhD', 'B.Tech', 'M.Tech', 'MBA', 'B.S', 'M.S']):
                    if current_edu:
                        education.append(current_edu)
                    current_edu = {"degree": line, "university": "", "year": ""}
                
                # Check if it's a university line (usually has "University" or "Institute")
                elif any(inst in line for inst in ['University', 'Institute', 'College', 'School']):
                    if current_edu:
                        current_edu["university"] = line
                
                # Check if it's a year
                elif re.search(r'\d{4}', line):
                    if current_edu:
                        current_edu["year"] = line
            
            if current_edu:
                education.append(current_edu)
        
        return education
    
    def parse_linkedin_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Main function to parse LinkedIn PDF"""
        print(f"📄 Parsing LinkedIn PDF: {pdf_path}")
        
        if not Path(pdf_path).exists():
            print(f"❌ File not found: {pdf_path}")
            return {}
        
        # Extract text
        text = self.extract_text_from_pdf(pdf_path)
        
        if not text or len(text) < 100:
            print("❌ Insufficient text extracted from LinkedIn PDF")
            return {}
        
        # Extract all information
        current_position = self.extract_current_position(text)
        
        profile = {
            "name": self.extract_name(text),
            "headline": self.extract_headline(text),
            "location": self.extract_location(text),
            "current_role": current_position.get("title", ""),
            "current_company": current_position.get("company", ""),
            "duration": current_position.get("duration", ""),
            "skills": self.extract_skills(text),
            "certifications": self.extract_certifications(text),
            "education": self.extract_education(text),
            "raw_text_length": len(text)
        }
        
        print(f"✅ Extracted {len(profile['skills'])} skills")
        print(f"✅ Extracted {len(profile['certifications'])} certifications")
        print(f"✅ Current Role: {profile['current_role']}\n")
        
        return profile
