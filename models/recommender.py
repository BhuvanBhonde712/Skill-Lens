# models/recommender.py
# Recommends job roles based on skills extracted from a resume.
#
# Approach:
#   - For each role in JOB_ROLES, compute a weighted match score:
#       * Required skills contribute 70% of the score
#       * Optional skills contribute 30% of the score
#   - Sort roles by match score and return the top N
#   - Identify which required/optional skills are missing for each role
#   - Aggregate missing skills across top roles to surface high-impact gaps

from collections import Counter
from data.job_roles import JOB_ROLES


def _compute_match_score(extracted_lower, required_skills, optional_skills):
    """
    Compute weighted match percentage between resume skills and a job role.

    Formula:
        score = (required_matched / total_required) * 70
              + (optional_matched / total_optional) * 30

    Args:
        extracted_lower (set[str]): Lowercase set of resume skills.
        required_skills (list[str]): Role's required skills.
        optional_skills (list[str]): Role's optional/bonus skills.

    Returns:
        float: Match score in range [0.0, 100.0].
    """
    req_total = max(len(required_skills), 1)
    opt_total = max(len(optional_skills), 1)

    req_matched = sum(1 for s in required_skills if s.lower() in extracted_lower)
    opt_matched = sum(1 for s in optional_skills if s.lower() in extracted_lower)

    req_score = (req_matched / req_total) * 70
    opt_score = (opt_matched / opt_total) * 30

    return round(req_score + opt_score, 1)


def recommend_job_roles(extracted_skills, top_n=6):
    """
    Recommend the top N job roles based on resume skills.

    Args:
        extracted_skills (list[str]): Skills found in the resume.
        top_n (int): Number of roles to return (default 6).

    Returns:
        list[dict]: Sorted list of role recommendation objects.
            Each dict has:
                name (str)               — role title
                match_score (float)      — 0–100 compatibility score
                description (str)        — what this role does
                required_skills (list)   — all required skills for the role
                optional_skills (list)   — all optional/bonus skills
                missing_required (list)  — required skills not in resume
                missing_optional (list)  — optional skills not in resume
                salary (str)             — average salary range
                experience_level (str)   — entry/mid/senior label
    """
    extracted_lower = {s.lower() for s in extracted_skills}
    results = []

    for role_name, role_data in JOB_ROLES.items():
        required = role_data.get("required_skills", [])
        optional = role_data.get("optional_skills", [])

        score = _compute_match_score(extracted_lower, required, optional)

        missing_required = [s for s in required if s.lower() not in extracted_lower]
        missing_optional = [s for s in optional if s.lower() not in extracted_lower]

        results.append({
            "name":             role_name,
            "match_score":      score,
            "description":      role_data.get("description", ""),
            "required_skills":  required,
            "optional_skills":  optional,
            "missing_required": missing_required,
            "missing_optional": missing_optional,
            "salary":           role_data.get("avg_salary", "N/A"),
            "experience_level": role_data.get("experience_level", "N/A")
        })

    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results[:top_n]


def get_all_missing_skills(extracted_skills, top_roles):
    """
    Aggregate missing required skills across all top recommended roles.

    A skill that is missing in 3 out of 5 top roles is more impactful
    to learn than one missing in only 1 role. Sorted by frequency.

    Args:
        extracted_skills (list[str]): Resume skills (used for filtering).
        top_roles (list[dict]): Output of recommend_job_roles().

    Returns:
        list[tuple]: [(skill_name, frequency), ...] sorted by frequency desc.
                     Capped at 15 skills.
    """
    counter = Counter()
    for role in top_roles:
        for skill in role["missing_required"]:
            counter[skill] += 1

    return counter.most_common(15)