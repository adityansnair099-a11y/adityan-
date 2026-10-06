import importlib.util
import subprocess
import sys
from pathlib import Path


def ensure_reportlab():
    if importlib.util.find_spec("reportlab") is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])


ensure_reportlab()

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

source_path = Path(r"c:\Users\DELL\OneDrive\Desktop\sky blue\business_analyst_roadmap.md")
out_path = Path(r"c:\Users\DELL\OneDrive\Desktop\sky blue\business_analyst_roadmap.pdf")

with source_path.open("r", encoding="utf-8") as f:
    lines = f.read().splitlines()

styles = getSampleStyleSheet()
body = styles["BodyText"]
body.fontName = "Helvetica"
body.fontSize = 11
body.leading = 16

story = []
for raw_line in lines:
    line = raw_line.strip()
    if not line:
        story.append(Spacer(1, 0.15 * inch))
        continue
    if line.startswith("# "):
        title = Paragraph(line[2:].upper(), styles["Title"])
        story.append(title)
        story.append(Spacer(1, 0.2 * inch))
    elif line.startswith("## "):
        heading = Paragraph(line[3:], styles["Heading2"])
        story.append(heading)
        story.append(Spacer(1, 0.12 * inch))
    elif line.startswith("- "):
        story.append(Paragraph("• " + line[2:], body))
    else:
        story.append(Paragraph(line, body))

pdf = SimpleDocTemplate(
    str(out_path),
    pagesize=A4,
    rightMargin=0.7 * inch,
    leftMargin=0.7 * inch,
    topMargin=0.7 * inch,
    bottomMargin=0.7 * inch,
)
pdf.build(story)
print(f"PDF created: {out_path}")
