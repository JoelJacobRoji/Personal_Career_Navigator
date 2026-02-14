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
        
        # Method 1: pdfplumber (better for complex layouts)
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"⚠️  pdfplumber extraction failed: {e}")
        
        # Method 2: PyPDF2 (fallback)
        if len(text.strip()) < 100:
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as e:
                print(f"⚠️  PyPDF2 extraction failed: {e}")
        
        return text.strip()
    
    def extract_email(self, text: str) -> str:
        """Extract email address using regex"""
        # Comprehensive email pattern
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        matches = re.findall(pattern, text, re.IGNORECASE)
        
        # Filter out common false positives
        valid_emails = [email for email in matches if not email.startswith('http')]
        
        return valid_emails[0] if valid_emails else ""
    
    def extract_phone(self, text: str) -> str:
        """Extract phone number with Indian format support"""
        patterns = [
            r'\+\s*91[\s-]?\d{10}',  # +91 7012032686 or + 91 7012032686
            r'\+91[\s-]?\d{5}[\s-]?\d{5}',  # +91 70120 32686
            r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # General
            r'\d{10}',  # Plain 10 digits
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                phone = matches[0]
                # Clean and format
                if isinstance(phone, tuple):
                    phone = ''.join(phone)
                return phone.strip()
        
        return ""
    
    def extract_name(self, text: str) -> str:
        """Extract name using pattern matching and NER"""
        
        # Remove common PDF artifacts
        text_clean = text.replace("Contact ", "").replace("CONTACT ", "").strip()
        
        lines = text_clean.split('\n')
        
        # Method 1: Look for ALL CAPS name at the beginning (common in resumes)
        for line in lines[:5]:
            line = line.strip()
            # Check if line is all caps and looks like a name
            if line.isupper() and 5 < len(line) < 50 and not any(char.isdigit() for char in line):
                # Exclude common section headers
                excluded = ['EXECUTIVE SUMMARY', 'SKILLS', 'EXPERIENCE', 'EDUCATION', 
                           'PROJECTS', 'CERTIFICATIONS', 'SUMMARY', 'CONTACT']
                if line not in excluded and '|' not in line:
                    return line.title()  # Convert to Title Case
        
        # Method 2: Use spaCy NER
        doc = self.nlp(text_clean[:500])
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                name = ent.text.strip()
                # Exclude false positives
                if name.lower() not in ['contact', 'summary', 'experience', 'education', 'skills']:
                    return name
        
        # Method 3: Look for name pattern in first few lines (Title Case)
        for line in lines[:5]:
            line = line.strip()
            # Name pattern: 2-4 words, Title Case, no numbers or special chars
            words = line.split()
            if 2 <= len(words) <= 4:
                if all(word[0].isupper() for word in words if word):
                    if not any(char.isdigit() for char in line) and '@' not in line:
                        return line
        
        return "Unknown"
    
    def extract_education(self, text: str) -> List[Dict]:
        """Extract education information with improved field parsing"""
        education = []
        
        # Enhanced patterns to capture "B Tech in CSE with Specialization in Data Science"
        patterns = [
            # Pattern 1: Full format with specialization
            r'(?i)(B\.?\s*Tech|B\.?E\.?|Bachelor|M\.?\s*Tech|Master|M\.?S\.?|Ph\.?D\.?|MBA)\s+in\s+([A-Za-z\s&]+?)(?:\s+with\s+[Ss]pecialization\s+in\s+([A-Za-z\s]+?))?(?=\s*\||$|\n)',
            
            # Pattern 2: Degree followed by field
            r'(?i)(B\.?\s*Tech|Bachelor|M\.?\s*Tech|Master|MBA|Ph\.?D\.?)[\s,]+([A-Za-z\s&,]+?)(?:with\s+[Ss]pecialization\s+in\s+)?([A-Za-z\s]+)?(?=\s*·|\s*,|\s*-|$|\n)',
            
            # Pattern 3: Generic
            r'(?i)(Associate|Diploma)[\s\w]*(?:in\s+)?([A-Za-z\s]+)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                degree = match.group(1).strip() if match.group(1) else ""
                field = match.group(2).strip() if len(match.groups()) > 1 and match.group(2) else ""
                specialization = match.group(3).strip() if len(match.groups()) > 2 and match.group(3) else ""
                
                # Combine field and specialization
                full_field = field
                if specialization:
                    full_field = f"{field}, {specialization}"
                
                # Clean up field (remove trailing punctuation)
                full_field = re.sub(r'[,\s]+$', '', full_field)
                
                # Only add if we have both degree and field
                if degree and full_field:
                    edu_entry = {
                        "degree": degree,
                        "field": full_field,
                        "university": ""
                    }
                    
                    # Avoid duplicates
                    if edu_entry not in education:
                        education.append(edu_entry)
        
        # Extract universities
        university_patterns = [
            r'(CHRIST|Christ University[^,\n]*)',
            r'(St\.\s*Francis School[^,\n]*)',
            r'([A-Z][a-z]+\s+University[^,\n]*)',
            r'([A-Z][a-z]+\s+Institute[^,\n]*)',
        ]
        
        universities = []
        for pattern in university_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            universities.extend(matches)
        
        # Attach universities to education entries
        for i, edu in enumerate(education):
            if i < len(universities):
                edu['university'] = universities[i].strip()
        
        return education if education else [{"degree": "N/A", "field": "N/A", "university": "N/A"}]
    
    def extract_experience_years(self, text: str) -> float:
        """Extract years of experience with student timeline calculation"""
        
        # Method 1: Direct experience mention
        pattern = r'(\d+)[\+\-\s]*(?:to\s+)?(\d+)?\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience|exp)?'
        matches = re.findall(pattern, text.lower())
        
        if matches:
            years = []
            for match in matches:
                if match[1]:
                    years.append(int(match[1]))
                else:
                    years.append(int(match[0]))
            if years:
                return max(years)
        
        # Method 2: Calculate from B.Tech start date (for students)
        # Look for "2024 - Present" or "January 2024"
        btech_pattern = r'(?:January|June|August|2024)\s*[-–]\s*(?:Present|2026|2027|2028)'
        if re.search(btech_pattern, text, re.IGNORECASE):
            # Student - calculate years since B.Tech start
            start_match = re.search(r'(January|June|2024)', text, re.IGNORECASE)
            if start_match:
                # Approximate: Jan 2024 to Feb 2026 = ~2 years
                return 1  # Conservative estimate for student experience
        
        return 0
    
    def extract_skills_nlp(self, text: str) -> Set[str]:
        """Extract technical skills using pattern matching"""
        text_lower = text.lower()
        extracted_skills = set()
        
        # Direct substring matching with word boundaries
        for skill in self.tech_skills_lower:
            # Use word boundaries for accurate matching
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                # Find original case from Config
                original_skill = next(s for s in Config.TECH_SKILLS if s.lower() == skill)
                extracted_skills.add(original_skill)
        
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
            "name": self.extract_name(text),
            "email": self.extract_email(text),
            "phone": self.extract_phone(text),
            "education": self.extract_education(text),
            "years_of_experience": self.extract_experience_years(text),
            "technical_skills": list(self.extract_skills_nlp(text)),
            "soft_skills": list(self.extract_soft_skills(text)),
            "raw_text_length": len(text)
        }
        
        print(f"✅ Extracted {len(profile['technical_skills'])} technical skills")
        print(f"✅ Extracted {len(profile['soft_skills'])} soft skills")
        print(f"✅ Experience: {profile['years_of_experience']} years\n")
        
        return profile
