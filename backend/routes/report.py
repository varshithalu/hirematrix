# routes/report.py

from fastapi import APIRouter
from database.queries import get_user_evaluations
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from fastapi.responses import StreamingResponse
import io
from datetime import datetime
from typing import Sequence, Dict, Any, List

router = APIRouter()


@router.get("/report/{user_id}")
def generate_report(user_id: str):

    evaluations: List[Any] = get_user_evaluations(user_id)

    if not evaluations:
        return {"error": "No evaluations found"}

    # You may fetch name/experience from resumes table if needed
    candidate_name = "Candidate"
    experience_level = "Not Specified"

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    elements = []
    styles = getSampleStyleSheet()

    # -------- Branding Header --------
    elements.append(Paragraph("<b>TalentScout AI Hiring Assistant</b>", styles["Title"]))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("Technical Assessment Report", styles["Heading2"]))
    elements.append(Spacer(1, 0.3 * inch))

    # -------- Candidate Info --------
    today = datetime.now().strftime("%d %B %Y")

    elements.append(Paragraph(f"<b>Candidate Name:</b> {candidate_name}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Experience Level:</b> {experience_level}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Date:</b> {today}", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    # -------- Score Calculation --------
    total_score = 0
    total_questions = len(evaluations)

    for e in evaluations:
        total_score += float(e.get("score", 0))

    avg_score = round(total_score / total_questions, 2)
    percentage = round((avg_score / 10) * 100, 2)

    # Recommendation Band
    if avg_score >= 8:
        recommendation = "Strong Candidate"
    elif avg_score >= 6:
        recommendation = "Moderate Candidate"
    else:
        recommendation = "Needs Improvement"

    elements.append(Paragraph(f"<b>Total Questions:</b> {total_questions}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Average Score:</b> {avg_score} / 10", styles["Normal"]))
    elements.append(Paragraph(f"<b>Percentage:</b> {percentage}%", styles["Normal"]))
    elements.append(Paragraph(f"<b>Recommendation:</b> {recommendation}", styles["Normal"]))
    elements.append(Spacer(1, 0.4 * inch))

    # -------- Score Breakdown Table --------
    table_data = [["Question (Truncated)", "Score"]]

    for e in evaluations:
        question = str(e.get("question", ""))[:60] + "..."
        score = str(e.get("score", 0))
        table_data.append([question, score])

    table = Table(table_data, colWidths=[4.5 * inch, 1 * inch])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
    ]))

    elements.append(table)

    # -------- Build PDF --------
    doc.build(elements)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=assessment_report.pdf"
        }
    )