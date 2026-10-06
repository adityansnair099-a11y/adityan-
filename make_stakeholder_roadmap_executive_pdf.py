import importlib.util
import subprocess
import sys
from pathlib import Path

if importlib.util.find_spec("reportlab") is None:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

source = Path(r"c:\Users\DELL\OneDrive\Desktop\sky blue\stakeholder_roadmap_executive.md")
out = Path(r"c:\Users\DELL\OneDrive\Desktop\sky blue\stakeholder_roadmap_executive.pdf")

with source.open("r", encoding="utf-8") as f:
    lines = f.read().splitlines()

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='ExecTitle', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=18, leading=22, textColor='#1F2A44', spaceAfter=12))
styles.add(ParagraphStyle(name='ExecHeading', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=12, leading=14, textColor='#1F2A44', spaceBefore=10, spaceAfter=6))
styles.add(ParagraphStyle(name='ExecBody', parent=styles['BodyText'], fontName='Helvetica', fontSize=10.5, leading=14, textColor='#222222'))

story = []
for raw in lines:
    line = raw.strip()
    if not line:
        story.append(Spacer(1, 0.12 * inch))
        continue
    if line.startswith('# '):
        story.append(Paragraph(line[2:].upper(), styles['ExecTitle']))
        story.append(Spacer(1, 0.15 * inch))
    elif line.startswith('## '):
        story.append(Paragraph(line[3:], styles['ExecHeading']))
    elif line.startswith('|'):
        story.append(Paragraph(line.replace('|', '  |  '), styles['ExecBody']))
    elif line.startswith('- '):
        story.append(Paragraph('• ' + line[2:], styles['ExecBody']))
    else:
        story.append(Paragraph(line, styles['ExecBody']))

pdf = SimpleDocTemplate(
    str(out),
    pagesize=A4,
    rightMargin=0.75 * inch,
    leftMargin=0.75 * inch,
    topMargin=0.7 * inch,
    bottomMargin=0.7 * inch,
)
pdf.build(story)
print(f"PDF created: {out}")
