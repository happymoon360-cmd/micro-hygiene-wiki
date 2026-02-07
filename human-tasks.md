# Human-Only Tasks

These tasks require human identity, account ownership, or manual platform interaction.
AI agents cannot do these — they need your hands.

---

## One-Time Setup (Do These First)

### 1. Domain & Hosting Accounts

- [ ] **Buy a domain** (Namecheap, Cloudflare, etc.)
  - Suggestion: `microhygiene.wiki` or `microhygienewiki.com`
  - ~$10-15/year

- [ ] **Create a Railway account** → https://railway.app
  - Deploy backend (follow `DEPLOYMENT.md`)
  - Set environment variables: `SECRET_KEY`, `FRONTEND_URL`, `ALLOWED_HOSTS`, `DEBUG=False`

- [ ] **Create a Vercel account** → https://vercel.com
  - Deploy frontend
  - Set environment variables: `VITE_API_URL`, `VITE_TURNSTILE_SITE_KEY`

- [ ] **Point domain DNS** to Vercel (frontend) and Railway (backend API subdomain)

### 2. Cloudflare Turnstile (CAPTCHA)

- [ ] **Create Cloudflare account** → https://dash.cloudflare.com
- [ ] **Get Turnstile site key + secret key** (free tier)
  - Dashboard → Turnstile → Add Site
  - Copy Site Key → Vercel env var `VITE_TURNSTILE_SITE_KEY`
  - Copy Secret Key → Railway env var `TURNSTILE_SECRET_KEY`

### 3. Google Search Console

- [ ] **Register site** → https://search.google.com/search-console
- [ ] **Verify domain ownership** (DNS TXT record or HTML file)
- [ ] **Submit sitemap** → `https://yourdomain.com/sitemap.xml`
- [ ] **Request indexing** for the homepage

### 4. Google Analytics (Optional but Recommended)

- [ ] **Create GA4 property** → https://analytics.google.com
- [ ] **Add tracking snippet** to `frontend/index.html`
- [ ] Verify data is flowing after first visit

### 5. Amazon Associates (Affiliate)

- [ ] **Sign up** → https://affiliate-program.amazon.com
- [ ] Wait for approval
- [ ] Note: You must generate 3 qualifying sales within 180 days or the account closes
- [ ] Recommendation: Apply AFTER you have some traffic (at least 100 visits/day)
- [ ] Once approved, replace placeholder ASINs in `affiliate_products.json` with real affiliate URLs containing your tag

---

## Weekly Routine (~2 hours/week)

### Monday (30 min)

- [ ] Review AI-generated Reddit drafts in `marketing/reddit_drafts.md`
- [ ] Edit if needed (adjust tone, fix anything that sounds robotic)
- [ ] Post 1-2 to target subreddits from your Reddit account
- [ ] Reply to any comments on previous posts

### Wednesday (1 hour) — Optional, skip if too busy

- [ ] Pick 1 script from `marketing/shortform_scripts.md`
- [ ] Record/create video using CapCut or Canva (use templates for speed)
- [ ] Upload to TikTok + Instagram Reels + YouTube Shorts
- [ ] Add site link to bio/profile

### Friday (30 min)

- [ ] Check Google Search Console: which queries are driving impressions?
- [ ] Check site analytics: which tips get the most views?
- [ ] Note down content gaps (searches with impressions but no clicks = title/description needs work)
- [ ] If a newsletter tool is set up, review and send the weekly newsletter

---

## Monthly Tasks (~1 hour/month)

### Analytics Review

- [ ] Check Google Search Console performance report
  - Which keywords are growing?
  - Which pages have high impressions but low CTR? (= rewrite titles/descriptions)
- [ ] Check affiliate earnings (if active)
- [ ] Decide if any new categories or tip topics are needed based on search data

### Content Refresh

- [ ] Flag outdated tips for AI agent to rewrite
- [ ] If keyword research (`marketing/keywords.md`) shows gaps, ask AI agent to generate new tips for those topics

---

## Platform Accounts Checklist

You will need accounts on these platforms. Create them when ready:

| Platform | Purpose | Free? | Priority |
|----------|---------|-------|----------|
| Railway | Backend hosting | Free tier available | Must have |
| Vercel | Frontend hosting | Free tier | Must have |
| Cloudflare | Turnstile CAPTCHA + DNS | Free | Must have |
| Google Search Console | SEO monitoring | Free | Must have |
| Google Analytics | Traffic tracking | Free | Recommended |
| Reddit | Community marketing | Free | Recommended |
| Amazon Associates | Affiliate revenue | Free | After traffic |
| TikTok | Short-form video | Free | Optional |
| Instagram | Reels + link in bio | Free | Optional |
| Buttondown / Substack | Newsletter | Free tier | Optional |

---

## Notes

- Don't try to do everything at once. Start with deployment + Google Search Console. That's enough for week 1.
- Reddit posts are the fastest way to get initial traffic. One good post on r/CleaningTips can bring 1000+ visitors in a day.
- Short-form video is high effort but high reward. Skip it if you don't have time — SEO + Reddit alone can sustain a niche site.
- Never pay for ads before you have at least 1 month of organic traffic data. You need to know which content resonates first.
