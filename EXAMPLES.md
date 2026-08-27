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

## Valid Branch Names

The `update-resume` workflow triggers on any push to a branch matching `update/**`:

### Valid Examples

```
update/new-resume
update/rev-4
update/review
update/2024-refresh
```

### Invalid Examples

```
feature/new-resume   ❌ Must start with "update/"
updates/rev-4         ❌ Must be exactly "update/", not "updates/"
resume-update         ❌ Must use the "update/<name>" branch format
```

## Workflow Example

### Initial Setup

```bash
# Create an update branch
git checkout -b update/rev-1

# Add your first resume
cp ~/Documents/my-resume.pdf resumes/resume-rev-1.pdf
git add resumes/
git commit -m "Initial resume"
git push -u origin update/rev-1
```

This opens a pull request to `master`. Merge it to deploy.

### Updating Your Resume

```bash
git checkout -b update/rev-2

# Add updated version
cp ~/Documents/my-updated-resume.pdf resumes/resume-rev-2.pdf
git add resumes/
git commit -m "Update resume rev-2"
git push -u origin update/rev-2
```

### Using Descriptive Names

```bash
git checkout -b update/2024-refresh

# You can include descriptive text in the middle
cp ~/Documents/cv.pdf resumes/resume-guilherme-costa-2024-rev-3.pdf
git add resumes/
git commit -m "Add resume rev-3"
git push -u origin update/2024-refresh
```

## What Happens After Push

1. GitHub Actions detects the push to a branch matching `update/**`
2. Script scans `resumes/` and finds the highest revision number (e.g., rev-3)
3. Extracts text from the PDF
4. Generates `index.md` with formatted content
5. Commits `index.md` to the same `update/**` branch
6. Opens a pull request from that branch to `master`
7. On merge to `master`, the `deploy-pages` workflow builds with Jekyll and deploys to GitHub Pages

## Checking Results

After pushing an `update/**` branch:

1. **Check the workflow**: Go to Actions tab, verify "Update Resume and Open PR" completed
2. **Review the PR**: Open the pull request created against `master` and check the generated `index.md`
3. **Merge the PR**: Merging triggers "Deploy to GitHub Pages"
4. **Visit your site**: After the deploy workflow finishes, navigate to `https://<username>.github.io/portfolio-v2/`

## Version Handling

There is no tracking file anymore. Every time the `update-resume` workflow runs, it scans all PDFs in `resumes/` and regenerates `index.md` from the one with the highest `rev-N`, regardless of what was processed before.

```
resumes/ contains:
  - resume-rev-1.pdf
  - resume-rev-2.pdf
  - resume-rev-3.pdf

Result: Always processes resume-rev-3.pdf (highest rev present)
```

### Reprocessing the Same Resume

Since there is no tracking file to compare against, you can force a reprocess at any time by pushing an empty commit (or any change) to an `update/**` branch:

```bash
git checkout -b update/reprocess
git commit --allow-empty -m "Reprocess latest resume"
git push -u origin update/reprocess
```

### Adding an Older Revision

If you add a PDF with a lower `rev-N` than an existing one, it will simply be ignored, the script always picks the highest number present in `resumes/`:

```
resumes/ contains:
  - resume-rev-5.pdf

You add: resume-rev-3.pdf

Result: resume-rev-5.pdf is still processed (3 < 5)
```
