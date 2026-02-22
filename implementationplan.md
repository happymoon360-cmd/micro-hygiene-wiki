# Antigravity Implementation Plan (Bulk Wiki Upgrade)

## Goal
Convert all generated wiki drafts into publishable image-rich articles with real image paths.

## Scope Summary
- Canonical source tips: **68**
- Draft files to process: `content/drafts/*.md` (68 files)
- Prompts per draft: **12**
- Total images to generate: **816 images**
- Output image format: PNG, 800x600
- Output image path pattern: `/images/tips/{slug}-{N}.png`

## Global Style Lock (must be identical for all images)
Use this exact style guidance across all prompt executions to keep visual consistency:

- `Style lock: unified wiki visual system v1`
- Modern flat editorial illustration
- Soft pastel blue-green palette
- Rounded geometry
- Subtle shading
- Bright high-key lighting
- Very light neutral background
- Consistent character proportions
- Clean medical-hygiene tone
- No text overlay, no logos, no watermark

## Input and Output
- Input drafts: `content/drafts/{slug}.md`
- Prompt format to parse: `![image-N](PROMPT: ... )`
- Final markdown destination: `content/published/{slug}.md`
- Generated image destination: `frontend/public/images/tips/{slug}-{N}.png`

## Reliability Scope (Secondary Verification)
- Every draft contains a `## Secondary Verification` section.
- Every draft contains 4+ references in `## References`.
- References are institutional sources (CDC, WHO, NHS, ACOG, AAD, NIH/NHLBI).
- Community-origin claims (Reddit/Quora) are treated as hypotheses and cross-checked.
- If community advice conflicts with institutional sources, institutional sources win.
- Safety wording remains conservative: use "may help" or "can reduce risk"; avoid cure claims.

## Required Workflow for Each Draft
1. Read frontmatter: `title`, `slug`, `category`.
2. Extract all `![image-N](PROMPT: ... )` lines (expected 12 lines).
3. Generate 12 images in numeric order (`1..12`).
4. Save image files using exact naming: `{slug}-{N}.png`.
5. Replace each prompt placeholder with final markdown image path:
   - Before: `![image-1](PROMPT: ...)`
   - After: `![descriptive alt text](/images/tips/{slug}-1.png)`
6. Verify style consistency: generated image matches style lock and does not include text/watermarks.
7. Move completed draft to `content/published/{slug}.md`.
8. Update fixture entry in `backend/apps/wiki/fixtures/tips_data.py`:
   - Match by slug
   - Replace `description` with final markdown body (no frontmatter)
9. Run seed sync script to update DB entries.
10. Run reliability spot-check:
   - Confirm `## Secondary Verification` remains in published markdown
   - Confirm `## References` links are preserved and readable

## Batch Strategy
- Recommended batch size: **4 drafts per batch** (48 images per batch)
- Total batches: **17 batches**
- After each batch:
  - Verify all 48 files exist
  - Verify no missing sequence numbers
  - Verify all placeholders replaced

## Slug List (68)
1. `how-to-wash-hands-properly-for-20-seconds`
2. `how-to-use-hand-sanitizer-when-unavailable`
3. `how-to-wash-hands-before-eating-properly`
4. `how-to-clean-under-fingernails-effectively`
5. `how-to-dry-hands-completely-after-washing`
6. `how-to-wash-hands-after-touching-surfaces`
7. `how-to-brush-teeth-twice-daily-correctly`
8. `how-to-floss-between-teeth-daily`
9. `how-to-replace-toothbrush-every-3-4-months`
10. `how-to-clean-tongue-scraper-properly`
11. `how-to-use-mouthwash-for-bacteria`
12. `how-to-visit-dentist-every-6-months`
13. `how-to-limit-sugary-foods-for-teeth`
14. `how-to-shower-daily-or-every-other-day`
15. `how-to-use-lukewarm-water-for-showers`
16. `how-to-use-mild-fragrance-free-soap`
17. `how-to-wash-feet-between-toes-properly`
18. `how-to-moisturize-skin-after-showering`
19. `how-to-exfoliate-1-2-times-per-week`
20. `how-to-wear-clean-underwear-daily`
21. `how-to-change-socks-daily-properly`
22. `how-to-wash-face-morning-and-night`
23. `how-to-avoid-over-washing-your-face`
24. `how-to-use-sunscreen-daily-correctly`
25. `how-to-remove-makeup-before-bed`
26. `how-to-avoid-touching-your-face`
27. `how-to-stop-popping-pimples-safely`
28. `how-to-change-pillowcase-weekly`
29. `how-to-wash-hair-2-3-times-weekly`
30. `how-to-apply-conditioner-on-ends`
31. `how-to-wash-hair-without-hot-water`
32. `how-to-wash-hairbrush-regularly`
33. `how-to-avoid-sharing-hair-tools`
34. `how-to-air-dry-hair-properly`
35. `how-to-keep-nails-short-and-clean`
36. `how-to-stop-biting-your-nails`
37. `how-to-push-back-cuticles-gently`
38. `how-to-clean-nail-tools-properly`
39. `how-to-avoid-sharing-nail-tools`
40. `how-to-wash-genital-area-properly`
41. `how-to-wipe-front-to-back-properly`
42. `how-to-change-menstrual-products-regularly`
43. `how-to-wear-breathable-underwear-properly`
44. `how-to-avoid-douching-properly`
45. `how-to-practice-safe-sex-hygiene`
46. `how-to-clean-phone-screen-properly`
47. `how-to-wash-bed-sheets-weekly`
48. `how-to-disinfect-high-touch-surfaces-daily`
49. `how-to-ventilate-your-home-daily`
50. `how-to-clean-toilet-bowl-regularly`
51. `how-to-wash-towels-after-3-4-uses`
52. `how-to-maintain-consistent-sleep-schedule`
53. `how-to-create-dark-bedroom-for-sleep`
54. `how-to-avoid-screens-before-bed`
55. `how-to-limit-caffeine-after-2-pm`
56. `how-to-establish-bedtime-routine`
57. `how-to-replace-pillows-every-1-2-years`
58. `how-to-wash-hands-before-food-prep`
59. `how-to-separate-raw-and-cooked-foods`
60. `how-to-cook-meat-to-safe-temperatures`
61. `how-to-refrigerate-perishable-food-promptly`
62. `how-to-wash-produce-before-eating`
63. `how-to-clean-kitchen-surfaces-daily`
64. `how-to-use-bottled-water-traveling`
65. `how-to-clean-airplane-tray-tables`
66. `how-to-pack-travel-sized-hygiene-kit`
67. `how-to-wear-flip-flops-in-shared-showers`
68. `how-to-sanitize-hotel-room-at-check-in`

## Completion Criteria
- All 68 drafts processed.
- 816 images generated and stored with exact naming.
- No remaining `PROMPT:` placeholders in published markdown.
- Secondary verification and references preserved in all 68 published articles.
- All 68 fixture descriptions updated by slug.
- DB synced with updated descriptions and slugs.
