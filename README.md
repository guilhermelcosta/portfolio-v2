# Portfolio - Automated Resume Converter

Automated system that converts PDF resumes to Markdown and publishes them via GitHub Pages.

## Overview

This repository automatically processes resume PDFs, extracts their content, converts to Markdown format, and publishes the result to GitHub Pages using Jekyll. The pipeline is split in two stages: an `update/**` branch generates the Markdown and opens a pull request, and merging that pull request into `master` triggers the deploy.

### Features

- Automatic PDF text extraction and parsing
- Intelligent detection of multiple positions at the same company
- Preservation of all resume information and formatting
- Branch-based workflow: pushing to `update/**` generates the Markdown and opens a PR to `master`
- Deploy to GitHub Pages happens only on merge to `master`
- Always processes the highest `rev-N` file found in `resumes/`
- Flexible file naming (any file starting with "resume" and ending with "rev-N.pdf")

## Quick Start

```bash
# Create an update branch
git checkout -b update/new-resume

# Add your resume (use any name that matches the pattern)
cp ~/path/to/cv.pdf resumes/resume-yourname-rev-2.pdf
git add resumes/
git commit -m "Add resume rev-2"
git push -u origin update/new-resume
```

The workflow generates `index.md` on that branch and opens a pull request to `master`. Merge the PR to deploy.

See [EXAMPLES.md](EXAMPLES.md) for more usage examples and naming patterns. 

## Project Structure

```
portfolio-v2/
├── .github/
│   ├── workflows/
│   │   ├── update-resume.yml          # Runs on update/** pushes, opens PR to master
│   │   └── deploy-pages.yml           # Runs on master pushes (merges), deploys to Pages
│   └── scripts/
│       └── update_resume.py           # PDF to Markdown converter
├── resumes/
│   └── resume*-rev-N.pdf              # Resume PDFs (versioned)
├── _config.yml                        # Jekyll configuration
└── index.md                           # Generated Markdown (auto-updated)
```

## Usage

### Adding a New Resume

1. Create a branch named `update/<anything>`, for example `update/rev-2` or `update/review`:
   ```bash
   git checkout -b update/rev-2
   ```

2. Create your resume PDF with naming pattern: `resume*-rev-N.pdf`
   - Must start with "resume"
   - Must end with "rev-N.pdf" where N is the version number
   - Example: `resume-guilherme-costa-en-rev-4.pdf`

3. Add the file to the `resumes/` directory and push the branch:
   ```bash
   cp ~/path/to/your-resume.pdf resumes/resume-yourname-rev-4.pdf
   git add resumes/
   git commit -m "Add resume rev-4"
   git push -u origin update/rev-2
   ```

4. The `update-resume` workflow automatically:
   - Finds the highest `rev-N` file in `resumes/`
   - Extracts content from the PDF
   - Updates `index.md` and commits it to the `update/**` branch
   - Opens a pull request to `master`

5. Review and merge the pull request. Merging into `master` triggers the `deploy-pages` workflow, which builds and deploys the site.

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

- **Version Detection**: Scans `resumes/` for files matching `resume*-rev-N.pdf` pattern and picks the highest `N`
- **Text Extraction**: Uses `pdftotext` to extract raw content
- **Parsing**: Identifies sections (Skills, Experience, Education, Certificates)
- **Multi-Position Handling**: Detects and formats multiple roles at the same company
- **Markdown Generation**: Creates properly formatted output with links

There is no version tracking file anymore, the script always regenerates `index.md` from the highest `rev-N` PDF present in `resumes/` whenever it runs.

## Workflow Execution

Two workflows split the pipeline:

1. **`update-resume.yml`**
   - **Trigger**: Push to any branch matching `update/**`
   - Extracts the highest-rev PDF, generates `index.md`, commits it to that branch
   - Opens a pull request targeting `master`

2. **`deploy-pages.yml`**
   - **Trigger**: Push to `master` (i.e. when the PR above is merged)
   - Builds the site with Jekyll and deploys it to GitHub Pages

## Troubleshooting

### Update Workflow Not Running

- Verify the branch name matches the pattern `update/**` (e.g. `update/rev-2`, `update/review`)
- Check the PDF is in the `resumes/` directory
- Confirm filename matches pattern `resume*-rev-N.pdf`
- Ensure GitHub Actions is enabled

### No Content Update

- Confirm the pushed PDF actually has the highest `rev-N` among files in `resumes/`
- Check workflow logs in Actions tab for errors
- Ensure PDF is readable and not corrupted

### Pull Request Not Opened

- Check the `update-resume` workflow logs; if a PR already exists for that branch, creation is skipped instead of failing
- Confirm the workflow has `pull-requests: write` permission (Settings → Actions → Workflow permissions)

### Deploy Failures

- Confirm GitHub Pages source is set to "GitHub Actions"
- Check the `deploy-pages` workflow has required permissions (Settings → Actions → Workflow permissions)
- Review deployment logs in Actions tab

## Requirements

The `update-resume` workflow automatically installs:
- Python 3.9+
- poppler-utils (for pdftotext)
- pandoc

## License

Personal portfolio project.
