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
    
    # Technical Skills (Top 100+ shown - expand as needed)
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
        "SQL Server", "DynamoDB", "Neo4j", "Elasticsearch", "Firebase", "Oracle SQL",
        
        # Cloud & DevOps
        "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Jenkins",
        "CI/CD", "Terraform", "Ansible", "Git", "GitHub Actions", "GitLab CI",
        "CircleCI", "Prometheus", "Grafana", "ELK Stack", "Datadog", "Ubuntu",
        
        # Data Science & ML
        "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Keras",
        "scikit-learn", "Pandas", "NumPy", "Matplotlib", "Seaborn", "NLP",
        "Computer Vision", "Neural Networks", "XGBoost", "LightGBM", "BERT", "EDA", "Probability",
        
        # Big Data
        "Apache Spark", "Hadoop", "Kafka", "Airflow", "Databricks", "Snowflake",
        
        # Testing
        "Unit Testing", "Integration Testing", "Selenium", "Jest", "Pytest",
        "JUnit", "Cypress", "Test-Driven Development",
        
        # Other technical skills
        "Data Structures", "OOP"
    }
    
    SOFT_SKILLS = {
        "Communication", "Leadership", "Problem Solving", "Teamwork",
        "Time Management", "Critical Thinking", "Adaptability", "Creativity",
        "Decision Making", "Collaboration", "Presentation Skills"
    }
