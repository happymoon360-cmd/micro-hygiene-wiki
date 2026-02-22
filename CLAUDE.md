# Micro-Hygiene Wiki - Agent Rules

## Project Overview

Community-driven hygiene tips wiki. Stack: Django REST + React TypeScript (Vite).
- Backend: `backend/` (Django 6 + DRF)
- Frontend: `frontend/` (React 18 + TypeScript + Vite)
- Deploy: Render (backend) + Vercel (frontend)
- Tip descriptions support **Markdown** (rendered via `react-markdown`)

---

## Two-Agent Content Pipeline

This project uses two AI agents working in sequence to expand wiki content daily.

```
OpenCode (Writer)  →  drafts/  →  Antigravity (Artist)  →  production
```

---

## Agent 1: OpenCode (Content Writer)

**Role:** Research, write wiki articles, and prepare image prompts.
**Frequency:** 1 new article per day.

### What OpenCode Does

1. Research a hygiene topic from Reddit (r/CleaningTips, r/Hygiene, r/LifeProTips, r/AskDocs), or other internet sources
2. Write a full wiki article in **Markdown format** with inline image placeholders (image-first format)
3. Write image generation prompts for each placeholder
4. Save as a draft file for Antigravity to process

### Step 1: Pick a Topic

- Check `backend/apps/wiki/fixtures/tips_data.py` for existing topics to avoid duplicates
- Check `content/drafts/` for pending drafts to avoid conflicts
- Choose a topic that fills a gap in the current categories

### Step 2: Write the Draft

Create a new file: `content/drafts/{slug}.md`

**Draft format:**

```markdown
---
title: "How to [action] [subject]"
slug: "how-to-action-subject"
category: "Hand Hygiene"
---

Introduction paragraph explaining why this matters. 2-3 sentences.

## Why This Is Important

Explain the health/science background. Evidence-based content.

![image-1](PROMPT: A clean, minimal flat illustration showing a person washing hands under running water. Style: modern flat design, soft pastel light blue and white colors, white background, simple shapes, no text, no watermark.)

## How to Do It

### Step 1: [First step]

Detailed instructions for step 1.

### Step 2: [Second step]

Detailed instructions for step 2.

![image-2](PROMPT: A clean, minimal flat illustration showing soap lather covering both hands. Style: modern flat design, soft pastel light blue and white colors, white background, simple shapes, no text, no watermark.)

### Step 3: [Third step]

Detailed instructions for step 3.

## Common Mistakes to Avoid

- Mistake 1: explanation
- Mistake 2: explanation

## Pro Tips

> Quote or highlight key insight from community/research.

- Additional tip 1
- Additional tip 2
```

### Draft Rules

1. **Title**: Always start with "How to"
2. **Length**: 700-1200 words (not counting image placeholders)
3. **Structure**: Use H2 (`##`) for main sections, H3 (`###`) for subsections
4. **Images**: Place 8-14 `![image-N](PROMPT: ...)` placeholders. Target one image per major step.
5. **Image prompts**: Must be detailed enough for Antigravity to generate consistent tutorial visuals. Always include style instructions.
6. **Tone**: Friendly, actionable, evidence-based. Say "may help" not "will cure"
7. **No duplicates**: Check existing content first
8. **English only**
9. **wikiHow-level structure**: Use Method/Part sections and numbered steps with short, actionable language.
10. **Per-step clarity**: Each step should explain action + reason + what to avoid.
11. **Secondary verification required**: Validate community tips against institutional guidance before publishing.
12. **Trustworthy references**: Include 3+ links from official sources (CDC, WHO, NHS, ACOG, AAD, NIH/NHLBI, etc.).

### wikiHow-Level Quality Bar (Required)

Use this checklist before saving a draft:

- 2-3 methods or parts (`## Method 1 of 3`, etc.)
- 10-14 total steps across all methods (`### Step N: ...`)
- At least 1 image prompt per step (8+ prompts minimum)
- Safety framing: when to stop, when to ask staff/professional help
- Skimmable bullets for mistakes, quick checks, and pro tips
- References section with practical, non-medical hygiene sources when available

### Reliability Rules (Required)

- Treat Reddit/Quora findings as starting points, not final truth.
- Cross-check each article with authoritative sources before finalizing.
- If sources conflict, prioritize institutional guidance.
- Use conservative wording: "may help", "can reduce risk", "is associated with".
- Avoid medical diagnosis or cure claims.
- Add escalation guidance for warning signs.

### Image Prompt Template for OpenCode

When writing `PROMPT:` placeholders, follow this template:

```
PROMPT: Instructional illustration for a hygiene tutorial. Scene: [specific scene/action], [key object], [environment], [camera framing]. Subject details: [hands/face/tools], [pose/action], [clean context], [neutral expression]. Style lock: unified wiki visual system v1. Modern flat editorial illustration, soft pastel blue-green palette, rounded geometry, subtle shading, bright high-key lighting, very light neutral background, consistent character proportions, clean medical-hygiene tone. Composition: clear focal point, no clutter, no text overlay, no logos, no watermark. Quality: high clarity, educational, beginner-friendly, consistent with previous steps.
```

Use the same style lock text in every prompt to keep image style consistent across all posts.

**Color palette by category (optional accent only):**
| Category | Primary | Accent |
|----------|---------|--------|
| Hand Hygiene | light blue | white |
| Oral Hygiene | mint green | white |
| Body Hygiene | lavender | soft pink |
| Facial Hygiene | peach | coral |
| Hair Hygiene | warm brown | gold |
| Nail Hygiene | soft pink | white |
| Intimate Hygiene | light purple | white |
| Environmental Hygiene | sage green | light brown |
| Sleep Hygiene | dark blue | indigo |
| Food Hygiene | warm yellow | orange |
| Travel Hygiene | sky blue | light green |

Note: Keep the style lock unchanged across all prompts. Category colors are optional accents only.

### Available Categories

```
Hand Hygiene, Oral Hygiene, Body Hygiene, Facial Hygiene,
Hair Hygiene, Nail Hygiene, Intimate Hygiene, Environmental Hygiene,
Sleep Hygiene, Food Hygiene, Travel Hygiene
```

New categories can be added to `CATEGORIES` in `tips_data.py` if needed.

### Antigravity Parsing Rule (Strict)

Antigravity extracts prompt lines from this exact pattern:

`![image-N](PROMPT: ... )`

Keep each prompt in one Markdown image line. Do not split prompt text across multiple lines.

---

## Agent 2: Antigravity (Image Generator & Publisher)

**Role:** Generate images from OpenCode's prompts, then publish the article.
**Trigger:** When a new file appears in `content/drafts/`.

### What Antigravity Does

1. Read the draft file from `content/drafts/{slug}.md`
2. Extract all `PROMPT:` placeholders
3. Generate images using Gemini image generation
4. Save images and replace placeholders with actual image paths
5. Move the finished article to production

### Step 1: Read the Draft

Open `content/drafts/{slug}.md` and parse:
- Frontmatter (title, slug, category)
- All `![image-N](PROMPT: ...)` lines

### Step 2: Generate Images

For each `PROMPT:` placeholder:

1. Extract the prompt text after `PROMPT: `
2. Generate image using Gemini
3. Save as: `frontend/public/images/tips/{slug}-{N}.png`
   - Example: `frontend/public/images/tips/how-to-wash-hands-properly-1.png`
4. **Image requirements:**
   - Size: 800x600px (landscape)
   - Format: PNG
   - No text or watermarks

### Step 3: Build the Final Markdown

Replace all `![image-N](PROMPT: ...)` with actual image paths:

```markdown
<!-- Before (OpenCode wrote this) -->
![image-1](PROMPT: A clean, minimal flat illustration showing...)

<!-- After (Antigravity replaces with this) -->
![Washing hands under running water](/images/tips/how-to-wash-hands-properly-1.png)
```

**Important:** Replace the `PROMPT: ...` with a descriptive alt text, not the prompt itself.

### Step 4: Add to Seed Data

Append to `backend/apps/wiki/fixtures/tips_data.py`:

```python
{
    "title": "How to ...",         # from frontmatter
    "slug": "how-to-...",          # from frontmatter
    "description": "...",           # the full final markdown (with image paths, without frontmatter)
    "category": "Hand Hygiene",     # from frontmatter
},
```

### Step 5: Load into Database

```bash
cd backend
./venv/bin/python manage.py shell -c "
from apps.wiki.fixtures.tips_data import TIPS_DATA, CATEGORIES
from apps.wiki.models import Category, Tip

for cat_name in CATEGORIES:
    Category.objects.get_or_create(name=cat_name, defaults={'slug': cat_name.lower().replace(' ', '-')})

for tip_data in TIPS_DATA:
    cat = Category.objects.get(name=tip_data['category'])
    Tip.objects.update_or_create(
        slug=tip_data['slug'],
        defaults={
            'title': tip_data['title'],
            'description': tip_data['description'],
            'category': cat,
        }
    )
"
```

### Step 6: Move Draft to Published

```bash
mv content/drafts/{slug}.md content/published/{slug}.md
```

---

## Directory Structure for Content Pipeline

```
content/
├── drafts/           # OpenCode writes here (pending Antigravity processing)
│   └── {slug}.md     # Draft with PROMPT: placeholders
├── published/        # Antigravity moves finished articles here
│   └── {slug}.md     # Final article with real image paths
```

Images go to: `frontend/public/images/tips/{slug}-{N}.png`

---

## Code Conventions

- Backend: Python, Django REST Framework, pytest for tests
- Frontend: TypeScript strict, React functional components, Vitest
- CSS: Component-scoped CSS files (no CSS-in-JS)
- Tip descriptions: **Markdown format** (rendered by `react-markdown` in TipDetailPage)
- API responses: snake_case
- URLs: kebab-case slugs
- Commits: `feat:`, `fix:`, `docs:`, `chore:` prefixes

## Key File Paths

| What | Path |
|------|------|
| Tip seed data | `backend/apps/wiki/fixtures/tips_data.py` |
| Models | `backend/apps/wiki/models.py` |
| API views | `backend/apps/wiki/views.py` |
| Serializers | `backend/apps/wiki/serializers.py` |
| API routes | `backend/apps/wiki/urls.py` |
| Frontend API client | `frontend/src/api/client.ts` |
| Tip detail page | `frontend/src/components/TipDetailPage.tsx` |
| Home page | `frontend/src/components/HomePage.tsx` |
| Tip images dir | `frontend/public/images/tips/` |
| Draft articles | `content/drafts/` |
| Published articles | `content/published/` |
| Django settings | `backend/config/settings.py` |

## Testing

```bash
# Backend (use venv)
cd backend && ./venv/bin/python -m pytest

# Frontend
cd frontend && npx vitest run
```

Always run tests after making changes. Do not break existing tests.
