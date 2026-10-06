import importlib.util
import subprocess
import sys
from pathlib import Path

if importlib.util.find_spec("reportlab") is None:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

source = Path(r"c:\Users\DELL\OneDrive\Desktop\sky blue\stakeholder_roadmap.md")
out = Path(r"c:\Users\DELL\OneDrive\Desktop\sky blue\stakeholder_roadmap.pdf")

with source.open("r", encoding="utf-8") as f:
    lines = f.read().splitlines()

styles = getSampleStyleSheet()
body = styles["BodyText"]
body.fontName = "Helvetica"
body.fontSize = 11
body.leading = 16

story = []
for raw in lines:
    line = raw.strip()
    if not line:
        story.append(Spacer(1, 0.12 * inch))
    elif line.startswith("# "):
        story.append(Paragraph(line[2:].upper(), styles["Title"]))
        story.append(Spacer(1, 0.18 * inch))
    elif line.startswith("## "):
        story.append(Paragraph(line[3:], styles["Heading2"]))
        story.append(Spacer(1, 0.10 * inch))
    elif line.startswith("|"):
        story.append(Paragraph(line.replace("|", "  |  "), body))
    elif line.startswith("-"):
        story.append(Paragraph("• " + line[1:].strip(), body))
    else:
        story.append(Paragraph(line, body))

pdf = SimpleDocTemplate(
    str(out),
    pagesize=A4,
    rightMargin=0.7 * inch,
    leftMargin=0.7 * inch,
    topMargin=0.7 * inch,
    bottomMargin=0.7 * inch,
)
pdf.build(story)
print(f"PDF created: {out}")
