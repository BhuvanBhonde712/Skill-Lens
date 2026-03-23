# app.py
# AI-Powered Resume Analyzer — Main Streamlit Application
#
# Run with:   streamlit run app.py
#
# Architecture:
#   app.py  ->  utils/extractor.py        (text extraction from PDF/DOCX)
#           ->  utils/skill_extractor.py  (NLP keyword + TF-IDF skill extraction)
#           ->  utils/scorer.py           (multi-criteria resume scoring)
#           ->  utils/visualizer.py       (Plotly charts)
#           ->  models/recommender.py     (job role matching)
#           ->  data/skills_db.py         (skills database)
#           ->  data/job_roles.py         (job roles and requirements)

import sys
import os

# Ensure the project root is on the Python path for clean imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

from utils.extractor       import extract_text
from utils.skill_extractor import extract_skills, get_skill_categories, compute_tfidf_scores
from utils.scorer          import calculate_resume_score, get_resume_level, MAX_SCORES
from utils.visualizer      import skill_distribution_chart, resume_strength_chart, score_breakdown_bar
from models.recommender    import recommend_job_roles, get_all_missing_skills


# ──────────────────────────────────────────────────────────────
# Page configuration  (must be the first Streamlit call)
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ──────────────────────────────────────────────────────────────
# Global CSS  — dark professional theme
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

  /* ── Base ── */
  .stApp { background-color: #0d1117; font-family: 'DM Sans', sans-serif; }
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 1.8rem 2.5rem; max-width: 1240px; }

  /* ── App header ── */
  .app-header {
    padding: 2rem 0 1.6rem;
    border-bottom: 1px solid #1e2535;
    margin-bottom: 2rem;
  }
  .app-header h1 {
    font-size: 2rem; font-weight: 700;
    color: #f0f4f8; letter-spacing: -0.5px; margin: 0 0 0.4rem;
  }
  .app-header p { color: #8899aa; font-size: 0.95rem; margin: 0; }
  .accent { color: #00bcd4; }

  /* ── Metric cards ── */
  .metric-card {
    background: #161b27; border: 1px solid #1e2535;
    border-radius: 10px; padding: 1.1rem 1.4rem;
  }
  .metric-card h3 {
    font-size: 0.72rem; font-weight: 600;
    color: #8899aa; text-transform: uppercase;
    letter-spacing: 0.08em; margin: 0 0 0.5rem;
  }
  .metric-card .val {
    font-family: 'Space Mono', monospace;
    font-size: 1.9rem; font-weight: 700; color: #f0f4f8; line-height: 1;
  }
  .metric-card .sub { font-size: 0.82rem; color: #8899aa; margin-top: 0.3rem; }

  /* ── Score colors ── */
  .c-excellent { color: #4caf50; }
  .c-good      { color: #8bc34a; }
  .c-average   { color: #ff9800; }
  .c-poor      { color: #ef5350; }
  .c-high      { color: #4caf50; }
  .c-mid       { color: #ff9800; }
  .c-low       { color: #ef5350; }

  /* ── Section headings ── */
  .sec-title {
    font-size: 1rem; font-weight: 600; color: #f0f4f8;
    margin: 0 0 1rem; padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e2535;
  }

  /* ── Skill badges ── */
  .badge {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem; font-weight: 400;
    padding: 0.22rem 0.65rem; margin: 0.18rem;
    border-radius: 4px;
  }
  .badge-default { background: #1a2535; border: 1px solid #2d3550; color: #c8d8e8; }
  .badge-accent  { background: #003545; border: 1px solid #00bcd4; color: #00bcd4; }
  .badge-danger  { background: #2d1a1a; border: 1px solid #ef5350; color: #ef5350; }

  /* ── Progress bar ── */
  .pbar-track { background: #1e2535; border-radius: 4px; height: 7px; overflow: hidden; margin-top: 0.35rem; }
  .pbar-fill  { height: 100%; border-radius: 4px; }

  /* ── Feedback items ── */
  .feedback-item {
    background: #161b27; border-left: 3px solid #ff9800;
    padding: 0.65rem 1rem; margin-bottom: 0.45rem;
    border-radius: 0 6px 6px 0; font-size: 0.87rem; color: #c8d8e8;
    line-height: 1.5;
  }

  /* ── Job role card ── */
  .job-card {
    background: #161b27; border: 1px solid #1e2535;
    border-radius: 10px; padding: 1.1rem 1.3rem; margin-bottom: 0.75rem;
    transition: border-color 0.15s;
  }
  .job-card:hover { border-color: #00bcd4; }
  .job-card h4 { font-size: 0.97rem; font-weight: 600; color: #f0f4f8; margin: 0 0 0.25rem; }
  .job-card p  { font-size: 0.84rem; color: #8899aa; margin: 0 0 0.6rem; line-height: 1.5; }

  /* ── Info box ── */
  .info-box {
    background: #0d1f2d; border: 1px solid #00bcd4;
    border-radius: 8px; padding: 0.9rem 1.1rem;
    font-size: 0.87rem; color: #b0d8e0; line-height: 1.6;
  }

  /* ── Tab bar ── */
  .stTabs [data-baseweb="tab-list"] {
    background: #161b27; border-radius: 8px; padding: 0.28rem; gap: 0.15rem;
  }
  .stTabs [data-baseweb="tab"] {
    color: #8899aa; font-size: 0.86rem; font-weight: 500;
    border-radius: 6px; padding: 0.45rem 1rem;
  }
  .stTabs [aria-selected="true"] {
    background: #1a2535 !important; color: #00bcd4 !important;
  }

  /* ── Divider ── */
  hr { border-color: #1e2535; margin: 1.5rem 0; }

  /* ── File uploader ── */
  [data-testid="stFileUploader"] > div {
    background: #161b27 !important; border: 1.5px dashed #2d3550 !important;
    border-radius: 10px !important;
  }

  /* ── Expander ── */
  details { background: #161b27 !important; border: 1px solid #1e2535 !important; border-radius: 8px !important; }
  summary { color: #c8d8e8 !important; font-size: 0.88rem !important; }

  /* ── Spinner text ── */
  .stSpinner > div { border-top-color: #00bcd4 !important; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# Utility render helpers
# ──────────────────────────────────────────────────────────────

def score_color(score):
    if score >= 80: return "c-excellent"
    elif score >= 65: return "c-good"
    elif score >= 45: return "c-average"
    else: return "c-poor"


def match_color(pct):
    if pct >= 65: return "c-high"
    elif pct >= 35: return "c-mid"
    else: return "c-low"


def badges_html(items, style="badge-default"):
    return "".join(f'<span class="badge {style}">{s}</span>' for s in items)


def progress_bar_html(val, max_val):
    pct = (val / max_val) * 100 if max_val else 0
    color = "#4caf50" if pct >= 70 else "#ff9800" if pct >= 40 else "#ef5350"
    return (
        f'<div class="pbar-track">'
        f'<div class="pbar-fill" style="width:{pct:.1f}%;background:{color};"></div>'
        f'</div>'
    )


# ──────────────────────────────────────────────────────────────
# App Header
# ──────────────────────────────────────────────────────────────

st.markdown("""
<style>

.skill-header{
display:flex;
align-items:center;
gap:16px;
margin-bottom:34px;
}

.logo-svg{
width:64px;
height:64px;
}

.title-box{
display:flex;
flex-direction:column;
justify-content:center;
}

.main-title{
font-size:44px;
font-weight:700;
letter-spacing:-0.8px;
line-height:1;
}

.skill{
color:#e6edf3;
}

.lens{
color:#00bcd4;
margin-left:0px;
}

.sub{
color:#8b949e;
font-size:15px;
margin-top:6px;
font-weight:500;
}

</style>

<div class="skill-header">

<svg class="logo-svg" viewBox="0 0 64 64" fill="none">

<!-- document -->
<rect x="10" y="6" width="30" height="44" rx="6" stroke="#00bcd4" stroke-width="3"/>

<!-- lines -->
<line x1="16" y1="18" x2="32" y2="18" stroke="#00bcd4" stroke-width="3"/>
<line x1="16" y1="26" x2="32" y2="26" stroke="#00bcd4" stroke-width="3"/>
<line x1="16" y1="34" x2="28" y2="34" stroke="#00bcd4" stroke-width="3"/>

<!-- lens circle -->
<circle cx="42" cy="42" r="10" stroke="#00bcd4" stroke-width="3"/>

<!-- lens stick -->
<line x1="49" y1="49" x2="58" y2="58" stroke="#00bcd4" stroke-width="3" stroke-linecap="round"/>

</svg>

<div class="title-box">

<div class="main-title">
<span class="skill">Skill</span>
<span class="lens">Lens</span>
</div>

<div class="sub">
• AI Resume Analyzer
</div>

</div>

</div>

""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# Upload Section
# ──────────────────────────────────────────────────────────────

upload_col, guide_col = st.columns([3, 2], gap="large")

with upload_col:
    st.markdown('<div class="sec-title">Upload Resume</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        label="Supports PDF and DOCX — max 10 MB",
        type=["pdf", "docx"],
        help="Text-based PDFs work best. Scanned/image PDFs are not supported."
    )

with guide_col:
    st.markdown("""
    <div class="info-box">
      <strong style="color:#00bcd4; font-size:0.9rem;">How it works</strong><br><br>
      Step 1 &mdash; Upload a PDF or DOCX resume<br>
      Step 2 &mdash; NLP extracts skills from raw text<br>
      Step 3 &mdash; Resume is scored across 6 criteria<br>
      Step 4 &mdash; Job roles are matched and skill gaps identified
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# Analysis Pipeline  (runs only when a file is uploaded)
# ──────────────────────────────────────────────────────────────

if uploaded_file is not None:

    file_bytes = uploaded_file.read()
    file_ext   = uploaded_file.name.rsplit(".", 1)[-1]

    with st.spinner("Extracting and analyzing resume..."):
        try:
            # ── Step 1: Extract text ──────────────────────────────────
            resume_text = extract_text(file_bytes, file_ext)

            if len(resume_text.strip()) < 80:
                st.error(
                    "Not enough text could be extracted. "
                    "Please ensure the file is a text-based PDF or a standard DOCX."
                )
                st.stop()

            # ── Step 2: Skill extraction ──────────────────────────────
            extracted_skills  = extract_skills(resume_text)
            categorized       = get_skill_categories(extracted_skills)
            tfidf_scores      = compute_tfidf_scores(resume_text, extracted_skills)

            # ── Step 3: Resume scoring ────────────────────────────────
            score_result = calculate_resume_score(resume_text, extracted_skills, categorized)

            # ── Step 4: Job recommendations ───────────────────────────
            recommendations  = recommend_job_roles(extracted_skills, top_n=6)
            missing_ranked   = get_all_missing_skills(extracted_skills, recommendations)

        except ValueError as ve:
            st.error(str(ve))
            st.stop()
        except Exception as e:
            st.error(f"Unexpected error during analysis: {str(e)}")
            st.stop()

    st.markdown("---")

    # ──────────────────────────────────────────────────────────
    # Top metrics row
    # ──────────────────────────────────────────────────────────

    total_score  = score_result["total_score"]
    level        = get_resume_level(total_score)
    top_role     = recommendations[0] if recommendations else None

    m1, m2, m3, m4 = st.columns(4, gap="small")

    with m1:
        st.markdown(f"""
        <div class="metric-card">
          <h3>Resume Score</h3>
          <div class="val {score_color(total_score)}">{total_score}<span style="font-size:1rem;color:#8899aa;">/100</span></div>
          <div class="sub">{level}</div>
        </div>""", unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-card">
          <h3>Skills Detected</h3>
          <div class="val">{len(extracted_skills)}</div>
          <div class="sub">{len(categorized)} categories</div>
        </div>""", unsafe_allow_html=True)

    with m3:
        top_pct  = top_role["match_score"] if top_role else 0
        top_name = top_role["name"]        if top_role else "—"
        st.markdown(f"""
        <div class="metric-card">
          <h3>Best Role Match</h3>
          <div class="val {match_color(top_pct)}">{top_pct}%</div>
          <div class="sub">{top_name}</div>
        </div>""", unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="metric-card">
          <h3>Skill Gaps</h3>
          <div class="val">{len(missing_ranked)}</div>
          <div class="sub">high-impact skills to acquire</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ──────────────────────────────────────────────────────────
    # Tabbed results
    # ──────────────────────────────────────────────────────────

    tab_skills, tab_score, tab_jobs, tab_gaps, tab_raw = st.tabs([
        "Skills Analysis",
        "Resume Score",
        "Job Recommendations",
        "Skill Gaps",
        "Extracted Text"
    ])

    # ── TAB 1: Skills Analysis ───────────────────────────────
    with tab_skills:

        st.markdown('<div class="sec-title">All Detected Skills</div>', unsafe_allow_html=True)

        if extracted_skills:
            # Top skills by TF-IDF relevance
            top_tfidf = list(tfidf_scores.keys())[:10]
            st.markdown("**Top Skills by Relevance (TF-IDF)**")
            st.markdown(badges_html(top_tfidf, "badge-accent"), unsafe_allow_html=True)

            st.markdown("<br>**All Detected Skills**", unsafe_allow_html=True)
            st.markdown(badges_html(extracted_skills), unsafe_allow_html=True)
        else:
            st.warning(
                "No skills were detected. "
                "Make sure your resume has a visible Skills or Technologies section."
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Skills by category with expanders
        if categorized:
            st.markdown('<div class="sec-title">Skills by Category</div>', unsafe_allow_html=True)
            for category, skills in sorted(categorized.items(), key=lambda x: -len(x[1])):
                with st.expander(f"{category}  —  {len(skills)} skill{'s' if len(skills) != 1 else ''}"):
                    st.markdown(badges_html(skills, "badge-default"), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            fig_dist = skill_distribution_chart(categorized)
            if fig_dist:
                st.plotly_chart(fig_dist, use_container_width=True)

    # ── TAB 2: Resume Score ──────────────────────────────────
    with tab_score:

        left, right = st.columns([1, 1], gap="large")

        with left:
            st.markdown('<div class="sec-title">Score Breakdown</div>', unsafe_allow_html=True)

            for criterion, raw in score_result["breakdown"].items():
                max_val = MAX_SCORES.get(criterion, 10)
                st.markdown(f"""
                <div style="margin-bottom:1.1rem;">
                  <div style="display:flex;justify-content:space-between;margin-bottom:0.25rem;">
                    <span style="font-size:0.87rem;color:#c8d8e8;">{criterion}</span>
                    <span style="font-size:0.82rem;color:#8899aa;font-family:monospace;">{raw}&nbsp;/&nbsp;{max_val}</span>
                  </div>
                  {progress_bar_html(raw, max_val)}
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div style="margin-top:1.5rem;padding:1rem 1.1rem;background:#161b27;
                        border-radius:8px;border:1px solid #1e2535;">
              <span style="font-size:0.72rem;text-transform:uppercase;color:#8899aa;letter-spacing:.08em;">Overall Assessment</span>
              <p style="font-size:0.88rem;color:#c8d8e8;margin:.5rem 0 0;line-height:1.6;">
                {score_result['overall_feedback']}
              </p>
            </div>
            """, unsafe_allow_html=True)

        with right:
            fig_radar = resume_strength_chart(score_result["breakdown"])
            st.plotly_chart(fig_radar, use_container_width=True)

            fig_bar = score_breakdown_bar(score_result["breakdown"])
            st.plotly_chart(fig_bar, use_container_width=True)

        # Improvement suggestions
        if score_result["feedback"]:
            st.markdown('<div class="sec-title">Improvement Suggestions</div>', unsafe_allow_html=True)
            for tip in score_result["feedback"]:
                st.markdown(f'<div class="feedback-item">{tip}</div>', unsafe_allow_html=True)

    # ── TAB 3: Job Recommendations ───────────────────────────
    with tab_jobs:

        st.markdown('<div class="sec-title">Top Matched Job Roles</div>', unsafe_allow_html=True)

        if not recommendations:
            st.warning("Not enough skills detected to generate role recommendations.")
        else:
            for role in recommendations:
                mc = match_color(role["match_score"])
                st.markdown(f"""
                <div class="job-card">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div>
                      <h4>{role['name']}</h4>
                      <p>{role['description']}</p>
                    </div>
                    <div style="text-align:right;min-width:72px;padding-left:1rem;">
                      <span class="{mc}" style="font-size:1.4rem;font-family:monospace;font-weight:700;">{role['match_score']}%</span>
                      <div style="font-size:0.72rem;color:#8899aa;">match</div>
                    </div>
                  </div>
                  <div style="display:flex;gap:1.5rem;font-size:0.8rem;color:#8899aa;margin-bottom:0.4rem;">
                    <span>Salary: <span style="color:#c8d8e8;">{role['salary']}</span></span>
                    <span>Level: <span style="color:#c8d8e8;">{role['experience_level']}</span></span>
                  </div>
                  {progress_bar_html(role['match_score'], 100)}
                </div>
                """, unsafe_allow_html=True)

                with st.expander(f"Skill details — {role['name']}"):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("**Required Skills**")
                        st.markdown(badges_html(role["required_skills"]), unsafe_allow_html=True)
                        if role["optional_skills"]:
                            st.markdown("<br>**Optional / Bonus Skills**", unsafe_allow_html=True)
                            st.markdown(badges_html(role["optional_skills"]), unsafe_allow_html=True)
                    with c2:
                        st.markdown("**Missing Required Skills**")
                        if role["missing_required"]:
                            st.markdown(badges_html(role["missing_required"], "badge-danger"), unsafe_allow_html=True)
                        else:
                            st.success("You have all required skills for this role.")
                        if role["missing_optional"]:
                            st.markdown("<br>**Missing Optional Skills**", unsafe_allow_html=True)
                            st.markdown(badges_html(role["missing_optional"]), unsafe_allow_html=True)

    # ── TAB 4: Skill Gaps ────────────────────────────────────
    with tab_gaps:

        st.markdown('<div class="sec-title">High-Priority Skill Gaps</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box" style="margin-bottom:1.4rem;">
          Skills listed below are missing from your resume and appear as requirements across
          multiple top matched job roles. Learning these will simultaneously boost your
          compatibility with several roles.
        </div>
        """, unsafe_allow_html=True)

        if missing_ranked:
            for skill, freq in missing_ranked:
                label = f"Required in {freq} role{'s' if freq > 1 else ''}"
                urgency_color = "#ef5350" if freq >= 3 else "#ff9800" if freq >= 2 else "#8899aa"
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                            padding:0.65rem 1rem;background:#161b27;border:1px solid #1e2535;
                            border-radius:8px;margin-bottom:0.4rem;">
                  <span style="font-family:monospace;font-size:0.86rem;color:#c8d8e8;">{skill}</span>
                  <span style="font-size:0.75rem;background:#1e2535;color:{urgency_color};
                               padding:0.18rem 0.6rem;border-radius:4px;border:1px solid {urgency_color}33;">
                    {label}
                  </span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success(
                "Your skill profile already covers the required skills "
                "across the top matched roles."
            )

    # ── TAB 5: Extracted Text ────────────────────────────────
    with tab_raw:

        st.markdown('<div class="sec-title">Extracted Resume Text</div>', unsafe_allow_html=True)

        word_count = len(resume_text.split())
        char_count = len(resume_text)
        display_text = resume_text[:4000] + ("\n\n[truncated — showing first 4000 characters]" if len(resume_text) > 4000 else "")

        st.markdown(f"""
        <div style="background:#161b27;border:1px solid #1e2535;border-radius:8px;
                    padding:1.2rem;font-family:monospace;font-size:0.8rem;
                    color:#c8d8e8;white-space:pre-wrap;overflow-y:auto;max-height:500px;
                    line-height:1.6;">
{display_text}
        </div>
        <div style="font-size:0.78rem;color:#8899aa;margin-top:0.5rem;">
          {word_count:,} words &nbsp;&middot;&nbsp; {char_count:,} characters extracted from <em>{uploaded_file.name}</em>
        </div>
        """, unsafe_allow_html=True)

else:
    # ── Empty state ───────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center;padding:5rem 2rem;color:#8899aa;">
      <div style="width:56px;height:56px;border:2px solid #2d3550;border-radius:12px;
                  display:flex;align-items:center;justify-content:center;margin:0 auto 1.5rem;
                  font-size:1.5rem;color:#2d3550;">&#9741;</div>
      <div style="font-size:1.05rem;font-weight:600;color:#c8d8e8;margin-bottom:0.5rem;">
        No resume uploaded
      </div>
      <div style="font-size:0.9rem;max-width:380px;margin:0 auto;line-height:1.6;">
        Upload a PDF or DOCX file above to begin the analysis.
        The system will extract skills, score your resume, and recommend job roles.
      </div>
    </div>
    """, unsafe_allow_html=True)