 # SkillLens — AI Resume Intelligence Platform

## Overview

SkillLens is an AI-powered resume analysis platform designed to help students and professionals evaluate their career readiness through intelligent resume understanding. The system applies Natural Language Processing techniques to extract technical skills, assess resume quality using a multi-criteria scoring framework, and recommend suitable job roles based on industry-aligned skill requirements.

The platform transforms unstructured resume content into structured career insights, enabling users to identify strengths, understand high-impact skill gaps, and make informed decisions about career growth and skill development.

---

## Try Live : https://skill-lens.streamlit.app/

## Key Features

- Automated technical skill extraction using NLP-based keyword matching and TF-IDF relevance scoring  
- Multi-dimensional resume evaluation using a weighted scoring engine  
- Intelligent job role recommendation based on skill compatibility analysis  
- Identification and prioritization of critical skill gaps  
- Interactive visual analytics for skill distribution and resume performance  
- Modular and scalable system architecture  
- Professional dashboard interface built using Streamlit  

---

## System Architecture

The application follows a modular pipeline architecture:

- Resume Input Layer — Upload and preprocessing of PDF and DOCX resumes  
- Text Extraction Module — Structured content extraction from documents  
- Skill Intelligence Engine — NLP-based skill detection and categorization  
- Resume Scoring Engine — Rule-based evaluation across defined criteria  
- Recommendation Engine — Role matching and compatibility scoring  
- Visualization Layer — Interactive charts and analytical insights  
- Presentation Layer — Streamlit-based user interface  

---

## Technology Stack

- Python  
- Streamlit  
- Natural Language Processing (TF-IDF, keyword extraction)  
- Plotly for data visualization  
- Modular rule-based AI scoring framework  

---

## Installation

1. Clone the repository: https://github.com/BhuvanBhonde712/Skill-Lens/
2. Create a virtual environment: Run 'python -m venv venv'
3. Activate the environment:
   - Windows:'venv\Scripts\activate'
   - Linux / macOS: 'source venv/bin/activate'
4. Install dependencies: 'pip install -r requirements.txt'
5. Run the application: 'streamlit run app.py'

---


---

## Usage

1. Upload a resume in PDF or DOCX format.  
2. The system extracts textual content and identifies technical skills.  
3. Resume strength is evaluated using predefined scoring parameters.  
4. Matching job roles are recommended based on skill compatibility.  
5. High-priority skill gaps are presented for targeted improvement.  

---

## Future Enhancements

- Integration with Large Language Models for contextual resume feedback  
- Resume content optimization and formatting suggestions  
- Real-time job market and role demand integration  
- Personalized learning roadmap generation  
- Multi-resume comparison and progress tracking  
- Deployment as a full-scale SaaS platform  

---

## Contribution

Contributions are welcome. Fork the repository, create a feature branch, and submit a pull request with a clear description of improvements or additions.

---

## License

This project is developed for academic and research purposes. Licensing terms may be updated for production or commercial deployment.


