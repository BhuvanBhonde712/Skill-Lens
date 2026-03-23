# data/job_roles.py
# Each job role defines: description, required skills, optional skills,
# experience level, and average salary range (India-based, LPA).

JOB_ROLES = {
    "Software Developer": {
        "description": "Designs, builds, and maintains software systems across full or partial stack.",
        "required_skills": [
            "python", "java", "javascript", "git", "sql",
            "rest api", "agile", "problem solving", "testing"
        ],
        "optional_skills": [
            "docker", "aws", "react", "node.js", "ci/cd",
            "typescript", "redis", "microservices"
        ],
        "experience_level": "Entry to Senior",
        "avg_salary": "6 - 20 LPA"
    },
    "Data Scientist": {
        "description": "Extracts insights from data and builds predictive models to drive business decisions.",
        "required_skills": [
            "python", "machine learning", "pandas", "numpy", "scikit-learn",
            "statistical analysis", "data visualization", "sql", "feature engineering"
        ],
        "optional_skills": [
            "deep learning", "tensorflow", "pytorch", "apache spark",
            "tableau", "r", "nlp", "mlops", "time series"
        ],
        "experience_level": "Mid to Senior",
        "avg_salary": "8 - 25 LPA"
    },
    "Data Analyst": {
        "description": "Interprets structured data and translates it into actionable business insights.",
        "required_skills": [
            "sql", "excel", "data analysis", "data visualization",
            "python", "statistical analysis", "tableau", "power bi"
        ],
        "optional_skills": [
            "r", "machine learning", "etl", "looker", "data pipeline"
        ],
        "experience_level": "Entry to Mid",
        "avg_salary": "4 - 15 LPA"
    },
    "Full Stack Developer": {
        "description": "Owns both client-side and server-side development, from database to UI.",
        "required_skills": [
            "html", "css", "javascript", "react", "node.js",
            "sql", "mongodb", "rest api", "git", "docker"
        ],
        "optional_skills": [
            "typescript", "next.js", "graphql", "aws", "redis",
            "ci/cd", "testing"
        ],
        "experience_level": "Entry to Senior",
        "avg_salary": "6 - 22 LPA"
    },
    "Machine Learning Engineer": {
        "description": "Builds, optimizes, and deploys ML/AI models in production-grade systems.",
        "required_skills": [
            "python", "machine learning", "deep learning", "tensorflow",
            "pytorch", "mlops", "docker", "kubernetes", "rest api",
            "feature engineering", "model deployment"
        ],
        "optional_skills": [
            "apache spark", "aws", "langchain", "llm",
            "rag", "vector database", "embeddings", "airflow"
        ],
        "experience_level": "Mid to Senior",
        "avg_salary": "12 - 35 LPA"
    },
    "DevOps Engineer": {
        "description": "Bridges development and operations by automating infrastructure and deployments.",
        "required_skills": [
            "linux", "docker", "kubernetes", "jenkins", "ci/cd",
            "terraform", "ansible", "aws", "bash", "git"
        ],
        "optional_skills": [
            "python", "nginx", "prometheus", "grafana", "helm",
            "argocd", "datadog"
        ],
        "experience_level": "Mid to Senior",
        "avg_salary": "8 - 25 LPA"
    },
    "Frontend Developer": {
        "description": "Builds high-quality, performant user interfaces and client-side applications.",
        "required_skills": [
            "html", "css", "javascript", "react", "typescript",
            "git", "rest api", "tailwindcss", "webpack"
        ],
        "optional_skills": [
            "next.js", "vue", "angular", "vite", "testing",
            "figma", "redux", "graphql"
        ],
        "experience_level": "Entry to Senior",
        "avg_salary": "5 - 18 LPA"
    },
    "Backend Developer": {
        "description": "Architects and implements server-side business logic, APIs, and data storage.",
        "required_skills": [
            "python", "java", "node.js", "rest api", "sql",
            "mongodb", "docker", "git", "microservices"
        ],
        "optional_skills": [
            "graphql", "redis", "kafka", "rabbitmq", "aws",
            "grpc", "fastapi"
        ],
        "experience_level": "Entry to Senior",
        "avg_salary": "6 - 22 LPA"
    },
    "Cybersecurity Analyst": {
        "description": "Identifies, monitors, and mitigates security risks across systems and networks.",
        "required_skills": [
            "cybersecurity", "network security", "linux", "penetration testing",
            "vulnerability assessment", "firewalls", "siem", "python"
        ],
        "optional_skills": [
            "ethical hacking", "cryptography", "kali linux", "wireshark",
            "metasploit", "owasp", "incident response"
        ],
        "experience_level": "Entry to Senior",
        "avg_salary": "6 - 20 LPA"
    },
    "Mobile App Developer": {
        "description": "Develops native or cross-platform mobile applications for Android and iOS.",
        "required_skills": [
            "flutter", "react native", "android", "ios", "dart",
            "kotlin", "swift", "git", "rest api"
        ],
        "optional_skills": [
            "firebase", "android studio", "xcode",
            "figma", "testing"
        ],
        "experience_level": "Entry to Senior",
        "avg_salary": "5 - 20 LPA"
    },
    "NLP / AI Engineer": {
        "description": "Builds systems that understand, process, and generate natural language using LLMs.",
        "required_skills": [
            "nlp", "python", "transformers", "bert", "spacy",
            "nltk", "machine learning", "deep learning", "pytorch"
        ],
        "optional_skills": [
            "langchain", "llm", "hugging face", "gpt", "rag",
            "vector database", "embeddings", "text mining"
        ],
        "experience_level": "Mid to Senior",
        "avg_salary": "10 - 30 LPA"
    },
    "UI/UX Designer": {
        "description": "Designs user-centered digital experiences grounded in research and prototyping.",
        "required_skills": [
            "figma", "ui/ux", "ux design", "adobe xd",
            "communication", "creativity", "problem solving"
        ],
        "optional_skills": [
            "html", "css", "prototyping", "user research",
            "analytical", "presentation"
        ],
        "experience_level": "Entry to Senior",
        "avg_salary": "4 - 18 LPA"
    }
}