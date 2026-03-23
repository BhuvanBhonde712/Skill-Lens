# utils/visualizer.py
# Generates Plotly figures for the Streamlit dashboard.
# All charts use the app's dark color palette for visual consistency.
#
# Charts provided:
#   - skill_distribution_chart  — horizontal bar chart of skills per category
#   - resume_strength_chart     — radar chart of score dimensions
#   - score_breakdown_bar       — horizontal bar chart of score breakdown

import plotly.graph_objects as go

# ---- Shared dark theme constants ----
BG_COLOR    = "#0d1117"
CARD_COLOR  = "#161b27"
GRID_COLOR  = "#1e2535"
TEXT_COLOR  = "#e0e0e0"
MUTED_COLOR = "#8899aa"
ACCENT      = "#00bcd4"


def skill_distribution_chart(categorized_skills):
    """
    Horizontal bar chart showing number of skills detected per category.

    Args:
        categorized_skills (dict): {category: [skill, ...]} mapping.

    Returns:
        plotly.graph_objects.Figure or None if no data.
    """
    if not categorized_skills:
        return None

    # Sort categories by skill count for cleaner visual hierarchy
    sorted_items = sorted(categorized_skills.items(), key=lambda x: len(x[1]))
    categories = [item[0] for item in sorted_items]
    counts = [len(item[1]) for item in sorted_items]

    # Color scale: low counts light teal, high counts bright teal
    max_count = max(counts) if counts else 1
    bar_colors = [
        f"rgba(0, {int(188 * (c / max_count) + 60)}, 212, {0.5 + 0.5 * (c / max_count)})"
        for c in counts
    ]

    fig = go.Figure(go.Bar(
        x=counts,
        y=categories,
        orientation='h',
        marker=dict(color=bar_colors, line=dict(width=0)),
        text=counts,
        textposition='outside',
        textfont=dict(color=MUTED_COLOR, size=12),
        hovertemplate='<b>%{y}</b><br>Skills: %{x}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(
            text="Detected Skills by Category",
            font=dict(size=15, color=TEXT_COLOR),
            x=0
        ),
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        font=dict(color=TEXT_COLOR, family="DM Sans, sans-serif"),
        xaxis=dict(
            gridcolor=GRID_COLOR,
            title=dict(text="Number of Skills", font=dict(color=MUTED_COLOR)),
            tickfont=dict(color=MUTED_COLOR),
            zeroline=False
        ),
        yaxis=dict(
            gridcolor=GRID_COLOR,
            tickfont=dict(color=TEXT_COLOR, size=12)
        ),
        height=max(300, len(categories) * 42),
        margin=dict(l=20, r=60, t=50, b=40)
    )

    return fig


def resume_strength_chart(score_breakdown):
    """
    Radar (spider) chart visualizing performance across each scoring dimension.
    Each axis is normalized to 0-100% of its maximum possible score.

    Args:
        score_breakdown (dict): {criterion: raw_score}.

    Returns:
        plotly.graph_objects.Figure
    """
    max_values = {
        "Skills Detected":  30,
        "Skills Diversity": 15,
        "Work Experience":  20,
        "Education":        15,
        "Projects":         10,
        "Resume Structure": 10,
    }

    categories = list(score_breakdown.keys())
    # Normalize each score to a 0-100 scale
    normalized = [
        round((score_breakdown[c] / max_values.get(c, 10)) * 100, 1)
        for c in categories
    ]

    # Close the polygon by repeating the first value
    r_vals = normalized + [normalized[0]]
    theta_vals = categories + [categories[0]]

    fig = go.Figure(go.Scatterpolar(
        r=r_vals,
        theta=theta_vals,
        fill='toself',
        fillcolor='rgba(0, 188, 212, 0.15)',
        line=dict(color=ACCENT, width=2),
        marker=dict(color=ACCENT, size=7),
        hovertemplate='<b>%{theta}</b><br>Score: %{r:.0f}%<extra></extra>'
    ))

    fig.update_layout(
        polar=dict(
            bgcolor=CARD_COLOR,
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor=GRID_COLOR,
                tickfont=dict(color=MUTED_COLOR, size=9),
                tickvals=[25, 50, 75, 100],
                ticksuffix="%",
                linecolor=GRID_COLOR
            ),
            angularaxis=dict(
                gridcolor=GRID_COLOR,
                tickfont=dict(color=TEXT_COLOR, size=11),
                linecolor=GRID_COLOR
            )
        ),
        paper_bgcolor=BG_COLOR,
        font=dict(color=TEXT_COLOR, family="DM Sans, sans-serif"),
        title=dict(
            text="Resume Strength Profile",
            font=dict(size=15, color=TEXT_COLOR),
            x=0
        ),
        height=380,
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig


def score_breakdown_bar(score_breakdown):
    """
    Horizontal bar chart showing raw score vs maximum for each criterion.
    Bars are color-coded: green (>=70%), amber (>=40%), red (<40%).

    Args:
        score_breakdown (dict): {criterion: raw_score}.

    Returns:
        plotly.graph_objects.Figure
    """
    max_values = {
        "Skills Detected":  30,
        "Skills Diversity": 15,
        "Work Experience":  20,
        "Education":        15,
        "Projects":         10,
        "Resume Structure": 10,
    }

    categories = list(score_breakdown.keys())
    raw_scores  = [score_breakdown[c] for c in categories]
    max_scores  = [max_values.get(c, 10) for c in categories]
    pct         = [(s / m) * 100 for s, m in zip(raw_scores, max_scores)]

    colors = [
        "#4caf50" if p >= 70 else "#ff9800" if p >= 40 else "#ef5350"
        for p in pct
    ]

    fig = go.Figure(go.Bar(
        x=raw_scores,
        y=categories,
        orientation='h',
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"{s} / {m}" for s, m in zip(raw_scores, max_scores)],
        textposition='outside',
        textfont=dict(color=MUTED_COLOR, size=11),
        hovertemplate='<b>%{y}</b><br>Score: %{x}<extra></extra>'
    ))

    # Add max-score reference line as a translucent overlay bar
    fig.add_trace(go.Bar(
        x=max_scores,
        y=categories,
        orientation='h',
        marker=dict(color='rgba(255,255,255,0.04)', line=dict(width=0)),
        showlegend=False,
        hoverinfo='skip'
    ))

    fig.update_layout(
        barmode='overlay',
        title=dict(
            text="Score Breakdown",
            font=dict(size=15, color=TEXT_COLOR),
            x=0
        ),
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        font=dict(color=TEXT_COLOR, family="DM Sans, sans-serif"),
        xaxis=dict(
            gridcolor=GRID_COLOR,
            title=dict(text="Points", font=dict(color=MUTED_COLOR)),
            tickfont=dict(color=MUTED_COLOR),
            zeroline=False
        ),
        yaxis=dict(
            tickfont=dict(color=TEXT_COLOR, size=12),
            gridcolor=GRID_COLOR
        ),
        height=350,
        margin=dict(l=20, r=80, t=50, b=40)
    )

    return fig