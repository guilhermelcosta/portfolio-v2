# Portfolio - Automated Resume Converter

Automated system that converts PDF resumes to Markdown and publishes them via GitHub Pages.

## Overview

This repository automatically processes resume PDFs, extracts their content, converts to Markdown format, and publishes the result to GitHub Pages using Jekyll.

### Features

- Automatic PDF text extraction and parsing
- Intelligent detection of multiple positions at the same company
- Preservation of all resume information and formatting
- Single consolidated workflow (update + deploy)
- Version tracking to avoid reprocessing
- Flexible file naming (any file starting with "resume" and ending with "rev-N.pdf")

## Quick Start

```bash
# Add your resume (use any name that matches the pattern)
cp ~/path/to/cv.pdf resumes/resume-yourname-rev-1.pdf
git add resumes/
git commit -m "Add resume rev-1"
git push
```

That's it! The workflow handles the rest.

See [EXAMPLES.md](EXAMPLES.md) for more usage examples and naming patterns.

## Project Structure

```
portfolio-v2/
├── .github/
│   ├── workflows/
│   │   └── update-resume.yml          # Consolidated workflow
│   └── scripts/
│       └── update_resume.py           # PDF to Markdown converter
├── resumes/
│   └── resume*-rev-N.pdf              # Resume PDFs (versioned)
├── _config.yml                        # Jekyll configuration
├── index.md                           # Generated Markdown (auto-updated)
└── last_processed.txt                 # Version tracking file
```

## Usage

### Adding a New Resume

1. Create your resume PDF with naming pattern: `resume*-rev-N.pdf`
   - Must start with "resume"
   - Must end with "rev-N.pdf" where N is the version number
   - Example: `resume-guilherme-costa-en-rev-4.pdf`

2. Add the file to the `resumes/` directory:
   ```bash
   cp ~/path/to/your-resume.pdf resumes/resume-yourname-rev-4.pdf
   ```

3. Commit and push:
   ```bash
   git add resumes/
   git commit -m "Add resume rev-4"
   git push
   ```

4. The workflow automatically:
   - Detects the new version
   - Extracts content from the PDF
   - Updates `index.md`
   - Builds and deploys to GitHub Pages

### Viewing Your Portfolio

After deployment completes, your portfolio is available at:
```
https://<username>.github.io/portfolio-v2/
```

## Configuration

### GitHub Pages Setup

Required configuration (should already be set):

1. Go to repository Settings → Pages
2. Set source to "GitHub Actions"
3. Ensure Actions are enabled in Settings → Actions

### Theme Customization

Edit `_config.yml` to change Jekyll theme:
```yaml
theme: jekyll-theme-<theme-name>
```

Available themes: minimal, cayman, slate, modernist, architect, etc.

## Script Details

### PDF Processing

The Python script (`update_resume.py`) performs:

- **Version Detection**: Scans `resumes/` for files matching `resume*-rev-N.pdf` pattern
- **Text Extraction**: Uses `pdftotext` to extract raw content
- **Parsing**: Identifies sections (Skills, Experience, Education, Certificates)
- **Multi-Position Handling**: Detects and formats multiple roles at the same company
- **Markdown Generation**: Creates properly formatted output with links

### Version Tracking

- `last_processed.txt` stores the last processed version number
- Only newer versions trigger processing
- Prevents unnecessary workflow runs

## Workflow Execution

Single workflow handles complete pipeline:

1. **Trigger**: Push to `master` branch with changes in `resumes/**`
2. **Update Phase**: Extract PDF, generate Markdown, commit changes
3. **Deploy Phase**: Build with Jekyll, deploy to GitHub Pages

## Troubleshooting

### Workflow Not Running

- Verify push is to `master` branch
- Check file is in `resumes/` directory
- Confirm filename matches pattern `resume*-rev-N.pdf`
- Ensure GitHub Actions is enabled

### No Content Update

- Verify version number (N) is greater than value in `last_processed.txt`
- Check workflow logs in Actions tab for errors
- Ensure PDF is readable and not corrupted

### Deploy Failures

- Confirm GitHub Pages source is set to "GitHub Actions"
- Check workflow has required permissions (Settings → Actions → Workflow permissions)
- Review deployment logs in Actions tab

## Requirements

The workflow automatically installs:
- Python 3.9+
- poppler-utils (for pdftotext)
- pandoc

## License

Personal portfolio project.
