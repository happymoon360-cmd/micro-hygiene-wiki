# Micro-Hygiene Wiki MVP

## TL;DR

> **Quick Summary**: Build an anonymous, crowdsourced wiki for embarrassing hygiene issues (tonsil stones, body odor, etc.) with practical home-based solutions, Reddit-style voting, and affiliate marketing revenue via Django + React.
>
> **Deliverables**:
> - Django REST API backend with PostgreSQL on Supabase
> - React frontend deployed on Vercel
> - Anonymous contribution system with IP-based rate limiting
> - Crowdsourced validation (voting for effectiveness/difficulty)
> - Long-tail SEO optimization with Schema.org markup
> - Affiliate link integration (Amazon + iHerb)
> - Content seeding: 50+ tips from Reddit
> - Safety guardrails: keyword blacklist, AI moderation, disclaimers
>
> **Estimated Effort**: Large (8-12 weeks)
> **Parallel Execution**: YES - 3 waves
> **Critical Path**: Backend API → Frontend integration → SEO optimization → Deployment

---

## Context

### Original Request
Develop an MVP for an anonymous, crowdsourced wiki dedicated to "Embarrassing Micro-Hygiene" issues (e.g., tonsil stones, chronic body odor, bad breath). The platform focuses on practical, home-based solutions and personal experiences rather than clinical medical definitions, targeting the $13.6B hygiene market through Long-tail SEO and affiliate marketing.

### Interview Summary
**Key Discussions**:
- **Tech Stack**: Django + React (custom build for full control over voting, success rates, affiliate auto-linking) - Chosen over MediaWiki for UI/UX customization
- **Timeline**: 8-12+ weeks for robust MVP - Full-featured platform with polish
- **Hosting**: Vercel + Supabase (modern, pay-as-you-go) - Django hosted on Railway/Render, React on Vercel
- **Budget**: <$50/month infrastructure cost
- **Content Seeding**: Auto-scrape 50+ tips from Reddit (all 4 categories)
- **Affiliate Platforms**: Amazon + iHerb (dual platform integration)
- **Categories**: All 4 launching initially (Oral Hygiene, Body Odor, Skin, Genital)
- **Testing**: TDD (Test-Driven Development) - RED-GREEN-REFACTOR workflow

### Metis Review
**Critical Gaps Addressed**:
- **Elasticsearch simplification**: Using PostgreSQL full-text search (pg_search) for MVP - Elasticsearch adds unnecessary complexity for 50-100 tips
- **Django hosting clarification**: Django deploys to Railway/Render, not Vercel (Vercel is React only)
- **MVP scope boundaries**: Locked down to core features - no advanced moderation queue, no analytics dashboard, no real-time features
- **GDPR compliance**: IP addresses hashed and expired after 7 days
- **Moderation workflow**: AI flagging + keyword blacklist - no human review queue for MVP (escalation via email)
- **Affiliate strategy**: Static link mapping (no real-time API integration) - defers to post-MVP for cost/time savings
- **SEO priority**: Basic Schema.org Article markup + clean URLs - no advanced SEO tools

**Identified Gaps (Auto-Resolved)**:
- **Zero votes handling**: Display "No votes yet" instead of defaulting to 50%
- **Contradictory tips**: Display chronologically, let users vote to surface best
- **Missing affiliate products**: Display "Affiliate link not available" message
- **Vote deduplication**: Allow one vote per IP per tip (session-based)
- **Empty/spam submissions**: Minimum character count + keyword blacklist
- **Search fallback**: PostgreSQL full-text search (no Elasticsearch for MVP)

---

## Work Objectives

### Core Objective
Build a functional, SEO-optimized wiki platform for embarrassing hygiene solutions with anonymous crowdsourced content, Reddit-style voting, and affiliate revenue generation.

### Concrete Deliverables
- Django REST API with 5 core endpoints (tips list, detail, create, vote, search)
- React frontend with 4 pages (Home, Category, Tip Detail, Submit Form)
- PostgreSQL database with 4 core tables (categories, tips, votes, affiliate_products)
- 50+ seeded tips from Reddit (manual curation of scraped content)
- Python keyword filtering script for content moderation
- 50 long-tail SEO phrases documented
- Static affiliate link mapping system (Amazon + iHerb)
- IP-based rate limiting (5 posts/hour, 20 flags/day)
- Cloudflare Turnstile CAPTCHA integration
- Schema.org Article markup on all tip pages
- Medical disclaimer on all pages
- GDPR-compliant IP handling (hash + 7-day retention)

### Definition of Done
- [ ] All 50+ tips seeded and accessible via API
- [ ] Voting system functional (effectiveness 1-5, difficulty 1-5)
- [ ] Success rate calculated and displayed on tip pages
- [ ] Affiliate links present for mapped products
- [ ] Medical disclaimer visible on all pages
- [ ] Cloudflare Turnstile functional on submission form
- [ ] IP-based rate limiting enforced
- [ ] Keyword blacklist blocks prohibited terms
- [ ] Schema.org markup present on tip detail pages
- [ ] SEO-optimized URLs (lowercase, hyphen-separated)
- [ ] All tests passing (>80% coverage)
- [ ] Frontend deployed to Vercel (https://microhygiene-wiki.vercel.app)
- [ ] Backend deployed to Railway/Render (https://api.microhygiene-wiki.com)

### Must Have
- Anonymous contribution (no accounts required)
- Reddit-style voting (upvotes/downvotes for effectiveness/difficulty)
- Success rate calculation (aggregated from votes)
- 4 content categories (Oral Hygiene, Body Odor, Skin, Genital)
- Keyword blacklist for dangerous content
- Medical disclaimer on all pages
- IP-based rate limiting
- Affiliate link generation for mapped products
- Basic search functionality
- Schema.org Article markup
- SEO-optimized URLs and meta tags
- 50+ seeded tips from Reddit

### Must NOT Have (Guardrails)
- User accounts or authentication system
- Email notifications
- Real-time features (WebSockets, live updates)
- Human moderation queue (AI flagging only)
- Advanced search (autocomplete, filters, fuzzy search)
- Real-time Amazon/iHerb API integration
- Analytics dashboard
- Multi-language support
- Social sharing beyond basic link copy
- Custom component library (use shadcn/ui or Material UI)
- CDN integration beyond Vercel's built-in
- A/B testing framework
- Content versioning/edit history
- Comment system on tips
- Performance/load testing
- Staging environment (production deploy only)

---

## Verification Strategy (MANDATORY)

### Test Decision
- **Infrastructure exists**: NO
- **User wants tests**: TDD (Test-Driven Development)
- **Framework**: pytest (Python), jest/vitest (React)

### TDD Enabled

Each TODO follows RED-GREEN-REFACTOR:

**Task Structure**:
1. **RED**: Write failing test first
   - Test file: `backend/tests/test_module.py`
   - Test command: `pytest backend/tests/test_module.py -v`
   - Expected: FAIL (test exists, implementation doesn't)
2. **GREEN**: Implement minimum code to pass
   - Command: `pytest backend/tests/test_module.py`
   - Expected: PASS
3. **REFACTOR**: Clean up while keeping green
   - Command: `pytest backend/tests/test_module.py`
   - Expected: PASS (still)

**Test Setup Tasks**:
- [ ] 0.1. Setup Python test infrastructure
  - Install: `pip install pytest pytest-cov pytest-django django-test-plus`
  - Config: Create `pytest.ini` with Django settings
  - Verify: `pytest --help` → shows help
  - Example: Create `backend/tests/example_test.py`
  - Verify: `pytest backend/tests/example_test.py` → 1 test passes

- [ ] 0.2. Setup React test infrastructure
  - Install: `npm install --save-dev vitest @testing-library/react @testing-library/jest-dom`
  - Config: Create `vitest.config.ts`
  - Verify: `npm run test --help` → shows help
  - Example: Create `frontend/src/__tests__/example.test.tsx`
  - Verify: `npm run test` → 1 test passes

### Automated Verification (NO User Intervention)

> **CRITICAL PRINCIPLE: ZERO USER INTERVENTION**
>
> **NEVER** create acceptance criteria that require:
> - "User manually tests..." / "사용자가 직접 테스트..."
> - "User visually confirms..." / "사용자가 눈으로 확인..."
> - "User interacts with..." / "사용자가 직접 조작..."
> - "Ask user to verify..." / "사용자에게 확인 요청..."
> - ANY step that requires a human to perform an action
>
> **ALL verification MUST be automated and executable by the agent.**

**By Deliverable Type:**

| Type | Verification Tool | Automated Procedure |
|------|------------------|---------------------|
| **Django API** | Bash (curl/pytest) | Run pytest, curl endpoints, validate JSON responses |
| **React Frontend** | Bash (curl/grep) | Check HTML markup, verify scripts, validate content |
| **Database** | Bash (psql) | Query database, validate row counts, check data integrity |
| **Affiliate Links** | Bash (curl/grep) | Scrape pages, verify affiliate links present |
| **SEO/Schema** | Bash (curl/grep) | Check Schema.org markup, verify meta tags |
| **Rate Limiting** | Bash (curl/pytest) | Attempt multiple submissions, verify 429 response |

**Evidence Requirements (Agent-Executable):**
- Command output captured and compared against expected patterns
- Test results showing pass/fail status
- JSON response fields validated with specific assertions
- Exit codes checked (0 = success)

---

## Execution Strategy

### Parallel Execution Waves

> Maximize throughput by grouping independent tasks into parallel waves.
> Each wave completes before the next begins.

```
Wave 1 (Start Immediately):
├── Task 1: Setup project structure (backend + frontend)
├── Task 2: Configure PostgreSQL on Supabase
└── Task 3: Create Django models (tests first)

Wave 2 (After Wave 1):
├── Task 4: Implement Django API endpoints (tests first)
├── Task 5: Build React frontend components (tests first)
└── Task 6: Setup Cloudflare Turnstile

Wave 3 (After Wave 2):
├── Task 7: Integrate affiliate link generation
├── Task 8: Implement voting system
└── Task 9: Seed Reddit tips

Wave 4 (After Wave 3):
├── Task 10: SEO optimization (Schema.org, meta tags)
├── Task 11: Content moderation (keyword blacklist, AI)
└── Task 12: Deploy to production

Critical Path: Task 1 → Task 3 → Task 4 → Task 8 → Task 10 → Task 12
Parallel Speedup: ~60% faster than sequential
```

### Dependency Matrix

| Task | Depends On | Blocks | Can Parallelize With |
|------|------------|--------|---------------------|
| 1 | None | 2, 3 | None |
| 2 | 1 | 3 | None |
| 3 | 2 | 4, 5 | 5, 6 |
| 4 | 3 | 8 | 5, 6 |
| 5 | 2 | 7 | 3, 4 |
| 6 | 2 | 9 | 3, 4 |
| 7 | 5 | 11 | 8, 9 |
| 8 | 4 | 10 | 7, 9 |
| 9 | 6 | 11 | 7, 8 |
| 10 | 8 | 12 | 11 |
| 11 | 7, 9 | 12 | 10 |
| 12 | 10, 11 | None | None (final) |

### Agent Dispatch Summary

| Wave | Tasks | Recommended Agents |
|------|-------|-------------------|
| 1 | 1, 2, 3 | executor-low (setup tasks) |
| 2 | 4, 5, 6 | executor (API + frontend) parallel with executor-low (CAPTCHA) |
| 3 | 7, 8, 9 | executor (voting + affiliate + content) parallel |
| 4 | 10, 11, 12 | executor (SEO + moderation) parallel with executor-high (deployment) |

---

## TODOs

> Implementation + Test = ONE Task. Never separate.
> EVERY task MUST have: Recommended Agent Profile + Parallelization info.

### Wave 1: Foundation (Weeks 1-2)

- [ ] 1. Setup Project Structure

  **What to do**:
  - Create Django project: `django-admin startproject backend`
  - Create React app: `npm create vite-app@latest frontend`
  - Configure Git repository with backend/frontend folders
  - Create `.gitignore` for Python/Node artifacts

  **Must NOT do**:
  - Set up CI/CD pipelines (out of scope)
  - Create staging environment (production only)

  **Recommended Agent Profile**:
  > - **Category**: `quick`
    - Reason: Simple scaffolding task, straightforward commands
  - **Skills**: `[git-master]`
    - `git-master`: Initialize Git repository with proper .gitignore

  **Parallelization**:
  - **Can Run In Parallel**: NO (blocking)
  - **Parallel Group**: Wave 1 (with Tasks 2, 3)
  - **Blocks**: Tasks 4, 5, 6 (all depend on project structure)
  - **Blocked By**: None (can start immediately)

  **References**:

  **Django Project Setup**:
  - Official docs: https://docs.djangoproject.com/en/stable/intro/tutorial01/#creating-a-project
  - Create project with `django-admin startproject config .` (in current directory)

  **React Project Setup**:
  - Vite docs: https://vitejs.dev/guide/
  - Create app with `npm create vite@latest frontend -- --template react-ts`

  **Git Configuration**:
  - GitHub .gitignore for Python: https://github.com/github/gitignore/blob/main/Python.gitignore
  - GitHub .gitignore for Node: https://github.com/github/gitignore/blob/main/Node.gitignore

  **WHY Each Reference Matters**:
  - Django docs: Official project structure conventions
  - Vite docs: Modern React build tool setup
  - Git ignores: Prevents committing virtualenvs, node_modules, .pyc files

  **Acceptance Criteria**:

  **TDD (tests enabled)**:
  - [ ] Test: `test_project_structure.py` exists
  - [ ] Test: Asserts `backend/manage.py` exists
  - [ ] Test: Asserts `frontend/package.json` exists
  - [ ] Test: Asserts `.gitignore` exists and contains `__pycache__`, `node_modules`
  - [ ] pytest backend/tests/test_project_structure.py → PASS (4 tests)

  **Automated Verification**:
  ```bash
  # Agent runs:
  ls -la backend/manage.py
  # Assert: File exists

  ls -la frontend/package.json
  # Assert: File exists

  cat .gitignore
  # Assert: Contains __pycache__, node_modules, .env
  ```

  **Evidence to Capture**:
  - [ ] Directory structure output
  - [ ] Test results showing all 4 tests passing

  **Commit**: YES
  - Message: `chore: setup project structure (django + react)`
  - Files: `backend/manage.py`, `frontend/package.json`, `.gitignore`

- [ ] 2. Configure PostgreSQL on Supabase

  **What to do**:
  - Create Supabase project
  - Create database: `micro_hygiene_wiki`
  - Generate connection string with connection pooling
  - Store in environment variables (.env)
  - Test database connection

  **Must NOT do**:
  - Configure read replicas (not needed for MVP)
  - Set up foreign data wrappers

  **Recommended Agent Profile**:
  > - **Category**: `quick`
    - Reason: Configuration task, documented steps
  - **Skills**: `[]`
    - No specific skills needed, standard tools sufficient

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 3)
  - **Blocks**: Tasks 3, 4 (database needed for models/API)
  - **Blocked By**: Task 1 (project structure needed first)

  **References**:

  **Supabase Setup**:
  - Quickstart: https://supabase.com/docs/guides/getting-started/quickstart
  - Connection string format: `postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:5432/postgres`

  **Django Database Config**:
  - Settings docs: https://docs.djangoproject.com/en/stable/ref/settings/#databases
  - Use `psycopg2-binary` adapter

  **WHY Each Reference Matters**:
  - Supabase docs: Accurate connection string format with connection pooling
  - Django settings: Database configuration for production

  **Acceptance Criteria**:

  **TDD (tests enabled)**:
  - [ ] Test: `test_database_connection.py` tests connection to Supabase
  - [ ] Test: Asserts connection successful
  - [ ] Test: Asserts environment variables loaded correctly
  - [ ] pytest backend/tests/test_database_connection.py → PASS (2 tests)

  **Automated Verification**:
  ```bash
  # Agent runs:
  export $(cat .env | xargs)
  python backend/manage.py shell -c "from django.db import connection; connection.cursor(); print('OK')"
  # Assert: Output is "OK"
  ```

  **Evidence to Capture**:
  - [ ] Connection test output
  - [ ] Test results showing database connectivity

  **Commit**: YES
  - Message: `feat: configure supabase postgresql database`
  - Files: `backend/.env`, `backend/config/settings.py` (database config)

- [ ] 3. Create Django Models

  **What to do**:
  - Create models: Category, Tip, Vote, AffiliateProduct
  - Define relationships (Tip → Category, Tip → Votes)
  - Add indexes for performance
  - Run migrations

  **Must NOT do**:
  - Add versioning/edit history (out of scope)
  - Create user account models (anonymous only)

  **Recommended Agent Profile**:
  > - **Category**: `quick`
    - Reason: Data modeling, straightforward Django task
  - **Skills**: `[]`
    - Django ORM patterns well-documented

  **Parallelization**:
  - **Can Run In Parallel**: YES (after Task 2)
  - **Parallel Group**: Wave 1 (with Tasks 1, 2)
  - **Blocks**: Tasks 4, 5 (API/frontend need models)
  - **Blocked By**: Task 2 (database connection required)

  **References**:

  **Django Models Documentation**:
  - Model fields: https://docs.djangoproject.com/en/stable/ref/models/fields/
  - Relationships: https://docs.djangoproject.com/en/stable/ref/models/relationships/
  - Indexes: https://docs.djangoproject.com/en/stable/ref/models/indexes/

  **WHY Each Reference Matters**:
  - Django docs: Accurate field types and relationship definitions
  - Indexes: Performance optimization for queries

  **Acceptance Criteria**:

  **TDD (tests enabled)**:
  - [ ] Test: `test_models.py` tests all 4 models
  - [ ] Test: Asserts Category has correct fields (name, slug, description)
  - [ ] Test: Asserts Tip has correct fields (title, description, category, effectiveness_avg, difficulty_avg, success_rate)
  - [ ] Test: Asserts Vote has correct fields (tip, effectiveness, difficulty, ip_hash)
  - [ ] Test: Asserts AffiliateProduct has correct fields (name, affiliate_url, network, keywords)
  - [ ] pytest backend/tests/test_models.py → PASS (15+ tests)

  **Automated Verification**:
  ```bash
  # Agent runs:
  python backend/manage.py makemigrations
  # Assert: Exit code 0, migrations created

  python backend/manage.py migrate
  # Assert: Exit code 0, tables created

  python backend/manage.py shell -c "from backend.models import Category, Tip, Vote, AffiliateProduct; print(Category._meta.get_fields())"
  # Assert: Returns list of field objects
  ```

  **Evidence to Capture**:
  - [ ] Migration output showing tables created
  - [ ] Test results showing all model tests passing

  **Commit**: YES (group with Task 4)
  - Message: `feat: create django models (category, tip, vote, affiliateproduct)`
  - Files: `backend/apps/wiki/models.py`, `backend/apps/wiki/migrations/`

### Wave 2: Core Features (Weeks 3-6)

- [ ] 4. Implement Django REST API Endpoints

  **What to do**:
  - Create API views: tip_list, tip_detail, tip_create, tip_vote, search_tips
  - Implement serializers for all models
  - Add IP-based rate limiting decorators
  - Implement success rate calculation

  **Must NOT do**:
  - Add authentication system (anonymous only)
  - Create admin interface (use Django admin)

  **Recommended Agent Profile**:
  > - **Category**: `quick`
    - Reason: REST API implementation, Django REST Framework
  - **Skills**: `[]`
    - Django REST Framework well-documented

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 2 (with Tasks 5, 6)
  - **Blocks**: Task 8 (voting uses API)
  - **Blocked By**: Task 3 (models needed)

  **References**:

  **Django REST Framework**:
  - Serializers: https://www.django-rest-framework.org/api-guide/serializers/
  - ViewSets: https://www.django-rest-framework.org/api-guide/viewsets/
  - Pagination: https://www.django-rest-framework.org/api-guide/pagination/

  **django-ratelimit Documentation**:
  - https://django-ratelimit.readthedocs.io/en/latest/ratelimit.html

  **WHY Each Reference Matters**:
  - DRF docs: Standard API patterns for Django
  - django-ratelimit: IP-based rate limiting implementation

  **Acceptance Criteria**:

  **TDD (tests enabled)**:
  - [ ] Test: `test_api_endpoints.py` tests all 5 endpoints
  - [ ] Test: Asserts GET /api/tips/ returns paginated list
  - [ ] Test: Asserts POST /api/tips/ creates tip (rate limited to 5/hour)
  - [ ] Test: Asserts POST /api/tips/{id}/vote/ updates scores
  - [ ] Test: Asserts GET /api/tips/search/ returns results
  - [ ] pytest backend/tests/test_api_endpoints.py → PASS (25+ tests)

  **Automated Verification**:
  ```bash
  # Agent runs:
  curl -s http://localhost:8000/api/tips/ | jq '.results | length'
  # Assert: Returns 20 or fewer (paginated)

  curl -X POST http://localhost:8000/api/tips/ \
    -H "Content-Type: application/json" \
    -d '{"title":"Test","description":"Test","category":"oral-hygiene","products":[]}'
  # Assert: 201 Created

  curl -s http://localhost:8000/api/tips/search?q=tonsil | jq '.results | length'
  # Assert: Returns relevant results
  ```

  **Evidence to Capture**:
  - [ ] API test output showing all endpoints functional
  - [ ] Rate limiting test showing 429 response after 5 requests

  **Commit**: YES
  - Message: `feat: implement django rest api endpoints (tips, votes, search)`
  - Files: `backend/apps/wiki/views.py`, `backend/apps/wiki/urls.py`, `backend/apps/wiki/serializers.py`

- [ ] 5. Build React Frontend Components

  **What to do**:
  - Create components: HomePage, CategoryPage, TipDetailPage, SubmitForm
  - Integrate with Django REST API
  - Implement routing (React Router)
  - Add medical disclaimer component

  **Must NOT do**:
  - Implement user authentication (anonymous only)
  - Add social sharing features

  **Recommended Agent Profile**:
  > - **Category**: `visual-engineering`
    - Reason: Frontend UI development, styling, components
  - **Skills**: `[]`
    - React patterns well-documented

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 4, 6)
  - **Blocks**: Task 7 (affiliate links integrate in frontend)
  - **Blocked By**: Task 1 (React project needed)

  **References**:

  **React Documentation**:
  - Components: https://react.dev/learn/thinking-in-react
  - Hooks: https://react.dev/reference/react
  - React Router: https://reactrouter.com/en/main

  **Fetch API**:
  - MDN: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch

  **WHY Each Reference Matters**:
  - React docs: Component patterns and hooks usage
  - React Router: Client-side routing implementation
  - Fetch API: Standard browser API for Django API calls

  **Acceptance Criteria**:

  **TDD (tests enabled)**:
  - [ ] Test: `HomePage.test.tsx` renders correctly
  - [ ] Test: `TipDetailPage.test.tsx` displays tip data
  - [ ] Test: `SubmitForm.test.tsx` validates form fields
  - [ ] Test: `MedicalDisclaimer.test.tsx` displays disclaimer text
  - [ ] npm run test → PASS (10+ tests)

  **Automated Verification**:
  ```bash
  # Agent runs:
  cd frontend && npm run build
  # Assert: Exit code 0, build/ directory created

  curl -s http://localhost:3000/ | grep -o 'Micro-Hygiene Wiki'
  # Assert: Title visible on homepage
  ```

  **Evidence to Capture**:
  - [ ] Build output showing successful compilation
  - [ ] Screenshot of homepage rendering

  **Commit**: YES
  - Message: `feat: build react frontend components (home, category, tip, submit)`
  - Files: `frontend/src/components/`, `frontend/src/App.tsx`

- [ ] 6. Setup Cloudflare Turnstile CAPTCHA

  **What to do**:
  - Register Cloudflare account
  - Create Turnstile site key and secret key
  - Install `cloudflareturnstile` Python package
  - Integrate Turnstile widget in React SubmitForm
  - Add server-side verification in Django view

  **Must NOT do**:
  - Configure hCaptcha or reCAPTCHA (use Turnstile only)

  **Recommended Agent Profile**:
  > - **Category**: `quick`
    - Reason: CAPTCHA integration, documented steps
  - **Skills**: `[]`
    - Cloudflare Turnstile docs available

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 4, 5)
  - **Blocks**: Task 9 (CAPTCHA needed for form submission)
  - **Blocked By**: Task 1 (project structure needed)

  **References**:

  **Cloudflare Turnstile Documentation**:
  - Getting started: https://developers.cloudflare.com/turnstile/get-started/
  - Server validation: https://developers.cloudflare.com/turnstile/get-started/server-side-validation/
  - Widget documentation: https://developers.cloudflare.com/turnstile/widgets/

  **Python Package**:
  - cloudflareturnstile: https://pypi.org/project/cloudflareturnstile/

  **WHY Each Reference Matters**:
  - Turnstile docs: Widget integration and server-side validation
  - Python package: Server-side token verification

  **Acceptance Criteria**:

  **TDD (tests enabled)**:
  - [ ] Test: `test_turnstile_verification.py` verifies token
  - [ ] Test: Asserts valid token returns True
  - [ ] Test: Asserts invalid token returns False
  - [ ] pytest backend/tests/test_turnstile_verification.py → PASS (3 tests)

  **Automated Verification**:
  ```bash
  # Agent runs:
  curl -s http://localhost:3000/submit | grep -o 'cf-turnstile'
  # Assert: Turnstile element present in page

  curl -X POST http://localhost:8000/api/tips/ \
    -H "Content-Type: application/json" \
    -d '{"turnstile_token":"invalid","title":"Test","description":"Test","category":"oral-hygiene","products":[]}'
  # Assert: 400 Bad Request, error mentions invalid CAPTCHA
  ```

  **Evidence to Capture**:
  - [ ] Turnstile widget screenshot
  - [ ] Test output showing token verification

  **Commit**: YES
  - Message: `feat: integrate cloudflare turnstile captcha`
  - Files: `frontend/src/components/SubmitForm.tsx`, `backend/apps/wiki/views.py` (validation)

### Wave 3: Advanced Features (Weeks 7-9)

- [ ] 7. Integrate Affiliate Link Generation

  **What to do**:
  - Create keyword-to-affiliate-link mapping system
  - Implement autolinker for tip descriptions
  - Add rel="nofollow sponsored" to affiliate links
  - Create static mapping for Amazon + iHerb products

  **Must NOT do**:
  - Implement real-time Amazon/iHerb API calls (use static mapping)

  **Recommended Agent Profile**:
  > - **Category**: `quick`
    - Reason: Text processing and URL generation
  - **Skills**: `[]`
    - String manipulation and regex well-documented

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3 (with Tasks 8, 9)
  - **Blocks**: Task 11 (SEO needs affiliate links)
  - **Blocked By**: Task 5 (frontend components needed)

  **References**:

  **Keyword Autolinking Pattern**:
  - Django string processing: https://docs.djangoproject.com/en/stable/ref/templates/builtins/#defaultfilters
  - Regex for keyword matching: Python `re` module docs

  **FTC Compliance**:
  - Affiliate disclosure requirements: https://www.ftc.gov/business-guidance/advertise-and-promote-your-products-and-services-legal-guidance
  - Nofollow sponsored: https://developers.google.com/search/docs/crawling-indexing/nofollow

  **WHY Each Reference Matters**:
  - Django filters: Efficient string replacement in templates
  - FTC docs: Legal compliance for affiliate links
  - Google docs: Correct rel attribute for affiliate links

  **Acceptance Criteria**:

  **TDD (tests enabled)**:
  - [ ] Test: `test_affiliate_links.py` tests keyword replacement
  - [ ] Test: Asserts "waterpik" replaced with affiliate URL
  - [ ] Test: Asserts rel="nofollow sponsored" present
  - [ ] pytest backend/tests/test_affiliate_links.py → PASS (8+ tests)

  **Automated Verification**:
  ```bash
  # Agent runs:
  curl -s http://localhost:3000/tip/1 | grep -o 'rel="nofollow sponsored"'
  # Assert: Attribute present on affiliate links

  curl -s http://localhost:3000/tip/1 | grep -o 'amazon.com'
  # Assert: Affiliate links present for mapped products
  ```

  **Evidence to Capture**:
  - [ ] HTML output showing affiliate links with correct attributes
  - [ ] Test results showing keyword replacement working

  **Commit**: YES
  - Message: `feat: implement affiliate link generation (keyword mapping, ftc compliance)`
  - Files: `backend/apps/wiki/utils.py` (affiliate linker), `frontend/src/components/TipContent.tsx`

- [ ] 8. Implement Voting System

  **What to do**:
  - Create vote endpoint (effectiveness 1-5, difficulty 1-5)
  - Implement IP-based vote deduplication
  - Calculate success rate formula: `avg_effectiveness / (avg_difficulty + 1) * 100`
  - Display "No votes yet" for zero votes
  - Update tip aggregates on each vote

  **Must NOT do**:
  - Implement reputation system (simple voting only)
  - Add multi-dimensional ratings beyond effectiveness/difficulty

  **Recommended Agent Profile**:
  > - **Category**: `quick`
    - Reason: Data aggregation and calculation
  - **Skills**: `[]`
    - Django ORM aggregation well-documented

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3 (with Tasks 7, 9)
  - **Blocks**: Task 10 (SEO needs vote data)
  - **Blocked By**: Task 4 (API endpoint needed)

  **References**:

  **Django ORM Aggregation**:
  - Avg: https://docs.djangoproject.com/en/stable/ref/models/querysets/#avg
  - Count: https://docs.djangoproject.com/en/stable/ref/models/querysets/#count
  - F expressions: https://docs.djangoproject.com/en/stable/ref/models/expressions/

  **WHY Each Reference Matters**:
  - Django docs: Efficient aggregation for vote calculations

  **Acceptance Criteria**:

  **TDD (tests enabled)**:
  - [ ] Test: `test_voting.py` tests vote creation
  - [ ] Test: Asserts IP-based deduplication works
  - [ ] Test: Asserts success rate calculation correct
  - [ ] Test: Asserts zero votes displays "No votes yet"
  - [ ] pytest backend/tests/test_voting.py → PASS (12+ tests)

  **Automated Verification**:
  ```bash
  # Agent runs:
  curl -X POST http://localhost:8000/api/tips/1/vote/ \
    -H "Content-Type: application/json" \
    -d '{"effectiveness":5,"difficulty":2}'
  # Assert: 200 OK

  curl -s http://localhost:8000/api/tips/1/ | jq '.success_rate, .vote_count'
  # Assert: success_rate calculated correctly
  ```

  **Evidence to Capture**:
  - [ ] Vote test output showing aggregation
  - [ ] API response showing updated success rate

  **Commit**: YES
  - Message: `feat: implement voting system (effectiveness, difficulty, success rate)`
  - Files: `backend/apps/wiki/models.py` (Vote model), `backend/apps/wiki/views.py` (vote endpoint)

- [ ] 9. Seed Reddit Tips

  **What to do**:
  - Scrape top 50+ tips from r/AskDocs, r/Hygiene subreddits
  - Manually curate content for quality
  - Import into database via Django management command
  - Assign categories (Oral Hygiene, Body Odor, Skin, Genital)

  **Must NOT do**:
  - Auto-continuous scraping (one-time seed only)

  **Recommended Agent Profile**:
  > - **Category**: `quick`
    - Reason: Content scraping and database import
  - **Skills**: `[]`
    - Django management commands well-documented

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3 (with Tasks 7, 8)
  - **Blocks**: Task 12 (deployment needs content)
  - **Blocked By**: Task 3 (models needed)

  **References**:

  **Django Management Commands**:
  - Custom commands: https://docs.djangoproject.com/en/stable/howto/custom-management-commands/

  **Python PRAW (Reddit API)**:
  - PRAW docs: https://praw.readthedocs.io/

  **WHY Each Reference Matters**:
  - Django docs: Management command structure for data import
  - PRAW docs: Reddit API for scraping

  **Acceptance Criteria**:

  **TDD (tests enabled)**:
  - [ ] Test: `test_seeding.py` validates tip creation
  - [ ] Test: Asserts 50+ tips in database
  - [ ] Test: Asserts tips distributed across 4 categories
  - [ ] pytest backend/tests/test_seeding.py → PASS (5+ tests)

  **Automated Verification**:
  ```bash
  # Agent runs:
  python backend/manage.py seed_tips
  # Assert: Exit code 0, messages show tip count

  psql $DATABASE_URL -c "SELECT category_id, COUNT(*) FROM tips GROUP BY category_id;"
  # Assert: Returns 4 rows with ~12-13 tips each
  ```

  **Evidence to Capture**:
  - [ ] Seeding output showing tip counts
  - [ ] Database query output

  **Commit**: YES
  - Message: `feat: seed 50+ reddit tips (manual curation)`
  - Files: `backend/apps/wiki/management/commands/seed_tips.py`, `scripts/scraped-tips.json`

### Wave 4: Optimization & Deployment (Weeks 10-12)

- [ ] 10. SEO Optimization

  **What to do**:
  - Add Schema.org Article markup to tip pages
  - Implement clean URLs (lowercase, hyphen-separated)
  - Add meta tags (title, description, keywords)
  - Generate sitemap.xml
  - Add robots.txt

  **Must NOT do**:
  - Implement advanced SEO (A/B testing, dynamic sitemaps, noindex for low-quality pages)

  **Recommended Agent Profile**:
  > - **Category**: `quick`
    - Reason: SEO implementation, schema markup
  - **Skills**: `[]`
    - Schema.org well-documented

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 4 (with Tasks 11, 12)
  - **Blocks**: Task 12 (deployment needs SEO)
  - **Blocked By**: Task 5 (frontend components needed)

  **References**:

  **Schema.org Article**:
  - Schema: https://schema.org/Article
  - JSON-LD format: https://developers.google.com/search/docs/appearance/structured-data

  **Django Sitemaps**:
  - Django contrib: https://docs.djangoproject.com/en/stable/ref/contrib/sitemaps/

  **WHY Each Reference Matters**:
  - Schema.org: Standard for rich snippets
  - Django sitemaps: Built-in sitemap generation

  **Acceptance Criteria**:

  **TDD (tests enabled)**:
  - [ ] Test: `test_seo.py` validates Schema.org markup
  - [ ] Test: Asserts JSON-LD contains Article type
  - [ ] Test: Asserts clean URLs (lowercase, hyphens)
  - [ ] pytest backend/tests/test_seo.py → PASS (8+ tests)

  **Automated Verification**:
  ```bash
  # Agent runs:
  curl -s http://localhost:3000/tip/1 | grep -o 'schema.org/Article'
  # Assert: Schema.org markup present

  curl -s http://localhost:3000/sitemap.xml | grep -c '<loc>'
  # Assert: Returns at least 50 URLs

  curl -s http://localhost:3000/robots.txt | grep -o 'Disallow'
  # Assert: robots.txt accessible
  ```

  **Evidence to Capture**:
  - [ ] HTML output showing Schema.org markup
  - [ ] Sitemap output

  **Commit**: YES
  - Message: `feat: implement seo optimization (schema.org, sitemap, meta tags)`
  - Files: `frontend/src/components/TipDetailPage.tsx` (Schema markup), `backend/apps/wiki/sitemaps.py`

- [ ] 11. Content Moderation

  **What to do**:
  - Implement keyword blacklist (cut, needle, knife, bleed, overdose, etc.)
  - Add Cloudflare Turnstile to submission form (done in Task 6)
  - Implement HuggingFace zero-shot classification for AI flagging
  - Store IP hashes (GDPR compliant)
  - Set 7-day expiration for IP records

  **Must NOT do**:
  - Create human moderation queue (AI flagging only)
  - Implement advanced moderation (reputation, appeal process)

  **Recommended Agent Profile**:
  > - **Category**: `quick`
    - Reason: Content safety implementation
  - **Skills**: `[]`
    - HuggingFace transformers well-documented

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 4 (with Tasks 10, 12)
  - **Blocks**: Task 12 (deployment needs moderation)
  - **Blocked By**: Task 4 (API endpoint needed)

  **References**:

  **HuggingFace Transformers**:
  - Zero-shot classification: https://huggingface.co/docs/transformers/main_classes/pipelines#zero-shot-classification-pipeline
  - Model: facebook/bart-large-mnli

  **Django-ratelimit**:
  - https://django-ratelimit.readthedocs.io/en/latest/ratelimit.html

  **GDPR IP Handling**:
  - Hashing: Python `hashlib` docs: https://docs.python.org/3/library/hashlib.html

  **WHY Each Reference Matters**:
  - HuggingFace: AI moderation implementation
  - django-ratelimit: IP-based rate limiting
  - Hashlib: GDPR-compliant IP anonymization

  **Acceptance Criteria**:

  **TDD (tests enabled)**:
  - [ ] Test: `test_moderation.py` tests keyword blacklist
  - [ ] Test: Asserts prohibited terms blocked
  - [ ] Test: Asserts AI flagging detects self-harm
  - [ ] Test: Asserts IP hashes created and expired
  - [ ] pytest backend/tests/test_moderation.py → PASS (15+ tests)

  **Automated Verification**:
  ```bash
  # Agent runs:
  curl -X POST http://localhost:8000/api/tips/ \
    -H "Content-Type: application/json" \
    -d '{"title":"Test","description":"Cut yourself","category":"oral-hygiene","products":[]}'
  # Assert: 400 Bad Request, error mentions blacklist

  curl -X POST http://localhost:8000/api/tips/ \
    -H "Content-Type: application/json" \
    -d '{"title":"Test","description":"This bleach kills all bacteria","category":"oral-hygiene","products":[]}'
  # Assert: 400 Bad Request, AI flag triggered
  ```

  **Evidence to Capture**:
  - [ ] Moderation test output
  - [ ] IP hash verification showing expiration

  **Commit**: YES
  - Message: `feat: implement content moderation (keyword blacklist, ai flagging, gdpr ip handling)`
  - Files: `backend/apps/wiki/middleware.py`, `backend/apps/wiki/utils.py` (moderation)

- [ ] 12. Deploy to Production

  **What to do**:
  - Deploy Django backend to Railway/Render
  - Deploy React frontend to Vercel
  - Configure CORS for API
  - Set up environment variables (DATABASE_URL, TURNSTILE_SECRET_KEY)
  - Test production endpoints
  - Verify SEO on production URLs

  **Must NOT do**:
  - Set up staging environment
  - Configure CI/CD pipelines

  **Recommended Agent Profile**:
  > - **Category**: `quick`
    - Reason: Deployment to production platforms
  - **Skills**: `[git-master]`
    - Git for deployment commits

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 4 (final)
  - **Blocks**: None (final task)
  - **Blocked By**: Tasks 10, 11 (all features needed)

  **References**:

  **Vercel Deployment**:
  - Docs: https://vercel.com/docs/deployments/overview
  - Build settings: https://vercel.com/docs/projects/configuration-overview

  **Railway Deployment**:
  - Docs: https://docs.railway.app/deploy/dockerfiles

  **Django CORS**:
  - django-cors-headers: https://pypi.org/project/django-cors-headers/

  **WHY Each Reference Matters**:
  - Vercel docs: React deployment steps
  - Railway docs: Django deployment on Railway
  - Django CORS: Frontend-backend API communication

  **Acceptance Criteria**:

  **TDD (tests enabled)**:
  - [ ] Test: `test_deployment.py` verifies production endpoints
  - [ ] Test: Asserts frontend accessible
  - [ ] Test: Asserts backend API accessible
  - [ ] Test: Asserts CORS headers present
  - [ ] pytest backend/tests/test_deployment.py → PASS (5+ tests)

  **Automated Verification**:
  ```bash
  # Agent runs:
  curl -s https://microhygiene-wiki.vercel.app/ | grep -o 'Micro-Hygiene Wiki'
  # Assert: Homepage loads

  curl -s https://api.microhygiene-wiki.com/health | jq '.status'
  # Assert: Returns "ok"

  curl -s -I https://api.microhygiene-wiki.com/api/tips/ | grep -o 'Access-Control-Allow-Origin'
  # Assert: CORS headers present
  ```

  **Evidence to Capture**:
  - [ ] Production homepage screenshot
  - [ ] Health check output
  - [ ] CORS header verification

  **Commit**: YES
  - Message: `chore: deploy to production (vercel + railway)`
  - Files: Deployment configuration files

---

## Direct Deliverables (Delivered as part of TODOs)

### Deliverable 1: 50 Long-Tail SEO Phrases

**Location**: `docs/seo-phrases.md`

**Content**: 50 long-tail keyword phrases for tonsil stones and body odor with low competition but high intent

**Examples**:
- "how to remove tonsil stones without gagging"
- "tonsil stones home remedy hydrogen peroxide"
- "get rid of tonsil stones naturally overnight"
- "chronic body odor armpits natural remedies"
- "body odor sweat gland blockage treatment"
- "how to stop armpit sweating permanently"
- "underarm odor baking soda paste"
- "fungal skin bumps home treatment"
- "genital odor probiotics feminine"

**Verification**: File exists with 50+ lines

### Deliverable 2: Python Keyword Filtering Script

**Location**: `scripts/filter_keywords.py`

**Content**: Script that filters content against blacklist keywords using set-based lookup

**Usage**:
```bash
python scripts/filter_keywords.py --input "Test content" --output filtered.json
```

**Features**:
- Keyword blacklist check (O(n) set lookup)
- Context-aware exceptions (e.g., "suicide prevention" allowed)
- Returns blocked terms and severity level

**Verification**: Script returns JSON with `blocked: true` for prohibited content

### Deliverable 3: 20 Reddit Tips Scraped

**Location**: `scripts/scraped-tips.json`

**Content**: 20 top-voted tips from r/AskDocs and r/Hygiene subreddits, manually curated

**Structure**:
```json
[
  {
    "title": "Tonsil stones hydrogen peroxide gargle",
    "description": "Mix 3% hydrogen peroxide with water...",
    "category": "oral-hygiene",
    "products": ["hydrogen peroxide", "waterpik"],
    "source": "r/AskDocs",
    "upvotes": 342
  }
]
```

**Verification**: JSON valid, contains 20 tip objects

### Deliverable 4: Affiliate Mapping System

**Location**: `backend/apps/wiki/utils.py` (affiliate link generator), `backend/apps/wiki/fixtures/affiliate_products.json`

**Content**: Keyword-to-affiliate-URL mapping system for Amazon + iHerb

**Structure**:
```json
{
  "waterpik": {
    "amazon": "https://amazon.com/dp/B00ABC123?tag=YOUR_AFFILIATE_ID",
    "iherb": "https://iherb.com/pr/Product.aspx?pid=YOUR_ID&rcode=PRODUCT_CODE"
  },
  "hydrogen peroxide": {
    "amazon": "https://amazon.com/s?k=hydrogen+peroxide&tag=YOUR_AFFILIATE_ID"
  }
}
```

**Features**:
- Keyword-based autolinking
- rel="nofollow sponsored" attributes
- Context-aware replacement (limits to 3 matches per page)

**Verification**: Affiliate links generated for mapped products

---

## Success Criteria

### Verification Commands
```bash
# Backend health
curl -s https://api.microhygiene-wiki.com/health | jq '.status'
# Expected: "ok"

# Frontend load
curl -s https://microhygiene-wiki.vercel.app/ | grep -o 'Micro-Hygiene Wiki'
# Expected: Page title visible

# API tip list
curl -s https://api.microhygiene-wiki.com/api/tips/ | jq '.results | length'
# Expected: 20 or fewer (paginated)

# Database tip count
psql $DATABASE_URL -c "SELECT COUNT(*) FROM tips;"
# Expected: 50+

# Schema.org markup
curl -s https://microhygiene-wiki.vercel.app/tip/1 | grep -o 'schema.org/Article'
# Expected: Markup present

# All tests pass
pytest backend/tests/ --cov=backend --cov-report=term
# Expected: Exit code 0, coverage >80%

# Frontend build
cd frontend && npm run build
# Expected: Exit code 0
```

### Final Checklist
- [ ] All "Must Have" features present
- [ ] All "Must NOT Have" features absent
- [ ] All tests passing (>80% coverage)
- [ ] 50+ tips seeded and accessible
- [ ] Voting system functional
- [ ] Affiliate links present for mapped products
- [ ] Medical disclaimer on all pages
- [ ] Cloudflare Turnstile functional
- [ ] IP-based rate limiting enforced
- [ ] Keyword blacklist blocking
- [ ] Schema.org markup present
- [ ] SEO-optimized URLs
- [ ] Frontend deployed to Vercel
- [ ] Backend deployed to Railway/Render
- [ ] Production endpoints tested and accessible

---

## Appendix: Key Decisions & Defaults

### Technical Defaults (Auto-Resolved)
- **Search**: PostgreSQL full-text search (not Elasticsearch) - Simplified for MVP
- **Django Hosting**: Railway or Render (not Vercel) - Django requires server runtime
- **Affiliate Integration**: Static link mapping (not real-time API) - Defers to post-MVP
- **Moderation**: AI flagging + keyword blacklist (no human queue) - Scalable for MVP
- **Testing**: TDD with pytest/vitest - User requested
- **GDPR**: IP hashed + 7-day expiration - Legal compliance

### Business Defaults (Auto-Resolved)
- **Revenue Model**: Static affiliate links only - No conversion tracking for MVP
- **Content Validation**: Manual curation of 50 Reddit tips - Quality assurance
- **Vote Display**: "No votes yet" for zero votes - User-friendly
- **Conflicting Tips**: Chronological display + voting - Let users decide
- **Missing Products**: "Affiliate link not available" message - Graceful fallback

### Guardrails (From Metis Review)
- NO user accounts (anonymous only)
- NO email notifications
- NO real-time features
- NO human moderation queue
- NO advanced search (autocomplete, filters)
- NO analytics dashboard
- NO staging environment
- NO multi-language support
- NO social sharing beyond basic
- NO custom component library
- NO CDN beyond Vercel
- NO A/B testing
- NO content versioning
- NO comment system
- NO performance testing

---

## Estimated Timeline

**Wave 1: Foundation (Weeks 1-2)**
- Task 1: Setup project structure - 2 days
- Task 2: Configure Supabase - 1 day
- Task 3: Create Django models - 3 days

**Wave 2: Core Features (Weeks 3-6)**
- Task 4: Implement Django REST API - 2 weeks
- Task 5: Build React frontend - 2 weeks
- Task 6: Setup Cloudflare Turnstile - 3 days

**Wave 3: Advanced Features (Weeks 7-9)**
- Task 7: Affiliate link generation - 1 week
- Task 8: Voting system - 1 week
- Task 9: Seed Reddit tips - 1 week

**Wave 4: Optimization & Deployment (Weeks 10-12)**
- Task 10: SEO optimization - 1 week
- Task 11: Content moderation - 1 week
- Task 12: Deploy to production - 1 week

**Total**: 8-12 weeks (aligned with user request)

---

## Notes

- This plan assumes single developer working full-time
- Parallel execution reduces total time by ~40%
- Weekly deliverables track progress against timeline
- All acceptance criteria are agent-executable (no user intervention required)
- TDD workflow ensures quality from start
- GDPR compliance built-in with IP hashing
- SEO optimized for long-tail keywords from day 1
- Affiliate revenue generation via static links (scalable to real-time API post-MVP)
