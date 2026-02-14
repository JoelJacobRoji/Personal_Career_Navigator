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
        # LinkedIn PDFs have section headers
        pattern = rf'{section_name}\s*\n(.*?)(?:\n[A-Z][a-z]+\s*\n|$)'
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""
    
    def extract_name(self, text: str) -> str:
        """Extract name from LinkedIn PDF"""
        lines = text.split('\n')
        # Name is typically in first few lines
        for line in lines[:5]:
            line = line.strip()
            # Clean up "Contact" prefix if present
            line = line.replace("Contact ", "").replace("CONTACT ", "")
            
            if len(line) > 3 and len(line) < 50 and not any(char.isdigit() for char in line):
                if line[0].isupper() and not any(x in line.lower() for x in ['http', 'www', '@', '|']):
                    # Exclude common headers
                    if line not in ['Summary', 'Experience', 'Education', 'Skills']:
                        return line
        return "Unknown"
    
    def extract_headline(self, text: str) -> str:
        """Extract LinkedIn headline"""
        lines = text.split('\n')
        for i, line in enumerate(lines[:15]):
            if any(keyword in line for keyword in ['engineer', 'developer', 'analyst', 'manager', 'scientist', 'specialist']):
                return line.strip()
        return ""
    
    def extract_location(self, text: str) -> str:
        """Extract location"""
        pattern = r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)*,\s[A-Z][a-z]+(?:\s[A-Z][a-z]+)*)'
        matches = re.findall(pattern, text)
        
        # Filter for actual locations (cities/states)
        for match in matches:
            if any(place in match for place in ['India', 'Karnataka', 'Bengaluru', 'Bangalore', 'Delhi', 'Mumbai']):
                return match
        
        return matches[0] if matches else ""
    
    def extract_current_position(self, text: str) -> Dict[str, str]:
        """Extract current job position (filter out awards/certifications)"""
        experience_section = self.extract_profile_section(text, "Experience")
        
        if not experience_section:
            return {"title": "", "company": "", "duration": ""}
        
        lines = [line.strip() for line in experience_section.split('\n') if line.strip()]
        
        # Find lines with "Present" (current position)
        for i, line in enumerate(lines):
            if "Present" in line or "present" in line:
                # Look backwards for job title and company
                title = ""
                company = ""
                
                # Typical format: Company, then Title, then Duration
                if i >= 2:
                    company = lines[i - 2]
                    title = lines[i - 1]
                elif i >= 1:
                    title = lines[i - 1]
                
                # Filter out certifications/courses/awards
                excluded_keywords = ['Course', 'Certification', 'Hackathon', 'Award', 
                                   'Certificate', 'Challenge', 'Workshop']
                
                if not any(keyword in title for keyword in excluded_keywords):
                    return {
                        "title": title,
                        "company": company,
                        "duration": line
                    }
        
        # Fallback: Get first non-certification entry
        for i in range(0, min(len(lines), 10), 3):
            if i + 1 < len(lines):
                potential_company = lines[i]
                potential_title = lines[i + 1]
                
                # Check if it's a real job (not certification)
                excluded = ['Course', 'Certification', 'Hackathon', 'Award', 'Certificate']
                if not any(keyword in potential_title for keyword in excluded):
                    # Check if company name looks valid
                    if any(keyword in potential_company for keyword in ['AIESEC', 'IIIC', 'CAPS', 'IEEE', 'University']):
                        return {
                            "title": potential_title,
                            "company": potential_company,
                            "duration": lines[i + 2] if i + 2 < len(lines) else ""
                        }
        
        return {"title": "", "company": "", "duration": ""}
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from entire LinkedIn PDF"""
        extracted_skills = set()
        text_lower = text.lower()
        
        # Method 1: Skills section
        skills_section = self.extract_profile_section(text, "Skills")
        if not skills_section:
            skills_section = self.extract_profile_section(text, "Top Skills")
        
        if skills_section:
            for skill in self.tech_skills_lower:
                if skill in skills_section.lower():
                    original_skill = next(s for s in Config.TECH_SKILLS if s.lower() == skill)
                    extracted_skills.add(original_skill)
        
        # Method 2: Certifications section (often contains technology names)
        cert_section = self.extract_profile_section(text, "Certifications")
        if not cert_section:
            cert_section = self.extract_profile_section(text, "Licenses & Certifications")
        
        if cert_section:
            for skill in self.tech_skills_lower:
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, cert_section.lower()):
                    original_skill = next(s for s in Config.TECH_SKILLS if s.lower() == skill)
                    extracted_skills.add(original_skill)
        
        # Method 3: Summary section
        summary = self.extract_profile_section(text, "Summary")
        if summary:
            for skill in self.tech_skills_lower:
                if skill in summary.lower():
                    original_skill = next(s for s in Config.TECH_SKILLS if s.lower() == skill)
                    extracted_skills.add(original_skill)
        
        # Method 4: Search entire document
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
                # Valid certification: not empty, not too short, not just a company name
                if line and len(line) > 5:
                    # Exclude company names that appear alone
                    if not line in ['Amazon Web Services (AWS)', 'Google Cloud', 'Microsoft']:
                        certifications.append(line)
        
        return certifications
    
    def extract_education(self, text: str) -> List[Dict]:
        """Extract education details"""
        edu_section = self.extract_profile_section(text, "Education")
        
        education = []
        
        if edu_section:
            lines = [line.strip() for line in edu_section.split('\n') if line.strip()]
            
            i = 0
            while i < len(lines):
                line = lines[i]
                
                # Check if it's a university/school name
                if any(keyword in line for keyword in ['University', 'Institute', 'College', 'School']):
                    current_edu = {
                        "university": line,
                        "degree": "",
                        "field": "",
                        "year": ""
                    }
                    
                    # Look ahead for degree
                    if i + 1 < len(lines):
                        next_line = lines[i + 1]
                        
                        # Check if it's a degree line
                        degree_match = re.search(
                            r'(B\.?\s*Tech|B\.?E\.?|Bachelor|Master|M\.?\s*Tech|MBA|PhD)(?:\s+in\s+)?([A-Za-z\s,&]+?)(?:\s*·|$)',
                            next_line,
                            re.IGNORECASE
                        )
                        
                        if degree_match:
                            current_edu["degree"] = degree_match.group(1).strip()
                            current_edu["field"] = degree_match.group(2).strip() if len(degree_match.groups()) > 1 else ""
                            i += 1
                            
                            # Look for year
                            if i + 1 < len(lines):
                                year_line = lines[i + 1]
                                if re.search(r'\d{4}', year_line):
                                    current_edu["year"] = year_line
                                    i += 1
                    
                    if current_edu["degree"] or current_edu["field"]:
                        education.append(current_edu)
                
                i += 1
        
        return education if education else [{"university": "N/A", "degree": "N/A", "field": "N/A", "year": "N/A"}]
    
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
