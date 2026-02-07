# Micro-Hygiene Wiki — Implementation & Debug Plan

This document lists every bug, broken feature, and required fix found during a full code review.
Organized by severity. Each item includes the file, line number, what's wrong, and how to fix it.

---

## PHASE 1: Critical — App Won't Start

These bugs cause import errors or syntax errors. Django will refuse to start entirely.

### 1.1 Missing `include` import in `config/urls.py`

- **File:** `backend/config/urls.py:56`
- **Bug:** `path("api/", include("apps.wiki.urls"))` uses `include`, but the import on line 1 is only `from django.urls import path`. `include` is never imported.
- **Impact:** `NameError: name 'include' is not defined` — Django won't start.
- **Fix:** Change the import to `from django.urls import path, include`.

### 1.2 Invalid Python syntax in `TipListView.get_paginated_response`

- **File:** `backend/apps/wiki/views.py:33-34`
- **Bug:** The lines read:
  ```python
  'next': data.has_next() and data.next_page_number() else None,
  'previous': data.has_previous() and data.previous_page_number() else None,
  ```
  `X and Y else Z` is not valid Python. The ternary syntax is `Y if X else Z`.
- **Impact:** `SyntaxError` — the entire `views.py` module fails to import, breaking all API endpoints.
- **Fix:** Rewrite as:
  ```python
  'next': data.next_page_number() if data.has_next() else None,
  'previous': data.previous_page_number() if data.has_previous() else None,
  ```

### 1.3 `SearchView` does not exist

- **File:** `backend/apps/wiki/urls.py:26`
- **Bug:** URL references `views.SearchView.as_view()`, but the actual view is a function `search_tips` decorated with `@api_view(['GET'])` (views.py:74). There is no `SearchView` class anywhere.
- **Impact:** `AttributeError: module 'apps.wiki.views' has no attribute 'SearchView'` at startup.
- **Fix:** Change the URL to:
  ```python
  path("api/tips/search/", views.search_tips, name="tip-search"),
  ```

---

## PHASE 2: High — Crashes at Runtime / Data Integrity

These won't prevent Django from starting (after Phase 1 fixes), but will cause 500 errors or wrong data.

### 2.1 `Tip` model has no `slug` field

- **File:** `backend/apps/wiki/models.py` (Tip class, lines 33-54)
- **Bug:** `TipListSerializer` and `TipDetailSerializer` both include `"slug"` in their `fields` list, but the `Tip` model has no `slug` field or property.
- **Impact:** DRF will raise `ImproperlyConfigured` or `AttributeError` when serializing any tip.
- **Fix:** Add a `slug` field to the `Tip` model:
  ```python
  slug = models.SlugField(max_length=255, blank=True)
  ```
  Override `save()` to auto-generate slug from title using `django.utils.text.slugify()`. Then create and run a migration. Also update `seed_tips.py` to populate slugs for existing data.

### 2.2 `TipListView` pagination is completely broken

- **File:** `backend/apps/wiki/views.py:16-36`
- **Bug:** The `list` method calls `self.get_paginated_response(serializer)` passing the **serializer object**, but `get_paginated_response` treats its argument as a Django `Page` object (calling `.paginator.count`, `.number`, `.has_next()`, etc.). A serializer has none of these attributes.
- **Impact:** `AttributeError` — the tip listing endpoint returns 500.
- **Fix:** Refactor the `list` method. Either:
  - Pass the `page_obj` (from `paginate_queryset`) to `get_paginated_response`, and serialize `page_obj.object_list` separately inside `get_paginated_response`, OR
  - Use DRF's built-in `PageNumberPagination` class instead of manual Django `Paginator`, which handles this automatically. This is the cleaner approach — define a pagination class in settings or on the view.

### 2.3 `TipDetailView` uses `select_related('votes')` incorrectly

- **File:** `backend/apps/wiki/views.py:41`
- **Bug:** `votes` is a reverse ForeignKey relation (Tip has many Votes). `select_related` only works for forward FK/OneToOne fields.
- **Impact:** Django raises `FieldError` or silently fails depending on version.
- **Fix:** Change to:
  ```python
  queryset = Tip.objects.select_related('category').prefetch_related('votes')
  ```

### 2.4 `TipDetailView` lookup field mismatch

- **File:** `backend/apps/wiki/views.py:43` and `backend/apps/wiki/urls.py:11`
- **Bug:** The view sets `lookup_field = 'id'`, but the URL captures `<int:tip_id>`. DRF's `RetrieveAPIView` looks for the URL kwarg matching `lookup_field` (i.e., `id`), but the URL provides `tip_id`.
- **Impact:** 500 error or always 404.
- **Fix:** Either change the URL to `<int:id>` or set `lookup_url_kwarg = 'tip_id'` on the view.

### 2.5 `CategoryDetailView.retrieve` has broken pagination

- **File:** `backend/apps/wiki/views.py:58-71`
- **Bug:** Multiple issues:
  1. `self.paginate_queryset(tips, LimitOffsetPagination())` — `paginate_queryset` doesn't accept a pagination class as second arg.
  2. Accesses `page.object_list` but DRF's `paginate_queryset` returns a list, not a Page object.
  3. Even if it worked, the serializer result is not properly structured.
- **Impact:** 500 error on any category detail request.
- **Fix:** Remove the broken manual pagination. Simply serialize all tips for the category (they're already fetched by the query). If pagination is needed, use DRF's pagination properly:
  ```python
  def retrieve(self, request, *args, **kwargs):
      category = self.get_object()
      tips = Tip.objects.filter(category=category).select_related('category').order_by('-created_at')
      serializer = TipListSerializer(tips, many=True)
      return Response({
          'id': category.id,
          'name': category.name,
          'slug': category.slug,
          'description': category.description,
          'tips': serializer.data,
      })
  ```

### 2.6 `flag_content` view missing `tip_id` parameter

- **File:** `backend/apps/wiki/views.py:291`
- **Bug:** URL pattern is `api/tips/<int:tip_id>/flag/` (urls.py:17), passing `tip_id` as a kwarg. But the function signature is `def flag_content(request):` — it doesn't accept `tip_id`.
- **Impact:** `TypeError: flag_content() got an unexpected keyword argument 'tip_id'` — 500 error on every flag request.
- **Fix:** Either:
  - Add `tip_id` to the function signature: `def flag_content(request, tip_id):` and use it instead of reading `tip_id` from request body, OR
  - Change the URL pattern to not include `tip_id`: `path("api/tips/flag/", ...)` (keeping the current body-based approach).

### 2.7 Vote range validation inconsistency (1-5 vs 1-10)

- **File:** `backend/apps/wiki/views.py:147-154` vs `backend/apps/wiki/serializers.py:131-132`
- **Bug:** The `tip_vote` view function validates effectiveness and difficulty as 1-10, but `VoteTipSerializer` validates them as 1-5. The frontend UI shows 1-5 labels. The view doesn't use the serializer at all.
- **Impact:** Inconsistent validation. Users could submit values 6-10 via the view endpoint, breaking the 1-5 scale displayed in the UI.
- **Fix:** Decide on one range (1-5 matches the UI). Update `tip_vote` view to either:
  - Use `VoteTipSerializer` for validation, OR
  - Change the hardcoded range checks to 1-5.

### 2.8 `json` potentially undefined in `tip_vote` except block

- **File:** `backend/apps/wiki/views.py:136-142`
- **Bug:** `import json` is inside the `if not data:` branch. If `data` is truthy but `int(data.get("effectiveness"))` raises `ValueError`, the `except` block catches `json.JSONDecodeError` — but `json` was never imported.
- **Impact:** `NameError: name 'json' is not defined` instead of the intended error response.
- **Fix:** Move `import json` to the top of the file (or at least to the top of the function, outside the conditional).

### 2.9 `settings` not imported in `utils.py`

- **File:** `backend/apps/wiki/utils.py:323-328`
- **Bug:** `AIModerator.__init__` references `settings` (e.g., `getattr(settings, "HUGGINGFACE_ZERO_SHOT_MODEL", ...)`), but `from django.conf import settings` is never imported in this file.
- **Impact:** `NameError: name 'settings' is not defined` when creating an `AIModerator` instance, which happens in the `moderate_content` function used by `create_tip`.
- **Fix:** Add `from django.conf import settings` to the imports at the top of `utils.py`.

### 2.10 Duplicate unreachable code in `AIModerator.moderate_text`

- **File:** `backend/apps/wiki/utils.py:452-503`
- **Bug:** The `moderate_text` method has a complete duplicate of its logic after line 451. Lines 452-503 are unreachable dead code (the method already returns from the first block on lines 385-451).
- **Impact:** No runtime crash (dead code), but confusing and indicates copy-paste error.
- **Fix:** Delete lines 452-503 entirely.

### 2.11 Duplicate `except Exception` block in `get_classifier`

- **File:** `backend/apps/wiki/utils.py:373-383`
- **Bug:** Two identical `except Exception as e:` blocks in sequence. The second one (lines 379-383) is unreachable.
- **Impact:** Dead code, no crash.
- **Fix:** Delete the second `except Exception` block (lines 379-383).

---

## PHASE 3: Medium — Frontend Features Broken

### 3.1 `HomePage.tsx` renders duplicate navbar and footer

- **File:** `frontend/src/components/HomePage.tsx:75-161`
- **Bug:** HomePage renders its own `<nav className="navbar">` and `<footer>`. But `App.tsx` (lines 19-29, 74-76) already renders a global navbar and footer that wraps all routes.
- **Impact:** Users see two navbars and two footers on the homepage.
- **Fix:** Remove the `<nav>`, `<footer>`, and outer `<div className="app">` wrapper from `HomePage.tsx`. Keep only the `<main>` content. Also remove the duplicate `<MedicalDisclaimer />` since App.tsx already includes it.

### 3.2 Search does not work on `HomePage.tsx`

- **File:** `frontend/src/components/HomePage.tsx:35-42`
- **Bug:** `handleSearch` updates `searchQuery` state, but `fetchTips()` (called by the `useEffect`) always calls `getTips(currentPage)` — it never uses `searchQuery` or calls `searchTips()` from the API client.
- **Impact:** Typing in the search box and pressing "Search" does nothing.
- **Fix:** Two options:
  - In `fetchTips`, check if `searchQuery` is set — if so, call `searchTips(searchQuery)` from the API client instead of `getTips(currentPage)`.
  - Add `searchQuery` as a dependency of the `useEffect` so it re-fetches when query changes.

### 3.3 Vote buttons are broken on `HomePage.tsx`

- **File:** `frontend/src/components/HomePage.tsx:123-130`
- **Bug:** Two problems:
  1. Vote buttons are nested inside a `<Link>` — clicking a vote button also navigates to the tip detail page.
  2. The vote sends `tip.effectiveness_avg` and `tip.difficulty_avg` (the current averages) as the user's vote values. Users should choose their own values, not re-submit the averages.
- **Impact:** Voting from the homepage always navigates away, and the vote data is meaningless.
- **Fix:** Remove vote buttons from the homepage tip cards entirely (voting belongs on the detail page), or restructure so buttons are outside the `<Link>` and open a rating modal/dropdown.

### 3.4 `CategoryPage.tsx` fetches all tips instead of category tips

- **File:** `frontend/src/components/CategoryPage.tsx:34`
- **Bug:** After fetching category data via `getCategory(slug)` (which already returns tips for that category), the code then calls `getTips(1)` which returns ALL tips regardless of category.
- **Impact:** Category page shows all tips from every category, not just the selected one.
- **Fix:** Use the tips from the category response:
  ```typescript
  const categoryData = await getCategory(slug);
  setCategory(categoryData);
  setTips(categoryData.tips || []);
  ```
  Remove the separate `getTips(1)` call.

### 3.5 `CategoryPage.tsx` shows slug instead of description

- **File:** `frontend/src/components/CategoryPage.tsx:77`
- **Bug:** `<p className="tip-description">{tip.slug}</p>` — this displays the tip's slug (URL fragment) as if it were the description.
- **Impact:** Users see URL-formatted text like "how-to-clean-kitchen" instead of actual tip descriptions.
- **Fix:** The `TipList` type doesn't include `description`. Either:
  - Add `description` to `TipListSerializer` fields and update the `TipList` TypeScript type, then use `{tip.description}`, OR
  - Remove this line entirely (tip cards don't need full descriptions — users can click through to detail).

### 3.6 `CategoryPage.tsx` pagination doesn't trigger re-fetch

- **File:** `frontend/src/components/CategoryPage.tsx:43-45`
- **Bug:** `handlePageChange` sets `currentPage` state, but there's no `useEffect` watching `currentPage`. The data never re-fetches when page changes.
- **Impact:** Pagination buttons exist but do nothing.
- **Fix:** Since category tips come from `getCategory()` (which returns all tips for the category, not paginated), either:
  - Implement client-side pagination (slice the tips array by page), OR
  - Add a backend endpoint that returns paginated tips per category and call it in a `useEffect` watching `currentPage`.

### 3.7 `TipDetailPage.tsx` loading state never cleared on success

- **File:** `frontend/src/components/TipDetailPage.tsx:21-43`
- **Bug:** `setLoading(true)` is called on line 24. On success (line 37), `setTip(data)` is called but `setLoading(false)` is never called. The `setLoading(false)` only exists in the `catch` block (line 39).
- **Impact:** Tip detail page shows "Loading tip..." spinner forever, even after data loads successfully.
- **Fix:** Add `setLoading(false)` after `setTip(data)`:
  ```typescript
  const data = await getTip(parseInt(tipId));
  setTip(data);
  setLoading(false);
  ```
  Or use a `finally` block.

### 3.8 `TipDetailPage.tsx` voting state never resets on success

- **File:** `frontend/src/components/TipDetailPage.tsx:45-63`
- **Bug:** `setVoting({ id: tip.id })` on line 48 disables vote buttons. On success, `setTip(data)` is called (line 57) but `setVoting(null)` is never called.
- **Impact:** After voting once, all vote buttons remain permanently disabled for that tip.
- **Fix:** Add `setVoting(null)` after the successful vote refresh:
  ```typescript
  const data = await getTip(parseInt(tipId));
  setTip(data);
  setVoting(null);
  ```

### 3.9 `TipDetailPage.tsx` vote difficulty values can be out of range

- **File:** `frontend/src/components/TipDetailPage.tsx:129-157`
- **Bug:** Vote buttons hardcode difficulty as relative to current average:
  - `tip.difficulty_avg + 1` (could be > 5)
  - `tip.difficulty_avg - 1` (could be < 1)
  - `tip.difficulty_avg - 2` (could be negative)
  These can produce values outside the valid 1-5 range.
- **Impact:** Backend rejects the vote with 400 error, or (if the 1-10 range is kept) accepts nonsensical data.
- **Fix:** Let users independently rate both effectiveness AND difficulty. Use two separate rating inputs (e.g., two rows of 1-5 star buttons), not pre-computed values based on averages.

### 3.10 `SubmitForm.tsx` — Turnstile CAPTCHA never initializes

- **File:** `frontend/src/components/SubmitForm.tsx:15, 125`
- **Bug:** The Turnstile token setter is `_setTurnstileToken` (prefixed with underscore, convention for "unused"). The Cloudflare Turnstile script is never loaded, and no callback ever calls the setter. The `turnstileToken` state is always empty string.
- **Impact:** The submit button is always disabled (`disabled={isSubmitting || !turnstileToken}`). Users can never submit tips.
- **Fix:** Either:
  - **Full implementation:** Load the Turnstile script (`<script src="https://challenges.cloudflare.com/turnstile/v0/api.js">`), render the widget with `turnstile.render()`, and set the token via the callback. Consider using a React wrapper like `@marsidev/react-turnstile`.
  - **Temporary bypass for development:** Remove the `!turnstileToken` from the disabled condition and skip token validation in `DEBUG` mode (the backend already does this — line 214 of views.py).

### 3.11 `ProductsPage.tsx` uses hardcoded mock data

- **File:** `frontend/src/components/ProductsPage.tsx:39-47`
- **Bug:** The page fetches categories (line 31) but ignores the response, then uses 5 hardcoded mock products with `example.com` URLs.
- **Impact:** Products page shows fake data. No real affiliate links.
- **Fix:** Either:
  - Create a backend API endpoint (`GET /api/products/`) that returns `AffiliateProduct` model data, and fetch from it, OR
  - Remove the mock data and display real products from the affiliate fixture JSON, loaded via a new API endpoint.

### 3.12 No `/categories` listing page

- **File:** `frontend/src/App.tsx:25`
- **Bug:** The navbar has `<Link to="/categories">Categories</Link>`, but there's no route for `/categories` — only `/categories/:slug`. Clicking "Categories" in the nav goes to 404.
- **Impact:** Users cannot browse the list of all categories.
- **Fix:** Create a `CategoriesListPage` component that fetches `getCategories()` and displays all categories as clickable cards/links. Add a route: `<Route path="/categories" element={<CategoriesListPage />} />`.

---

## PHASE 4: Low — Code Quality & Cleanup

### 4.1 Duplicate imports in `views.py`

- **File:** `backend/apps/wiki/views.py:4, 91-92`
- **Bug:** `csrf_exempt` is imported twice: once via `from django.views.decorators.csrf import csrf_exempt` (line 4) and again on line 92. Also `require_http_methods` is imported on both line 3 and line 91.
- **Impact:** No runtime issue, just messy code.
- **Fix:** Remove the duplicate imports on lines 91-92. Keep only the top-level imports.

### 4.2 `import json as json` pattern

- **File:** `backend/apps/wiki/views.py:136, 198`
- **Bug:** `import json as json` inside function bodies. The `as json` alias is redundant. Also imported multiple times in different functions.
- **Impact:** No bug, just poor style.
- **Fix:** Move `import json` to the top of the file. Remove all inline imports.

### 4.3 `TipListSerializer` declares `vote_score` but doesn't include it in fields

- **File:** `backend/apps/wiki/serializers.py:49, 52-62`
- **Bug:** `vote_score = serializers.SerializerMethodField()` is declared, and `get_vote_score` is implemented, but `"vote_score"` is not in the `fields` list.
- **Impact:** The `vote_score` field is never serialized. Frontend never receives it.
- **Fix:** Add `"vote_score"` to the `fields` list in `TipListSerializer.Meta`.

### 4.4 Affiliate link `rel` attribute missing `nofollow sponsored`

- **File:** `frontend/src/components/ProductsPage.tsx:91`
- **Bug:** Product links use `rel="noopener noreferrer"` but not `rel="nofollow sponsored"` which is required for affiliate links per SEO best practices and Google guidelines.
- **Fix:** Change to `rel="noopener noreferrer nofollow sponsored"`.

### 4.5 `views.py` mixes DRF Response and Django JsonResponse

- **File:** `backend/apps/wiki/views.py`
- **Bug:** Class-based views use DRF's `Response()`, while function-based views use Django's `JsonResponse()`. This inconsistency means function-based views don't go through DRF's content negotiation or renderer pipeline.
- **Impact:** Inconsistent response format, no DRF browsable API for function views.
- **Fix:** Convert function-based views to use DRF's `Response` and `@api_view` decorator consistently (some already use `@api_view`, but then return `JsonResponse` instead of `Response`).

---

## Implementation Order

Work through these phases in order. Each phase depends on the previous one:

1. **Phase 1** first — without these fixes, the Django server won't even start.
2. **Phase 2** next — these cause 500 errors on individual endpoints.
3. **Phase 3** then — these fix frontend features that are broken or non-functional.
4. **Phase 4** last — cleanup and polish.

After each phase, run the existing test suite (`pytest` for backend, `npm run test:run` for frontend) to verify nothing regresses. Create new tests for any bugs that didn't have coverage.

---

## Files to Modify (Summary)

| File | Changes |
|------|---------|
| `backend/config/urls.py` | Add `include` import |
| `backend/apps/wiki/urls.py` | Fix SearchView reference, fix tip_id URL kwarg |
| `backend/apps/wiki/views.py` | Fix syntax error, fix pagination, fix select_related, fix flag_content signature, fix imports, fix json import, fix vote validation range |
| `backend/apps/wiki/models.py` | Add `slug` field to `Tip` model |
| `backend/apps/wiki/serializers.py` | Add `vote_score` to TipListSerializer fields |
| `backend/apps/wiki/utils.py` | Add `settings` import, remove duplicate code blocks |
| `frontend/src/components/HomePage.tsx` | Remove duplicate nav/footer, fix search, fix vote buttons |
| `frontend/src/components/TipDetailPage.tsx` | Fix loading state, fix voting state, fix vote values |
| `frontend/src/components/CategoryPage.tsx` | Use category tips, fix description display, fix pagination |
| `frontend/src/components/SubmitForm.tsx` | Implement Turnstile or add dev bypass |
| `frontend/src/components/ProductsPage.tsx` | Replace mock data with real API, fix rel attribute |
| `frontend/src/App.tsx` | Add `/categories` route |
| **New file:** `frontend/src/components/CategoriesListPage.tsx` | New page listing all categories |
| **New migration** | For Tip.slug field |

---

## PHASE 5: Marketing & Growth (AI Agent Tasks)

All tasks in this phase can be fully executed by AI agents. No human login, upload, or identity verification required.

### 5.1 SEO — Rewrite Tip Titles for Search Intent

- **What:** Rewrite all 50+ existing tip titles to match how real users search Google.
- **Input:** Current titles from `backend/apps/wiki/fixtures/tips_data.py`
- **Output:** Updated `tips_data.py` with search-optimized titles.
- **Rules:**
  - Use long-tail keyword format: "How to [action] [object] [qualifier]"
  - Example: "Kitchen Counter Cleaning" → "How to Disinfect Kitchen Counters Without Bleach"
  - Keep titles under 60 characters (Google truncates beyond this).
  - Each title must be unique and target a different search query.

### 5.2 SEO — Generate Meta Descriptions for All Tips

- **What:** Generate unique meta descriptions for every tip page.
- **Output:** Add a `meta_description` field to `Tip` model, or generate them dynamically in the serializer from the first 155 characters of description.
- **Rules:**
  - 150-155 characters max.
  - Include primary keyword naturally.
  - End with a call-to-action or value statement.
  - Example: "Learn the fastest way to disinfect kitchen counters using natural ingredients. Community-rated 4.8/5 for effectiveness."

### 5.3 Content — Bulk Generate 150+ Additional Tips

- **What:** Generate new tip content to cover more search queries and fill thin categories.
- **Output:** Extended `tips_data.py` fixture with 200+ total tips.
- **Target distribution per category:**
  - Kitchen: 25 tips
  - Bathroom: 25 tips
  - Body: 20 tips
  - Facial: 15 tips
  - Hair: 15 tips
  - Nail: 10 tips
  - Intimate: 10 tips
  - Environmental: 20 tips
  - Sleep: 15 tips
  - Food: 25 tips
  - Travel: 20 tips
- **Rules:**
  - Each tip must be factually accurate (cite common hygiene guidelines like CDC, WHO).
  - Description should be 100-300 words with actionable steps.
  - No medical claims — stick to general hygiene practices.
  - Avoid duplicating existing tip topics.

### 5.4 Content — Generate Seed Vote Data

- **What:** Generate realistic-looking vote data so the site doesn't look empty on launch.
- **Output:** A Django management command or fixture that creates vote records.
- **Rules:**
  - 5-20 votes per tip (randomized).
  - Effectiveness scores should skew positive (3-5 range, weighted toward 4).
  - Difficulty scores should vary realistically by category (Kitchen tips: easier, Intimate tips: moderate).
  - Generate unique IP hashes (random SHA256) for each vote.
  - Recalculate `effectiveness_avg`, `difficulty_avg`, and `success_rate` after seeding.

### 5.5 Marketing Copy — Reddit Post Drafts

- **What:** Write 5-10 Reddit post drafts tailored to specific subreddits.
- **Output:** Markdown file `marketing/reddit_drafts.md`
- **Target subreddits and tone:**
  - **r/CleaningTips** (1.3M members) — Write as a helpful community member sharing a useful tip. Do NOT mention the site in the post body. Only add a subtle link in comments after getting engagement.
  - **r/LifeProTips** — "LPT: [tip]" format. One specific, actionable tip per post.
  - **r/InternetIsBeautiful** — "I built a community-voted wiki for hygiene tips" launch post. Focus on the voting/community aspect.
  - **r/SideProject** — Developer-focused: tech stack, what you learned, asking for feedback.
  - **r/homemaking** — Warm, practical tone. Share 3-5 tips as a list post.
- **Rules:**
  - Each draft must follow the specific subreddit's rules (check sidebar).
  - Never sound promotional. Value-first, link-later.
  - Include a "Comment version" with the site link for each post.

### 5.6 Marketing Copy — Short-Form Video Scripts

- **What:** Write 10 short-form video scripts (TikTok/Reels/Shorts format).
- **Output:** Markdown file `marketing/shortform_scripts.md`
- **Format per script:**
  ```
  HOOK (first 2 seconds): [attention-grabbing statement]
  BODY (15-25 seconds): [tip explanation with visual cues]
  CTA (3 seconds): [call to action]
  TEXT OVERLAY: [on-screen text suggestions]
  HASHTAGS: [5-8 relevant hashtags]
  ```
- **Rules:**
  - Hook must create curiosity or shock: "You've been washing your hands wrong", "Your kitchen sponge has more bacteria than your toilet"
  - Scripts should work WITHOUT showing a face (text overlay + stock footage style).
  - Each script covers one tip from the database.
  - Include B-roll/visual direction notes.

### 5.7 Marketing Copy — Weekly Newsletter Templates

- **What:** Create 4 newsletter templates (1 month of weekly sends).
- **Output:** Markdown file `marketing/newsletter_templates.md`
- **Format:**
  - Subject line (under 50 chars, curiosity-driven)
  - Preview text (under 90 chars)
  - Body: 3 curated tips with brief descriptions
  - CTA: Link to site for full details
  - Footer: Unsubscribe link placeholder
- **Rules:**
  - Each newsletter features tips from different categories.
  - Tone: friendly, concise, no fluff.
  - Subject line examples: "Your sponge is dirtier than you think", "3 tips your dentist wishes you knew"

### 5.8 SEO — Long-Tail Keyword Research List

- **What:** Generate a list of 100 long-tail keywords the site should target.
- **Output:** CSV or markdown file `marketing/keywords.md`
- **Format per entry:**
  | Keyword | Est. Search Volume | Difficulty | Matching Category | Has Existing Tip? |
- **Rules:**
  - Focus on informational queries ("how to", "best way to", "is it safe to").
  - Prioritize low-competition keywords (3+ words).
  - Group by category.
  - Flag keywords that don't have a matching tip yet (content gap = opportunity).

### 5.9 Content — Affiliate Product Data

- **What:** Replace the mock product data with a curated list of real affiliate-worthy products.
- **Output:** Updated `backend/apps/wiki/fixtures/affiliate_products.json`
- **Rules:**
  - 20-30 products across all 11 categories.
  - Include: product name, relevant keywords, category, placeholder affiliate URL format.
  - Product types: cleaning supplies, personal hygiene tools, sanitizers, organizers.
  - Do NOT generate real affiliate URLs (those require human account signup). Use placeholder format: `https://amazon.com/dp/PLACEHOLDER_ASIN?tag=YOUR_TAG`

---

## Marketing Files Structure

After Phase 5, the following files should exist:

```
marketing/
├── reddit_drafts.md          # 5.5 — Reddit post drafts
├── shortform_scripts.md      # 5.6 — TikTok/Reels scripts
├── newsletter_templates.md   # 5.7 — 4 weekly newsletter templates
└── keywords.md               # 5.8 — 100 long-tail keywords
```
