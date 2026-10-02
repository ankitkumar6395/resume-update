
from pathlib import Path
import json
import subprocess
from jinja2 import Template
from xhtml2pdf import pisa

repo = Path(__file__).resolve().parent

# Load resume data and template
with open(repo / "resume.json", encoding="utf-8") as f:
    resume_data = json.load(f)

with open(repo / "resume_template.html", encoding="utf-8") as f:
    template = Template(f.read())

# Generate website HTML
html_output = template.render(**resume_data)
(repo / "index.html").write_text(html_output, encoding="utf-8")

# Generate PDF
with open(repo / "resume.pdf", "wb") as f:
    result = pisa.CreatePDF(html_output, dest=f)

if result.err:
    raise RuntimeError("PDF generation failed")

# Publish changes to GitHub
subprocess.run(
    ["git", "add", "index.html", "resume.pdf"],
    cwd=repo, check=True
)

changed = subprocess.run(
    ["git", "diff", "--cached", "--quiet"],
    cwd=repo
)

if changed.returncode == 0:
    print("No changes to publish.")
else:
    subprocess.run(
        ["git", "commit", "-m", "Update resume"],
        cwd=repo, check=True
    )
    subprocess.run(
        ["git", "push", "origin", "main"],
        cwd=repo, check=True
    )
    print("Changes pushed to GitHub!")

print("Resume generated successfully!")
