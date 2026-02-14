"""
Resume Parser - Extract skills and information from resume PDFs
"""

import re
import PyPDF2
import pdfplumber
from typing import Dict, List, Set, Any
from pathlib import Path

import spacy
from nltk.corpus import stopwords

# Import config
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import Config


class ResumeParser:
    """Extract skills and information from resumes using NLP"""
    
    def __init__(self):
        print("🔧 Initializing Resume Parser...")
        
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_lg")
            print("✅ spaCy model loaded successfully")
        except Exception as e:
            print(f"❌ Error loading spaCy: {e}")
            print("Run: python -m spacy download en_core_web_lg")
            raise
        
        # Load stopwords
        self.stop_words = set(stopwords.words('english'))
        
        # Skill patterns (lowercase for matching)
        self.tech_skills_lower = {skill.lower() for skill in Config.TECH_SKILLS}
        self.soft_skills_lower = {skill.lower() for skill in Config.SOFT_SKILLS}
        
        print("✅ Resume Parser initialized\n")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF file using multiple methods"""
        text = ""
        
        # Method 1: PyPDF2
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"⚠️  PyPDF2 extraction failed: {e}")
        
        # Method 2: pdfplumber (better for complex layouts)
        if len(text.strip()) < 100:  # If PyPDF2 didn't work well
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text() + "\n"
            except Exception as e:
                print(f"⚠️  pdfplumber extraction failed: {e}")
        
        return text.strip()
    
    def extract_email(self, text: str) -> str:
        """Extract email address using regex"""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(pattern, text)
        return matches[0] if matches else ""
    
    def extract_phone(self, text: str) -> str:
        """Extract phone number"""
        patterns = [
            r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\+?\d{10,13}'
        ]
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0] if isinstance(matches[0], str) else ''.join(matches[0])
        return ""
    
    def extract_name(self, text: str) -> str:
        """Extract name from top of resume"""
        first_lines = text.strip().split('\n')[:5]
        
        for line in first_lines:
            clean = line.strip()
            if len(clean.split()) >= 2 and clean.isupper():
                return clean.title()
        
        return "Unknown"
    
    def extract_education(self, text: str) -> List[Dict]:
        """Extract education section more cleanly"""
        education = []
        
        education_section = re.search(
            r'Education(.*?)(Certifications|Projects|Experience)',
            text,
            re.DOTALL | re.IGNORECASE
        )
        
        if education_section:
            section_text = education_section.group(1)
            lines = section_text.split('\n')
            
            for line in lines:
                clean_line = line.strip()
                if len(clean_line) > 10:
                    education.append({"details": clean_line})
        
        return education
        
        return education
    
    def extract_experience_years(self, text: str) -> float:
        """Estimate years of experience from Experience section only"""
        
        experience_section = re.search(
            r'Experience(.*?)(Projects|Education|Certifications)',
            text,
            re.DOTALL | re.IGNORECASE
        )
        
        if not experience_section:
            return 0
        
        section_text = experience_section.group(1)
        years = re.findall(r'(20\d{2})', section_text)
        
        if not years:
            return 0
        
        years = sorted(set(map(int, years)))
        
        return max(years) - min(years) if len(years) > 1 else 1
    
    def extract_skills_nlp(self, text: str) -> Set[str]:
        """Extract skills using safer matching"""
        text_lower = text.lower()
        extracted_skills = set()
        
        for skill in Config.TECH_SKILLS:
            skill_lower = skill.lower()
            
            # Special handling for very short skills like "C", "R"
            if len(skill_lower) <= 2:
                pattern = r'\b' + re.escape(skill_lower) + r'\b'
                if re.search(pattern, text_lower):
                    extracted_skills.add(skill)
            else:
                if skill_lower in text_lower:
                    extracted_skills.add(skill)
        
        return extracted_skills
    
    def extract_soft_skills(self, text: str) -> Set[str]:
        """Extract soft skills"""
        text_lower = text.lower()
        extracted_soft_skills = set()
        
        for skill in self.soft_skills_lower:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                original_skill = next(s for s in Config.SOFT_SKILLS if s.lower() == skill)
                extracted_soft_skills.add(original_skill)
        
        return extracted_soft_skills
    
    def parse_resume(self, file_path: str) -> Dict[str, Any]:
        """Main function to parse resume and extract all information"""
        print(f"📄 Parsing resume: {file_path}")
        
        if not Path(file_path).exists():
            print(f"❌ File not found: {file_path}")
            return {}
        
        # Extract text
        text = self.extract_text_from_pdf(file_path)
        
        if not text or len(text) < 50:
            print("❌ Insufficient text extracted from PDF")
            return {}
        
        # Extract all information
        profile = {
            "personal_info": {
                "name": self.extract_name(text),
                "email": self.extract_email(text),
                "phone": self.extract_phone(text),
            },
            "education": self.extract_education(text),
            "experience": {
                "years": self.extract_experience_years(text)
            },
            "skills": {
                "technical_skills": list(self.extract_skills_nlp(text)),
                "soft_skills": list(self.extract_soft_skills(text))
            },
            "raw_text_length": len(text)
        }

        print(f"✅ Extracted {len(profile['skills']['technical_skills'])} technical skills")
        print(f"✅ Extracted {len(profile['skills']['soft_skills'])} soft skills")
        print(f"✅ Experience: {profile['experience']['years']} years\n")

        return profile
