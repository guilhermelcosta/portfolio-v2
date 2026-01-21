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

def clean_text(text):
    """Clean up special characters from PDF extraction."""
    # Replace special dash/bullet characters
    text = text.replace('–', '-')
    text = re.sub(r'[•\u2022]', '•', text)
    return text

def parse_resume_text(text):
    """Parse resume preserving all information."""
    text = clean_text(text)
    lines = [line.rstrip() for line in text.split('\n')]
    
    # Extract header
    name = "Guilherme Lage da Costa"
    title = ""
    contact_parts = []
    
    for i, line in enumerate(lines[:10]):
        if "Software Engineer" in line:
            title = line.strip()
        if "LinkedIn" in line or "GitHub" in line or "@" in line or "+55" in line:
            if "LinkedIn" in line:
                contact_parts.append("[LinkedIn](https://linkedin.com/in/guilhermeldcosta)")
            if "GitHub" in line:
                contact_parts.append("[GitHub](https://github.com/guilhermeldcosta)")
            email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', line)
            if email_match:
                contact_parts.append(email_match.group(0))
            phone_match = re.search(r'\+55\s*\(\d+\)\s*\d+\s+\d+\s*\d+-\d+', line)
            if phone_match:
                contact_parts.append(phone_match.group(0))
    
    # Find section boundaries
    section_indices = {}
    for i, line in enumerate(lines):
        if line.strip() == 'Skills':
            section_indices['Skills'] = i
        elif line.strip() == 'Experience':
            section_indices['Experience'] = i
        elif line.strip() == 'Education':
            section_indices['Education'] = i
        elif line.strip() == 'Licenses & Certificates':
            section_indices['Licenses & Certificates'] = i
    
    return {
        'name': name,
        'title': title,
        'contact': contact_parts,
        'lines': lines,
        'section_indices': section_indices
    }

def generate_markdown(parsed_data):
    """Generate markdown with complete information."""
    lines = parsed_data['lines']
    section_indices = parsed_data['section_indices']
    
    md = f"# {parsed_data['name']}\n"
    if parsed_data['title']:
        md += f"**{parsed_data['title']}**\n\n"
    if parsed_data['contact']:
        md += " | ".join(parsed_data['contact']) + "\n\n"
    
    # Skills section
    if 'Skills' in section_indices and 'Experience' in section_indices:
        md += "## Skills\n"
        skills_lines = []
        for i in range(section_indices['Skills'] + 1, section_indices['Experience']):
            line = lines[i].strip()
            if line:
                skills_lines.append(line)
        md += ' '.join(skills_lines) + "\n\n"
    
    # Experience section
    if 'Experience' in section_indices and 'Education' in section_indices:
        md += "## Experience\n\n"
        i = section_indices['Experience'] + 1
        end = section_indices['Education']
        
        while i < end:
            line = lines[i].strip()
            
            # Skip empty lines
            if not line:
                i += 1
                continue
            
            # Company name (non-empty, non-bullet line)
            if not line.startswith('•'):
                company = line
                i += 1
                
                # Skip empty lines
                while i < end and not lines[i].strip():
                    i += 1
                
                # Location
                location = lines[i].strip() if i < end else ""
                if location and not location.startswith('•'):
                    i += 1
                else:
                    location = ""
                
                # Skip empty lines
                while i < end and not lines[i].strip():
                    i += 1
                
                # Position
                position = lines[i].strip() if i < end and not lines[i].strip().startswith('•') else ""
                if position:
                    i += 1
                else:
                    position = ""
                
                # Skip empty lines
                while i < end and not lines[i].strip():
                    i += 1
                
                # Dates
                dates = lines[i].strip() if i < end and re.search(r'\d{2}/\d{4}', lines[i]) else ""
                if dates:
                    i += 1
                
                # Write company header
                md += f"### {company}"
                if location:
                    md += f" | {location}"
                md += "\n"
                if position:
                    md += f"**{position}**"
                    if dates:
                        md += f" | {dates}"
                    md += "\n\n"
                
                # Collect bullet points (may span multiple lines)
                while i < end:
                    # Skip empty lines
                    while i < end and not lines[i].strip():
                        i += 1
                    
                    if i >= end:
                        break
                    
                    line = lines[i].strip()
                    
                    # If it's a bullet point
                    if line.startswith('•'):
                        i += 1
                        # Skip empty line after bullet
                        while i < end and not lines[i].strip():
                            i += 1
                        
                        # Collect the bullet text (may span multiple lines)
                        bullet_text = []
                        while i < end:
                            text_line = lines[i].strip()
                            if not text_line or text_line.startswith('•'):
                                break
                            # Check if it's the next company/position (all caps or specific pattern)
                            if text_line and not text_line.endswith(';') and not text_line.endswith('.') and not text_line.endswith(','):
                                # Might be next section, check context
                                if i + 1 < end and lines[i + 1].strip() in ['Remote', 'Belo Horizonte, MG', ''] or re.match(r'\d{2}/\d{4}', lines[i + 2].strip() if i + 2 < end else ''):
                                    break
                            bullet_text.append(text_line)
                            i += 1
                        
                        if bullet_text:
                            md += f"- {' '.join(bullet_text)}\n"
                    else:
                        # Not a bullet, might be next company
                        break
                
                md += "\n"
            else:
                i += 1
    
    # Education section
    if 'Education' in section_indices and 'Licenses & Certificates' in section_indices:
        md += "## Education\n\n"
        i = section_indices['Education'] + 1
        end = section_indices['Licenses & Certificates']
        
        # Find institution
        institution = ""
        location = ""
        while i < end and not lines[i].strip():
            i += 1
        if i < end:
            institution = lines[i].strip()
            i += 1
        
        while i < end and not lines[i].strip():
            i += 1
        if i < end and ('Belo Horizonte' in lines[i] or ', MG' in lines[i]):
            location = lines[i].strip()
            i += 1
        
        if institution:
            md += f"### {institution}"
            if location:
                md += f" | {location}"
            md += "\n\n"
        
        # Collect degrees
        while i < end:
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            
            if line.startswith("Bachelor's degree") or line.startswith("Postgraduate") or line.startswith("Master"):
                degree = line
                i += 1
                
                # Skip empty lines
                while i < end and not lines[i].strip():
                    i += 1
                
                # Get dates
                dates = ""
                if i < end and re.match(r'\d{2}/\d{4}', lines[i].strip()):
                    dates = lines[i].strip()
                    i += 1
                
                md += f"- **{degree}**"
                if dates:
                    md += f" | {dates}"
                md += "\n"
            else:
                i += 1
        
        md += "\n"
    
    # Licenses & Certificates section
    if 'Licenses & Certificates' in section_indices:
        md += "## Licenses & Certificates\n\n"
        i = section_indices['Licenses & Certificates'] + 1
        end = len(lines)
        
        while i < end:
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            
            # Certificate name
            if ',' not in line or (line.startswith('System') or line.startswith('Google')):
                cert_name = line
                i += 1
                
                # Skip empty lines
                while i < end and not lines[i].strip():
                    i += 1
                
                # Issuer and date
                issuer_date = ""
                if i < end and ',' in lines[i].strip():
                    issuer_date = lines[i].strip()
                    i += 1
                
                md += f"- **{cert_name}**"
                if issuer_date:
                    md += f" | {issuer_date}"
                md += "\n"
            else:
                i += 1
    
    return md

def main():
    resumes_dir = 'resumes'
    latest_rev = get_latest_rev(resumes_dir)
    last_processed = get_last_processed()
    if latest_rev > last_processed:
        pdf_file = f"resumes/resume-guilherme-costa-en-rev-{latest_rev}.pdf"
        if os.path.exists(pdf_file):
            text = extract_text_from_pdf(pdf_file)
            parsed_data = parse_resume_text(text)
            md_content = generate_markdown(parsed_data)
            with open('index.md', 'w', encoding='utf-8') as f:
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
