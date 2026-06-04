from datetime import date
from fastapi import HTTPException, status
from Schemas.aiSchemas import (
    ParseCVResponse,
    CouncilChatRequest,
    CouncilChatResponse,
    SuggestRolesRequest,
    SuggestRolesResponse,
    GenerateCVRequest,
    GenerateCVResponse,
)


def parse_cv(file_content: bytes, filename: str) -> ParseCVResponse:
    return ParseCVResponse(
        education="B.Sc. in Computer Science",
        experience="5 years at Tech Corp",
        skills="Python, Vue.js, FastAPI",
        softSkills="Leadership, Communication",
        certificates="AWS Certified Developer",
        languages="English, French"
    )


def council_chat(payload: CouncilChatRequest) -> CouncilChatResponse:
    return CouncilChatResponse(
        nextQuestion=f"You mentioned working in {payload.currentField}. Can you elaborate on your specific achievements?",
        extractedData={"keywords": ["Vue", "FastAPI"]}
    )


def suggest_roles(payload: SuggestRolesRequest) -> SuggestRolesResponse:
    return SuggestRolesResponse(
        suggestedRoles=["Senior Frontend Developer", "Full Stack Engineer"]
    )


def _nl2br(text: str) -> str:
    """Convert newlines to HTML paragraphs."""
    if not text:
        return ""
    paragraphs = [p.strip() for p in text.strip().split("\n") if p.strip()]
    return "".join(f"<p>{p}</p>" for p in paragraphs)


def _build_skills_html(skills_text: str, job_tags: list) -> str:
    """Parse skills string into tagged badges, highlighting those that match job."""
    if not skills_text:
        return "<p style='color:#94a3b8'>Not specified</p>"
    job_tags_lower = [t.lower() for t in job_tags]
    items = [s.strip() for s in skills_text.replace(",", "\n").split("\n") if s.strip()]
    html = '<div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:8px">'
    for item in items:
        is_match = any(t in item.lower() or item.lower() in t for t in job_tags_lower)
        color = "#2563eb" if is_match else "#64748b"
        bg = "#eff6ff" if is_match else "#f8fafc"
        border = "#bfdbfe" if is_match else "#e2e8f0"
        star = " ⭐" if is_match else ""
        html += (
            f'<span style="background:{bg};color:{color};border:1px solid {border};'
            f'padding:4px 12px;border-radius:20px;font-size:13px;font-weight:500">'
            f'{item}{star}</span>'
        )
    html += "</div>"
    return html


def generate_custom_cv(payload: GenerateCVRequest) -> GenerateCVResponse:
    p = payload.userProfile
    j = payload.jobInfo

    full_name = f"{p.first_name or ''} {p.last_name or ''}".strip() or "Candidate"
    current_title = p.current_title or j.title
    today = date.today().strftime("%B %Y")
    filename = f"CV_{(full_name).replace(' ', '_')}_{j.company.replace(' ', '_')}.html"

    # Build skills section with job-matching highlights
    skills_html = _build_skills_html(p.skills or "", j.tags)

    # Soft skills
    soft_skills_html = _build_skills_html(p.soft_skills or "", [])

    # Experience paragraphs
    experience_html = _nl2br(p.experience or "Professional experience not specified.")
    education_html = _nl2br(p.education or "Education not specified.")
    certs_html = _nl2br(p.certificates or "") if p.certificates else ""
    langs_html = _nl2br(p.languages or "") if p.languages else ""

    # Job tags chips
    tag_chips = "".join(
        f'<span style="background:#f0fdf4;color:#15803d;border:1px solid #bbf7d0;'
        f'padding:3px 10px;border-radius:20px;font-size:12px">{t}</span>'
        for t in j.tags
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>CV – {full_name} | {j.company}</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
      background: #f8fafc;
      color: #1e293b;
      line-height: 1.6;
    }}
    .page {{
      max-width: 860px;
      margin: 40px auto;
      background: #fff;
      border-radius: 16px;
      box-shadow: 0 4px 32px rgba(0,0,0,0.10);
      overflow: hidden;
    }}
    /* Header */
    .header {{
      background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%);
      color: white;
      padding: 48px 48px 36px;
    }}
    .header-name {{
      font-size: 2.4rem;
      font-weight: 700;
      letter-spacing: -0.5px;
    }}
    .header-title {{
      font-size: 1.1rem;
      opacity: 0.85;
      margin-top: 4px;
    }}
    .header-meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      margin-top: 20px;
      font-size: 0.9rem;
      opacity: 0.9;
    }}
    .header-meta span {{ display: flex; align-items: center; gap: 6px; }}
    /* Target job banner */
    .job-banner {{
      background: #eff6ff;
      border-left: 4px solid #2563eb;
      padding: 16px 48px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .job-banner-label {{
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: #2563eb;
    }}
    .job-banner-title {{
      font-size: 1.05rem;
      font-weight: 700;
      color: #1e3a5f;
    }}
    .job-banner-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}
    /* Body */
    .body {{
      display: grid;
      grid-template-columns: 1fr 280px;
      gap: 0;
    }}
    .main {{ padding: 36px 48px; border-right: 1px solid #e2e8f0; }}
    .sidebar {{ padding: 36px 28px; background: #f8fafc; }}
    /* Section */
    .section {{ margin-bottom: 32px; }}
    .section-title {{
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      color: #2563eb;
      border-bottom: 2px solid #bfdbfe;
      padding-bottom: 6px;
      margin-bottom: 14px;
    }}
    p {{ margin-bottom: 10px; font-size: 0.95rem; color: #334155; }}
    /* Print */
    @media print {{
      body {{ background: white; }}
      .page {{ margin: 0; border-radius: 0; box-shadow: none; }}
      .print-btn {{ display: none !important; }}
    }}
    .print-btn {{
      display: block;
      margin: 24px auto;
      padding: 12px 32px;
      background: #2563eb;
      color: white;
      border: none;
      border-radius: 8px;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      font-family: inherit;
    }}
    .print-btn:hover {{ background: #1d4ed8; }}
  </style>
</head>
<body>
  <button class="print-btn" onclick="window.print()">🖨️ Print / Save as PDF</button>

  <div class="page">
    <!-- Header -->
    <div class="header">
      <div class="header-name">{full_name}</div>
      <div class="header-title">{current_title}</div>
      <div class="header-meta">
        {f'<span>📍 {p.location}</span>' if p.location else ''}
        {f'<span>🔗 {p.github_url}</span>' if p.github_url else ''}
        {f'<span>🌐 {p.languages}</span>' if p.languages else ''}
      </div>
    </div>

    <!-- Target job banner -->
    <div class="job-banner">
      <div>
        <div class="job-banner-label">✨ Customized for</div>
        <div class="job-banner-title">{j.title} — {j.company}</div>
        {f'<div style="font-size:0.85rem;color:#64748b;margin-top:2px">📍 {j.location} &nbsp;|&nbsp; Generated {today}</div>' if j.location else f'<div style="font-size:0.85rem;color:#64748b;margin-top:2px">Generated {today}</div>'}
      </div>
      <div class="job-banner-tags">{tag_chips}</div>
    </div>

    <!-- Body -->
    <div class="body">
      <!-- Main column -->
      <div class="main">
        {'<div class="section"><div class="section-title">Professional Summary</div>' + _nl2br(p.long_resume) + '</div>' if p.long_resume else ''}

        <div class="section">
          <div class="section-title">Experience</div>
          {experience_html}
        </div>

        <div class="section">
          <div class="section-title">Education</div>
          {education_html}
        </div>

        {('<div class="section"><div class="section-title">Certifications</div>' + certs_html + '</div>') if certs_html else ''}
      </div>

      <!-- Sidebar -->
      <div class="sidebar">
        <div class="section">
          <div class="section-title">Technical Skills</div>
          {skills_html}
        </div>

        <div class="section">
          <div class="section-title">Soft Skills</div>
          {soft_skills_html}
        </div>

        {('<div class="section"><div class="section-title">Languages</div>' + langs_html + '</div>') if langs_html else ''}

        <div class="section">
          <div class="section-title">About this Position</div>
          <p style="font-size:0.85rem;color:#475569">{(j.description or '')[:300]}{'...' if j.description and len(j.description) > 300 else ''}</p>
        </div>
      </div>
    </div>
  </div>

  <button class="print-btn" onclick="window.print()">🖨️ Print / Save as PDF</button>
</body>
</html>"""

    return GenerateCVResponse(cvContent=html, filename=filename)
