# HyreBuy Backend - Vercel Deployment

## Quick Deploy

### Option 1: Deploy via Vercel CLI

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy from this directory:
```bash
cd hyrebuy-backend
vercel
```

4. Follow the prompts:
   - Set up and deploy? **Y**
   - Which scope? **Your account**
   - Link to existing project? **N**
   - Project name? **hyrebuy-backend**
   - Directory? **./** (press Enter)
   - Override settings? **N**

5. Set environment variables:
```bash
vercel env add DATABASE_URL production
vercel env add SECRET_KEY production
vercel env add ALLOWED_ORIGINS production
# ... add all other variables from .env.production.example
```

6. Deploy to production:
```bash
vercel --prod
```

### Option 2: Deploy via GitHub

1. Push to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin YOUR_REPO_URL
git push -u origin main
```

2. Import in Vercel Dashboard:
   - Go to https://vercel.com/new
   - Import your repository
   - Add environment variables
   - Deploy

## Environment Variables Required

Copy from `.env.production.example` and set these in Vercel:

```
APP_NAME
APP_VERSION
ENVIRONMENT
DEBUG
DATABASE_URL
REDIS_URL
SECRET_KEY
ALLOWED_ORIGINS
OSRM_API_URL
EMAIL_FROM
LOG_LEVEL
```

## Files for Deployment

- `vercel.json` - Vercel configuration
- `index.py` - Serverless function entry point
- `runtime.txt` - Python version
- `requirements.txt` - Python dependencies
- `.vercelignore` - Files to exclude from deployment

## Testing After Deployment

```bash
# Replace YOUR_DEPLOYMENT_URL with your actual URL
curl https://YOUR_DEPLOYMENT_URL.vercel.app/health
curl https://YOUR_DEPLOYMENT_URL.vercel.app/api/v1/properties?limit=1
```

## Troubleshooting

### Check Logs
```bash
vercel logs YOUR_DEPLOYMENT_URL.vercel.app
```

### Common Issues
1. **500 Error**: Check environment variables are set
2. **Database Error**: Verify DATABASE_URL format
3. **Import Error**: Check all dependencies in requirements.txt
