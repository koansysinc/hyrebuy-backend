# Deploy HyreBuy Backend to Railway

## Quick Start (5 Minutes)

### Step 1: Sign Up & Create Project

1. Go to **https://railway.app**
2. Click **"Start a New Project"** or **"Login with GitHub"**
3. Authorize Railway to access your GitHub repositories

### Step 2: Deploy from GitHub

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose **`koansysinc/hyrebuy-backend`**
4. Railway will automatically:
   - Detect Python project
   - Use `railway.json` configuration
   - Use `Procfile` for start command
   - Install dependencies from `requirements.txt`

### Step 3: Add Environment Variables

Click **"Variables"** tab and add these **one by one**:

**DATABASE_URL**
```
postgresql+asyncpg://f1061be62d163a20e0f4fd1aeeb789bacb6032c49341308e7891068696c56746:sk_fSCX2wag8FWJy4PdjSO3H@db.prisma.io:5432/postgres?ssl=require
```

**SECRET_KEY**
```
efd8b2ed956a7ae4f5d994dfdbe29fd8fafb36fc428b658dc0220daf30437f25
```

**ALLOWED_ORIGINS**
```
https://frontend-hyrebuy.vercel.app,https://hyrebuy-frontend-ikhr1fp7v-koansysincs-projects.vercel.app
```

**APP_NAME** (optional)
```
HyreBuy API
```

**ENVIRONMENT** (optional)
```
production
```

### Step 4: Generate Public Domain

1. Go to **"Settings"** tab
2. Scroll to **"Networking"** section
3. Click **"Generate Domain"**
4. Copy your Railway URL (e.g., `https://hyrebuy-backend-production.up.railway.app`)

### Step 5: Deploy

Railway will automatically deploy after you add the environment variables!

- Watch the **"Deployments"** tab for build progress
- Build typically takes **2-5 minutes**
- Once status shows **"Success"**, your API is live!

### Step 6: Test Your Deployment

Test these endpoints:

```bash
# Health check
curl https://your-railway-url.up.railway.app/health

# API Documentation
# Open in browser: https://your-railway-url.up.railway.app/docs
```

### Step 7: Update Frontend

Go to Vercel and update the environment variable:

1. Go to **Vercel Dashboard** → **hyrebuy-frontend** → **Settings** → **Environment Variables**
2. Update **`NEXT_PUBLIC_API_URL`** to your Railway URL
3. Redeploy frontend

---

## Railway Configuration Files (Already in Repo)

### `railway.json`
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### `Procfile`
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### `runtime.txt`
```
python-3.11.9
```

---

## Cost & Trial

- **Trial Credit**: $5 (automatically applied)
- **Usage**: ~$1-2/month for small apps
- **Trial duration**: Lasts several weeks for development
- **No credit card required** for trial

---

## Why Railway Works Better Than Render

✅ **Better Python Build Environment**
- Handles Rust/C compilation automatically
- Pre-built binaries for common packages
- Faster dependency installation

✅ **Faster Deployments**
- 2-5 minutes vs 10-15 minutes
- Better caching
- Instant rebuilds on code changes

✅ **Better Logs**
- Real-time deployment logs
- Runtime logs accessible via dashboard
- Easier debugging

✅ **Auto-Deploy from GitHub**
- Every git push triggers deployment
- No manual redeploy needed

❌ **Not Completely Free**
- But $5 trial lasts weeks
- Very affordable ($1-2/mo for small apps)

---

## Troubleshooting

### Build fails with "Module not found"
- Check that all dependencies are in `requirements.txt`
- Railway uses Python 3.11.9 from `runtime.txt`

### App crashes on startup
- Check "Deploy Logs" in Railway dashboard
- Verify environment variables are set correctly
- Make sure DATABASE_URL is accessible

### Can't access the app
- Make sure domain is generated in Settings → Networking
- Check that deploy status shows "Success"
- Try accessing `/health` endpoint first

---

## Next Steps After Deployment

1. ✅ Test all API endpoints via `/docs`
2. ✅ Update frontend NEXT_PUBLIC_API_URL
3. ✅ Test frontend → backend integration
4. ✅ Monitor logs in Railway dashboard

Your backend should be live in 5 minutes!
