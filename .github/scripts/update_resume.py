import os
import re
import subprocess
from pathlib import Path

def get_latest_rev(resumes_dir):
    pdf_files = list(Path(resumes_dir).glob("*.pdf"))
    revs = []
    for f in pdf_files:
        match = re.search(r'rev-(\d+)', f.name)
        if match:
            revs.append(int(match.group(1)))
    return max(revs) if revs else 0

def get_last_processed():
    try:
        with open('last_processed.txt', 'r') as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0

def extract_text_from_pdf(pdf_path):
    result = subprocess.run(['pdftotext', pdf_path, '-'], capture_output=True, text=True)
    return result.stdout

def parse_resume_text(text):
    lines = text.split('\n')
    sections = {}
    current_section = None
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line in ['Skills', 'Experience', 'Education', 'Licenses & Certificates']:
            current_section = line
            sections[current_section] = []
        elif current_section:
            sections[current_section].append(line)
    return sections

def generate_markdown(sections):
    md = "# Guilherme Lage da Costa\n**Software Engineer | Java | Spring Boot | Python | AWS**\n\n"
    md += "[LinkedIn](https://linkedin.com/in/guilhermeldcosta) | [GitHub](https://github.com/guilhermeldcosta) | guilhermeldcosta@gmail.com | +55 (31) 9 9169-8722\n\n"
    md += "## Summary\nSoftware engineer with a strong background in backend development, specializing in cloud-based solutions. Transitioned from civil engineering to software engineering in 2022.\n\n"
    md += "## Technical Toolkit\n"
    if 'Skills' in sections:
        skills = ' | '.join(sections['Skills'])
        md += f"{skills}\n\n"
    md += "## Professional Experience\n"
    if 'Experience' in sections:
        # Assuming experience is listed, need to parse further, but for simplicity, join
        md += '\n'.join(sections['Experience']) + '\n\n'
    md += "## Education\n"
    if 'Education' in sections:
        md += '\n'.join(sections['Education']) + '\n\n'
    md += "## Licenses & Certificates\n"
    if 'Licenses & Certificates' in sections:
        md += '\n'.join(sections['Licenses & Certificates']) + '\n'
    return md

def main():
    resumes_dir = 'resumes'
    latest_rev = get_latest_rev(resumes_dir)
    last_processed = get_last_processed()
    if latest_rev > last_processed:
        pdf_file = f"resumes/resume-guilherme-costa-en-rev-{latest_rev}.pdf"
        if os.path.exists(pdf_file):
            text = extract_text_from_pdf(pdf_file)
            sections = parse_resume_text(text)
            md_content = generate_markdown(sections)
            with open('index.md', 'w') as f:
                f.write(md_content)
            with open('last_processed.txt', 'w') as f:
                f.write(str(latest_rev))
            print(f"Updated to rev-{latest_rev}")
        else:
            print(f"PDF file for rev-{latest_rev} not found")
    else:
        print("No new resume to process")

if __name__ == "__main__":
    main()
