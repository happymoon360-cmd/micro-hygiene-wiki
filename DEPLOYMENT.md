# Deployment Guide

This guide walks you through deploying the Micro-Hygiene Wiki to production using Railway (or Render) for the Django backend and Vercel for the React frontend.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Django Backend Deployment (Railway/Render)](#django-backend-deployment-railwayrender)
- [React Frontend Deployment (Vercel)](#react-frontend-deployment-vercel)
- [Environment Variables Setup](#environment-variables-setup)
- [Post-Deployment Verification](#post-deployment-verification)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before deploying, ensure you have:

1. **Git repository** with all code committed
2. **Accounts created:**
   - [Railway](https://railway.app/) or [Render](https://render.com/)
   - [Vercel](https://vercel.com/)
3. **Domain name** (optional, but recommended for production)
4. **Cloudflare Turnstile account** for bot protection (free tier available)

---

## Django Backend Deployment (Railway/Render)

### Option A: Deploy to Railway (Recommended)

#### Step 1: Create New Project

1. Log in to [Railway](https://railway.app/)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your Micro-Hygiene Wiki repository
5. Select the `backend` directory as the root directory

#### Step 2: Configure Build Settings

Railway will automatically detect Python and use your `requirements.txt`.

**Build Settings:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn config.wsgi --bind 0.0.0.0:$PORT --workers 3`

#### Step 3: Add PostgreSQL Database

1. In your Railway project, click **"+ New"**
2. Select **"Add a Database"**
3. Choose **"PostgreSQL"**
4. Railway will automatically create a PostgreSQL instance

#### Step 4: Set Environment Variables

In Railway, go to your Django service → **Variables** tab and add:

```
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-railway-app-url.railway.app,localhost
FRONTEND_URL=https://your-vercel-app.vercel.app
TURNSTILE_SECRET_KEY=your-turnstile-secret-key
```

**Important:** Railway automatically sets `DATABASE_URL` for the PostgreSQL database - you don't need to set this manually.

#### Step 5: Deploy

1. Click **"Deploy"**
2. Railway will build and deploy your Django app
3. The Procfile will automatically run migrations on deployment

Your backend will be available at: `https://your-app-name.railway.app`

---

### Option B: Deploy to Render

#### Step 1: Create New Web Service

1. Log in to [Render](https://render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Set **Root Directory** to `backend`
5. Configure settings:
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`

#### Step 2: Add PostgreSQL Database

1. In your Render dashboard, click **"New +"** → **"PostgreSQL"**
2. Render will create a database instance
3. Copy the **Internal Database URL** from the database service

#### Step 3: Set Environment Variables

In your Render web service → **Environment** tab, add:

```
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com,localhost
FRONTEND_URL=https://your-vercel-app.vercel.app
TURNSTILE_SECRET_KEY=your-turnstile-secret-key
DATABASE_URL=postgresql://user:password@host:port/database_name
```

Replace `DATABASE_URL` with the Internal Database URL from Step 2.

#### Step 4: Deploy

1. Click **"Create Web Service"**
2. Render will deploy your Django backend

Your backend will be available at: `https://your-app-name.onrender.com`

---

## React Frontend Deployment (Vercel)

### Step 1: Deploy to Vercel

1. Log in to [Vercel](https://vercel.com/)
2. Click **"Add New Project"**
3. Import your GitHub repository
4. Set **Root Directory** to `frontend`
5. Vercel will automatically detect Vite from your `vercel.json`

### Step 2: Configure Build Settings

Vercel will use the settings from your `vercel.json`:

- **Framework Preset:** Vite
- **Build Command:** `npm run build`
- **Output Directory:** `dist`

### Step 3: Set Environment Variables

In Vercel project settings → **Environment Variables**, add:

```
VITE_API_URL=https://your-railway-app.railway.app
VITE_TURNSTILE_SITE_KEY=your-turnstile-site-key
```

**Note:** Vercel environment variables prefixed with `VITE_` are automatically available in your React app.

### Step 4: Deploy

1. Click **"Deploy"**
2. Vercel will build and deploy your React app
3. Once deployed, copy your Vercel URL

Your frontend will be available at: `https://your-project-name.vercel.app`

---

## Environment Variables Setup

### Generate Required Keys

#### 1. Django SECRET_KEY

Generate a secure secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### 2. Cloudflare Turnstile

1. Go to [Cloudflare Turnstile Dashboard](https://dash.cloudflare.com/?to=/:account/turnstile)
2. Create a new site
3. Copy the **Site Key** (frontend) and **Secret Key** (backend)

### Backend Environment Variables (Railway/Render)

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `django-insecure-abc123...` |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Allowed domain(s) | `app.railway.app,localhost` |
| `FRONTEND_URL` | Frontend URL (for CORS) | `https://app.vercel.app` |
| `TURNSTILE_SECRET_KEY` | Turnstile secret key | `0x4AAA...` |
| `DATABASE_URL` | PostgreSQL connection | (Auto-set by Railway/Render) |

### Frontend Environment Variables (Vercel)

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `https://app.railway.app` |
| `VITE_TURNSTILE_SITE_KEY` | Turnstile site key | `0x4AAA...` |

---

## Post-Deployment Verification

### Backend Health Check

#### Check if backend is running:

```bash
curl https://your-railway-app.railway.app/
```

You should see a response with Django's default page or your API response.

#### Check Django Admin:

```bash
curl https://your-railway-app.railway.app/admin/
```

Should redirect to login page (403 response if not authenticated).

### Frontend Verification

1. Visit your Vercel URL: `https://your-app.vercel.app`
2. Check browser console for any errors
3. Verify the page loads correctly

### Test CORS Configuration

1. Open browser DevTools → Console
2. Visit your frontend
3. Make an API request from browser console:

```javascript
fetch('https://your-railway-app.railway.app/api/tips/')
  .then(response => response.json())
  .then(data => console.log(data))
```

If CORS is configured correctly, you should not see CORS errors.

### Verify Database Connection

Check Railway/Render logs to ensure:

1. Migrations ran successfully
2. Database connection is established
3. No database-related errors

---

## Troubleshooting

### Backend Issues

#### 1. "Bad Request (400)" Error

**Cause:** `ALLOWED_HOSTS` doesn't include your backend domain.

**Solution:**
- Add your Railway/Render URL to `ALLOWED_HOSTS` environment variable
- Format: `ALLOWED_HOSTS=app.railway.app,localhost`

#### 2. "DisallowedHost" Error

**Cause:** Same as above - `ALLOWED_HOSTS` misconfigured.

**Solution:**
- Ensure your domain is in the `ALLOWED_HOSTS` list
- Separate multiple hosts with commas: `domain1.com,domain2.com`

#### 3. Database Connection Error

**Cause:** `DATABASE_URL` not set correctly.

**Solution:**
- On Railway: Check that PostgreSQL service is attached
- On Render: Verify `DATABASE_URL` matches the Internal Database URL
- Check logs for specific database errors

#### 4. CORS Errors in Browser

**Cause:** Frontend URL not in Django CORS allowed origins.

**Solution:**
- Verify `FRONTEND_URL` environment variable is set correctly
- Check Django settings: `CORS_ALLOWED_ORIGINS` should include your Vercel URL
- For debugging: In `settings.py`, set `DEBUG=True` temporarily (only in development!)

### Frontend Issues

#### 1. "Failed to fetch" API Errors

**Cause:** Backend URL incorrect or CORS not configured.

**Solution:**
- Check `VITE_API_URL` in Vercel environment variables
- Verify backend is accessible via `curl`
- Check CORS settings on backend

#### 2. Build Fails on Vercel

**Cause:** Missing dependencies or configuration issues.

**Solution:**
- Check Vercel build logs for specific errors
- Ensure all dependencies are in `package.json`
- Verify `vercel.json` is correctly configured

#### 3. 404 Not Found on All Pages

**Cause:** `vercel.json` rewrites not configured.

**Solution:**
- Ensure `vercel.json` has SPA rewrites configured
- Verify build output directory is correct (`dist`)

### Database Issues

#### 1. Migrations Not Running on Deploy

**Cause:** Procfile not set up correctly.

**Solution:**
- Ensure Procfile has: `release: python manage.py migrate --noinput`
- Check Railway/Render logs for migration output

#### 2. Database is Empty

**Cause:** No fixtures or initial data loaded.

**Solution:**
- Run `python manage.py loaddata <fixture-file>` locally
- Or create a Django admin user and add data via admin panel

---

## Custom Domain Setup (Optional)

### Backend Custom Domain

**Railway:**
1. Go to project → Settings → Domains
2. Add your custom domain
3. Update DNS settings per Railway's instructions

**Render:**
1. Go to web service → Settings → Custom Domains
2. Add your domain
3. Update DNS A records

### Frontend Custom Domain

**Vercel:**
1. Go to project → Settings → Domains
2. Add your custom domain
3. Update DNS settings per Vercel's instructions

### Update Environment Variables

After setting custom domains, update:

**Backend:**
- `ALLOWED_HOSTS=backend.yourdomain.com,localhost`

**Frontend:**
- `VITE_API_URL=https://backend.yourdomain.com`

**Backend (for CORS):**
- `FRONTEND_URL=https://yourdomain.com`

---

## Security Best Practices

1. **Never commit `.env` files** - Use `.env.example` instead
2. **Generate strong SECRET_KEY** for production
3. **Set DEBUG=False** in production
4. **Use HTTPS** for all production URLs
5. **Rotate API keys** regularly
6. **Monitor logs** for suspicious activity
7. **Keep dependencies updated** regularly

---

## Cost Estimation

### Free Tier Limits

**Railway Free Tier:**
- $5 free credit per month
- PostgreSQL: Included
- 512MB RAM, 0.5 CPU

**Render Free Tier:**
- 750 hours/month (enough for 1 web service + 1 database)
- PostgreSQL: Included
- 512MB RAM

**Vercel Free Tier:**
- Unlimited deployments
- 100GB bandwidth/month
- Serverless functions

### Estimated Production Costs

**Backend (Railway):** ~$5-20/month depending on traffic
**Database (Railway):** ~$5-15/month depending on size
**Frontend (Vercel):** Free - $20/month depending on bandwidth

---

## Support

- **Railway Docs:** https://docs.railway.app/
- **Render Docs:** https://render.com/docs
- **Vercel Docs:** https://vercel.com/docs
- **Django Deployment:** https://docs.djangoproject.com/en/6.0/howto/deployment/

---

**Last Updated:** January 2025
