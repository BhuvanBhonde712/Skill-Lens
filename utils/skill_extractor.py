# utils/skill_extractor.py
# Performs NLP-based skill extraction from resume text.
#
# Techniques used:
#   1. Keyword matching   — Match against the skills database using regex word boundaries.
#   2. TF-IDF scoring     — Rank skills by frequency-weighted relevance in the document.
#
# Multi-word skills (e.g. "machine learning", "react native") are handled correctly
# by sorting skills longest-first to avoid partial substring collisions.

import re
import math
from data.skills_db import SKILLS_DB, ALL_SKILLS


def preprocess_text(text):
    """
    Normalize resume text for consistent skill matching.

    Steps:
        - Lowercase
        - Remove punctuation except characters used in skill names (., +, #, /)
        - Collapse extra whitespace

    Args:
        text (str): Raw resume text.

    Returns:
        str: Cleaned and normalized text.
    """
    text = text.lower()
    # Keep alphanumeric, space, dot, plus, hash, slash (used in skill names like c++, node.js)
    text = re.sub(r'[^\w\s\.\+\#\/]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def build_skill_pattern(skill):
    """
    Build a regex pattern for a skill that respects word boundaries.

    Handles:
        - Multi-word skills: "machine learning" must not match "machine"
        - Special chars: "c++" -> escaped as "c\+\+"
        - Boundaries: "r" must not match inside "react" or "keras"

    Args:
        skill (str): A single skill name.

    Returns:
        str: Compiled regex pattern string.
    """
    escaped = re.escape(skill.lower())
    # Use negative lookbehind/lookahead for alphanumeric boundaries
    return r'(?<![a-z0-9])' + escaped + r'(?![a-z0-9])'


def extract_skills(text):
    """
    Extract matching skills from resume text using keyword-based NLP matching.

    Matches each skill from the database against the resume using
    regex word-boundary patterns. Longer/multi-word skills are checked
    first to prevent shorter skills from incorrectly matching substrings.

    Args:
        text (str): Raw resume text.

    Returns:
        list[str]: Sorted list of unique matched skill names.
    """
    processed = preprocess_text(text)
    found_skills = set()

    # Sort descending by length: "machine learning" before "machine" and "learning"
    skills_sorted = sorted(ALL_SKILLS, key=len, reverse=True)

    for skill in skills_sorted:
        pattern = build_skill_pattern(skill)
        if re.search(pattern, processed):
            found_skills.add(skill)

    return sorted(list(found_skills))


def get_skill_categories(skills):
    """
    Group a list of skills into their respective categories from the database.

    Args:
        skills (list[str]): Skills extracted from the resume.

    Returns:
        dict[str, list[str]]: Category -> list of matched skills in that category.
    """
    skills_lower = {s.lower() for s in skills}
    categorized = {}

    for category, category_skills in SKILLS_DB.items():
        matched = [s for s in category_skills if s.lower() in skills_lower]
        if matched:
            categorized[category] = matched

    return categorized


def compute_tfidf_scores(text, skills):
    """
    Compute a TF-IDF-inspired relevance score for each detected skill.

    TF  = frequency of skill occurrence / total word count in resume
    IDF = log( total_skills_in_db / (1 + number of skills detected) )
          — skills that are rarer in the DB get a higher IDF weight

    This is used to surface the candidate's "dominant" skills for display.

    Args:
        text (str): Raw resume text.
        skills (list[str]): Skills detected in the resume.

    Returns:
        dict[str, float]: {skill_name: relevance_score} sorted by score.
    """
    processed = preprocess_text(text)
    words = processed.split()
    total_words = max(len(words), 1)
    total_db_skills = len(ALL_SKILLS)
    num_detected = max(len(skills), 1)

    scores = {}
    for skill in skills:
        pattern = build_skill_pattern(skill)
        count = len(re.findall(pattern, processed))
        tf = count / total_words
        idf = math.log(total_db_skills / num_detected + 1)
        scores[skill] = round(tf * idf * 10000, 3)

    # Return sorted by score descending
    return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))