# utils/scorer.py
# Calculates a resume score (0-100) using a weighted multi-criteria system.
#
# Scoring breakdown:
#   Skills Detected    30 pts  — number of unique skills found
#   Skills Diversity   15 pts  — how many categories those skills span
#   Work Experience    20 pts  — experience section + action-verb density
#   Education          15 pts  — education section + degree-level keywords
#   Projects           10 pts  — projects section + deployment keywords
#   Resume Structure   10 pts  — summary, contact, certifications, links
#   ─────────────────────────
#   Total             100 pts

from utils.extractor import get_resume_sections

# Maximum points per criterion (must sum to 100)
MAX_SCORES = {
    "Skills Detected":  30,
    "Skills Diversity": 15,
    "Work Experience":  20,
    "Education":        15,
    "Projects":         10,
    "Resume Structure": 10,
}


def calculate_resume_score(text, extracted_skills, categorized_skills):
    """
    Compute a multi-dimensional resume score.

    Args:
        text (str): Raw resume text.
        extracted_skills (list[str]): Skills extracted by the skill extractor.
        categorized_skills (dict): Skills grouped by category.

    Returns:
        dict: {
            "total_score" (int): Final score out of 100,
            "breakdown" (dict): Per-criterion raw scores,
            "feedback" (list[str]): Specific improvement suggestions,
            "overall_feedback" (str): Summary message for the score level
        }
    """
    text_lower = text.lower()
    sections = get_resume_sections(text)
    breakdown = {}
    feedback = []

    # ----------------------------------------------------------------
    # 1. Skills Detected  (max 30)
    # ----------------------------------------------------------------
    n_skills = len(extracted_skills)
    if n_skills >= 20:
        s1 = 30
    elif n_skills >= 15:
        s1 = 25
    elif n_skills >= 10:
        s1 = 18
    elif n_skills >= 5:
        s1 = 10
    elif n_skills >= 2:
        s1 = 5
    else:
        s1 = 0

    breakdown["Skills Detected"] = s1
    if n_skills < 10:
        feedback.append(
            f"Only {n_skills} skills were detected. "
            "Add more relevant technical and soft skills to a dedicated Skills section."
        )

    # ----------------------------------------------------------------
    # 2. Skills Diversity  (max 15)
    # ----------------------------------------------------------------
    n_cats = len(categorized_skills)
    if n_cats >= 6:
        s2 = 15
    elif n_cats >= 4:
        s2 = 12
    elif n_cats >= 3:
        s2 = 8
    elif n_cats >= 2:
        s2 = 4
    else:
        s2 = 1

    breakdown["Skills Diversity"] = s2
    if n_cats < 3:
        feedback.append(
            "Your skills are concentrated in too few domains. "
            "Broaden your profile by adding skills from complementary categories."
        )

    # ----------------------------------------------------------------
    # 3. Work Experience  (max 20)
    # ----------------------------------------------------------------
    # Action verbs signal strong experience descriptions
    action_verbs = [
        "developed", "built", "designed", "implemented", "managed",
        "led", "created", "delivered", "optimized", "deployed",
        "improved", "maintained", "collaborated", "worked", "intern"
    ]
    exp_verb_count = sum(1 for v in action_verbs if v in text_lower)
    has_exp_section = "experience" in sections

    if has_exp_section and exp_verb_count >= 6:
        s3 = 20
    elif has_exp_section and exp_verb_count >= 3:
        s3 = 15
    elif has_exp_section:
        s3 = 10
    elif exp_verb_count >= 3:
        s3 = 6
    else:
        s3 = 2

    breakdown["Work Experience"] = s3
    if not has_exp_section:
        feedback.append(
            "No clearly labeled 'Experience' section was found. "
            "Add a Work Experience or Internship section with action verbs and quantified achievements."
        )
    elif exp_verb_count < 3:
        feedback.append(
            "Your experience descriptions are sparse. "
            "Use strong action verbs (built, deployed, optimized) and measurable outcomes."
        )

    # ----------------------------------------------------------------
    # 4. Education  (max 15)
    # ----------------------------------------------------------------
    edu_keywords = [
        "bachelor", "b.tech", "b.e", "b.sc", "master", "m.tech",
        "m.sc", "phd", "degree", "university", "college",
        "gpa", "cgpa", "percentage", "graduated", "pursuing"
    ]
    edu_count = sum(1 for kw in edu_keywords if kw in text_lower)
    has_edu = "education" in sections

    if has_edu and edu_count >= 3:
        s4 = 15
    elif has_edu:
        s4 = 10
    elif edu_count >= 2:
        s4 = 6
    else:
        s4 = 2

    breakdown["Education"] = s4
    if not has_edu:
        feedback.append(
            "Education section is missing or hard to detect. "
            "Add a clearly labeled section with your degree, institution, and graduation year."
        )

    # ----------------------------------------------------------------
    # 5. Projects  (max 10)
    # ----------------------------------------------------------------
    project_signals = [
        "project", "developed", "github", "deployed", "live",
        "streamlit", "vercel", "render", "heroku", "webapp",
        "api", "implemented", "built using"
    ]
    proj_count = sum(1 for p in project_signals if p in text_lower)
    has_proj = "projects" in sections

    if has_proj and proj_count >= 4:
        s5 = 10
    elif has_proj:
        s5 = 7
    elif proj_count >= 3:
        s5 = 4
    else:
        s5 = 0

    breakdown["Projects"] = s5
    if s5 < 5:
        feedback.append(
            "Add a Projects section with at least 2-3 projects. "
            "Include the tech stack used, what you built, and a GitHub or live link."
        )

    # ----------------------------------------------------------------
    # 6. Resume Structure  (max 10)
    # ----------------------------------------------------------------
    structure_points = 0

    # Has summary or objective
    if "summary" in sections or "objective" in text_lower:
        structure_points += 3
    else:
        feedback.append(
            "Add a brief professional summary at the top of your resume "
            "highlighting your skills, experience, and career goals."
        )

    # Has contact info
    if "@" in text or "email" in text_lower or "phone" in text_lower:
        structure_points += 2
    else:
        feedback.append("Include your email address and phone number.")

    # Has LinkedIn or GitHub
    if "linkedin" in text_lower:
        structure_points += 2
    else:
        feedback.append("Add your LinkedIn profile URL.")

    if "github" in text_lower:
        structure_points += 1
    else:
        feedback.append("Add your GitHub profile URL to showcase your code.")

    # Has certifications
    if "certifications" in sections:
        structure_points += 2

    breakdown["Resume Structure"] = min(structure_points, 10)

    # ----------------------------------------------------------------
    # Final total
    # ----------------------------------------------------------------
    total = min(sum(breakdown.values()), 100)

    if total >= 80:
        overall = "Strong resume. A few targeted refinements will make it stand out even more."
    elif total >= 65:
        overall = "Good resume with a solid foundation. Address the suggestions below to reach the next level."
    elif total >= 45:
        overall = "Average resume. It needs more depth in skills, experience descriptions, and structure."
    else:
        overall = "Resume needs significant improvement. Work through each suggestion carefully."

    return {
        "total_score": total,
        "breakdown": breakdown,
        "feedback": feedback,
        "overall_feedback": overall
    }


def get_resume_level(score):
    """
    Return a short human-readable label for the resume quality tier.

    Args:
        score (int): Resume score out of 100.

    Returns:
        str: One of "Excellent", "Good", "Average", "Needs Improvement".
    """
    if score >= 80:
        return "Excellent"
    elif score >= 65:
        return "Good"
    elif score >= 45:
        return "Average"
    else:
        return "Needs Improvement"