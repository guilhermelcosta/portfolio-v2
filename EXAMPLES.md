# Usage Examples

## Valid Resume Filename Patterns

The script accepts any PDF file that:
- Starts with "resume"
- Ends with "rev-N.pdf" (where N is a version number)

### Valid Examples

```
resume-rev-1.pdf
resume-rev-2.pdf
resume-john-smith-rev-3.pdf
resume-guilherme-costa-en-rev-4.pdf
resume-software-engineer-2024-rev-5.pdf
resume_backup_rev-6.pdf
```

### Invalid Examples

```
cv-guilherme-rev-1.pdf          ❌ Must start with "resume"
resume-guilherme.pdf             ❌ Must end with "rev-N.pdf"
resume-guilherme-v1.pdf          ❌ Must use "rev-N" format (not "v1")
resume-guilherme-revision-1.pdf  ❌ Must use "rev-N" format
```

## Workflow Example

### Initial Setup

```bash
# Add your first resume
cp ~/Documents/my-resume.pdf resumes/resume-rev-1.pdf
git add resumes/
git commit -m "Initial resume"
git push
```

### Updating Your Resume

```bash
# Add updated version
cp ~/Documents/my-updated-resume.pdf resumes/resume-rev-2.pdf
git add resumes/
git commit -m "Update resume rev-2"
git push
```

### Using Descriptive Names

```bash
# You can include descriptive text in the middle
cp ~/Documents/cv.pdf resumes/resume-guilherme-costa-2024-rev-3.pdf
git add resumes/
git commit -m "Add resume rev-3"
git push
```

## What Happens After Push

1. GitHub Actions detects the push to `resumes/`
2. Script finds the highest revision number (e.g., rev-3)
3. Compares with `last_processed.txt` (e.g., contains "2")
4. Since 3 > 2, processes the new file
5. Extracts text from PDF
6. Generates `index.md` with formatted content
7. Updates `last_processed.txt` to "3"
8. Commits changes
9. Builds Jekyll site
10. Deploys to GitHub Pages

## Checking Results

After the workflow completes:

1. **Check the workflow**: Go to Actions tab, verify "Update Resume and Deploy" completed
2. **View generated Markdown**: Open `index.md` in the repository
3. **Visit your site**: Navigate to `https://<username>.github.io/portfolio-v2/`

## Version Management

The script automatically handles versions:

```
last_processed.txt contains: 2

resumes/ contains:
  - resume-rev-1.pdf
  - resume-rev-2.pdf
  - resume-rev-3.pdf

Result: Processes resume-rev-3.pdf (highest unprocessed version)
```

### Skipping Processing

If you add an older version, it won't be processed:

```
last_processed.txt contains: 5

You add: resume-rev-3.pdf

Result: No processing (3 < 5)
```

### Force Reprocessing

To reprocess a specific version:

1. Edit `last_processed.txt` to a lower number
2. Commit and push
3. Workflow will reprocess the latest version

```bash
echo "2" > last_processed.txt
git add last_processed.txt
git commit -m "Force reprocess latest resume"
git push
```
