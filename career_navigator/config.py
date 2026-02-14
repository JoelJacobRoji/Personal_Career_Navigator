"""
Configuration for Career Navigator
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration settings"""
    
    # API Credentials
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    
    # Directories
    BASE_DIR = Path(__file__).parent
    OUTPUT_DIR = BASE_DIR / "outputs"
    SAMPLE_DATA_DIR = BASE_DIR / "sample_data"
    DATASETS_DIR = BASE_DIR / "datasets"
    
    # Create directories
    OUTPUT_DIR.mkdir(exist_ok=True)
    SAMPLE_DATA_DIR.mkdir(exist_ok=True)
    DATASETS_DIR.mkdir(exist_ok=True)
    
    # Technical Skills (Comprehensive List)
    TECH_SKILLS = {
        # Programming Languages
        "Python", "JavaScript", "Java", "C++", "C#", "TypeScript", "Go", "Rust",
        "Ruby", "PHP", "Swift", "Kotlin", "R", "Scala", "Perl", "MATLAB", "C",
        
        # Web Technologies
        "React", "Angular", "Vue.js", "Node.js", "Express.js", "Django", "Flask",
        "FastAPI", "Spring Boot", "ASP.NET", "HTML", "CSS", "SASS", "Bootstrap",
        "Tailwind CSS", "Next.js", "Nuxt.js", "Redux", "GraphQL", "REST API",
        
        # Databases
        "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra", "Oracle",
        "SQL Server", "DynamoDB", "Neo4j", "Elasticsearch", "Firebase",
        "Oracle SQL",
        
        # Cloud & DevOps
        "AWS", "Azure", "Google Cloud", "GCP", "Docker", "Kubernetes", "Jenkins",
        "CI/CD", "Terraform", "Ansible", "Git", "GitHub Actions", "GitLab CI",
        "CircleCI", "Prometheus", "Grafana", "ELK Stack", "Datadog",
        
        # Data Science & ML (EXPANDED)
        "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Keras",
        "scikit-learn", "Scikit-learn", "Pandas", "NumPy", "Matplotlib", "Seaborn",
        "NLP", "Natural Language Processing", "Computer Vision", "Neural Networks",
        "XGBoost", "LightGBM", "BERT", "GPT", "Transformers",
        "EDA", "Exploratory Data Analysis", "Data Cleaning", "Data Visualization",
        "Statistics", "Statistical Analysis", "Probability", "Statistical Modeling",
        "Feature Engineering", "Model Deployment", "MLOps",
        
        # Audio/Speech Processing
        "Whisper", "Librosa", "Speech Recognition", "Audio Processing",
        
        # Big Data
        "Apache Spark", "Hadoop", "Kafka", "Airflow", "Databricks", "Snowflake",
        
        # Development Tools
        "VS Code", "Jupyter Notebook", "PyCharm", "IntelliJ IDEA", "Eclipse",
        "Cisco Packet Tracer", "Postman", "Swagger",
        
        # Operating Systems
        "Linux", "Windows", "Ubuntu", "MacOS", "Unix",
        
        # Testing
        "Unit Testing", "Integration Testing", "Selenium", "Jest", "Pytest",
        "JUnit", "Cypress", "Test-Driven Development", "TDD",
        
        # Other
        "Agile", "Scrum", "JIRA", "Confluence", "OOP", "Data Structures",
        "Algorithms", "Design Patterns",
    }
    
    SOFT_SKILLS = {
        "Communication", "Leadership", "Problem Solving", "Problem-Solving",
        "Teamwork", "Team Coordination", "Time Management", "Critical Thinking",
        "Adaptability", "Creativity", "Decision Making", "Collaboration",
        "Presentation Skills", "Interpersonal Skills", "Public Speaking",
        "Research Skills", "Research", "Negotiation", "Project Management",
        "Strategic Planning", "Mentoring", "Analytical Thinking", "Analytical Skills",
    }
