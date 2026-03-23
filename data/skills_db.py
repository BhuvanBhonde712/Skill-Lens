# data/skills_db.py
# Comprehensive skills database organized by category.
# Each category maps to a list of lowercase skill keywords used for matching.

SKILLS_DB = {
    "Programming Languages": [
        "python", "java", "javascript", "typescript", "c", "c++", "c#", "go",
        "rust", "swift", "kotlin", "r", "scala", "php", "ruby", "matlab",
        "julia", "perl", "bash", "shell", "powershell", "dart", "haskell",
        "elixir", "lua", "groovy", "cobol", "assembly"
    ],
    "Web - Frontend": [
        "html", "css", "react", "angular", "vue", "vue.js", "react.js",
        "next.js", "nuxt.js", "svelte", "jquery", "bootstrap", "tailwind",
        "tailwindcss", "sass", "less", "webpack", "vite", "redux",
        "graphql", "ajax", "gatsby", "remix"
    ],
    "Web - Backend": [
        "node.js", "express", "django", "flask", "fastapi", "spring",
        "spring boot", "laravel", "rails", "ruby on rails", "asp.net",
        ".net", "nestjs", "hapi", "koa", "gin", "fiber", "actix",
        "rest api", "restful", "microservices", "websocket"
    ],
    "Data Science & Analytics": [
        "pandas", "numpy", "scipy", "matplotlib", "seaborn", "plotly",
        "data analysis", "data visualization", "statistical analysis",
        "excel", "tableau", "power bi", "looker", "data wrangling",
        "feature engineering", "eda", "exploratory data analysis",
        "jupyter", "spss", "sas", "etl", "data pipeline", "apache spark",
        "hadoop", "hive", "data mining"
    ],
    "Machine Learning & AI": [
        "machine learning", "deep learning", "neural networks",
        "scikit-learn", "sklearn", "tensorflow", "keras", "pytorch",
        "xgboost", "lightgbm", "catboost", "nlp", "natural language processing",
        "computer vision", "opencv", "transformers", "hugging face",
        "langchain", "llm", "generative ai", "reinforcement learning",
        "random forest", "svm", "support vector machine", "regression",
        "classification", "clustering", "pca", "dimensionality reduction",
        "time series", "forecasting", "recommendation system", "bert",
        "gpt", "word2vec", "spacy", "nltk", "text mining", "mlops",
        "model deployment", "rag", "vector database", "embeddings"
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
        "terraform", "ansible", "jenkins", "ci/cd", "github actions",
        "gitlab ci", "heroku", "vercel", "netlify", "linux", "unix",
        "nginx", "apache", "serverless", "lambda", "ec2", "s3", "rds",
        "devops", "sre", "cloud computing", "helm", "argocd", "prometheus",
        "grafana", "datadog"
    ],
    "Databases": [
        "sql", "mysql", "postgresql", "sqlite", "mongodb", "redis",
        "elasticsearch", "cassandra", "dynamodb", "oracle", "firebase",
        "supabase", "prisma", "sequelize", "mongoose", "nosql",
        "database design", "query optimization", "stored procedures",
        "neo4j", "couchdb", "influxdb"
    ],
    "Mobile Development": [
        "android", "ios", "react native", "flutter", "swift", "kotlin",
        "xamarin", "ionic", "cordova", "objective-c", "mobile development",
        "android studio", "xcode"
    ],
    "Cybersecurity": [
        "cybersecurity", "penetration testing", "ethical hacking",
        "network security", "cryptography", "siem", "soc", "firewalls",
        "vulnerability assessment", "burp suite", "metasploit", "kali linux",
        "owasp", "security auditing", "wireshark", "nmap", "zero trust",
        "incident response"
    ],
    "Tools & Workflow": [
        "git", "github", "gitlab", "bitbucket", "jira", "confluence",
        "trello", "agile", "scrum", "kanban", "project management",
        "figma", "adobe xd", "ui/ux", "ux design", "postman", "swagger",
        "vs code", "intellij", "testing", "tdd", "bdd", "documentation",
        "code review"
    ],
    "Soft Skills": [
        "communication", "leadership", "teamwork", "problem solving",
        "critical thinking", "time management", "adaptability",
        "creativity", "collaboration", "presentation", "analytical",
        "research", "mentoring", "coaching", "negotiation"
    ]
}

# Flattened deduplicated list of all skills for quick lookup
ALL_SKILLS = list({skill for skills in SKILLS_DB.values() for skill in skills})