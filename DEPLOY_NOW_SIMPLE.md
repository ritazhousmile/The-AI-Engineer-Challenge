# 🚀 Deploy Now - Simple Guide

The fastest way to deploy your chatbot. Choose one method below.

## 🎯 Method 1: Vercel Dashboard (Easiest - Recommended)

**No command line needed!** Just follow these steps in your browser.

### ⚡ Quick Steps

1. **Push code to GitHub** (if not already):
   ```bash
   git push origin main
   ```

2. **Deploy Backend:**
   - Go to: https://vercel.com/new
   - Import: `ritazhousmile/The-AI-Engineer-Challenge`
   - Settings:
     - Name: `mental-coach-api`
     - Framework: **Other**
     - Root: (empty)
   - Environment Variables → Add:
     ```
     OPENAI_API_KEY = your-openai-key
     DB_PATH = /tmp/conversations.db
     RATE_LIMIT_ENABLED = true
     RATE_LIMIT_REQUESTS = 60
     RATE_LIMIT_WINDOW = 60
     ALLOWED_ORIGINS = *
     ```
   - Click **Deploy** → Wait 1-2 min → Copy URL

3. **Deploy Frontend:**
   - Go to: https://vercel.com/new (again)
   - Import: Same repo
   - Settings:
     - Name: `mental-coach-frontend`
     - Framework: **Next.js**
     - Root: `frontend`
   - Environment Variables → Add:
     ```
     NEXT_PUBLIC_API_URL = your-backend-url-from-step-2
     ```
   - Click **Deploy** → Wait 2-3 min → Done! 🎉

**That's it!** Your chatbot is live.

---

## 🖥️ Method 2: Command Line (Advanced)

If you prefer command line:

### Step 1: Login to Vercel

```bash
vercel login
```

This will open your browser for authentication.

### Step 2: Run Deployment Script

```bash
./deploy_v2.sh
```

The script will:
- Deploy backend
- Set environment variables
- Deploy frontend
- Connect them together
- Test the deployment

### Step 3: Manual Environment Variables (if script fails)

**Backend:**
```bash
cd /path/to/project
vercel env add OPENAI_API_KEY production
# Paste your OpenAI key when prompted

vercel env add DB_PATH production
# Enter: /tmp/conversations.db

vercel env add RATE_LIMIT_ENABLED production
# Enter: true

vercel env add RATE_LIMIT_REQUESTS production
# Enter: 60

vercel env add RATE_LIMIT_WINDOW production
# Enter: 60

vercel env add ALLOWED_ORIGINS production
# Enter: *

vercel --prod
```

**Frontend:**
```bash
cd frontend
vercel env add NEXT_PUBLIC_API_URL production
# Enter your backend URL (e.g., https://mental-coach-api-xyz.vercel.app)

vercel --prod
```

---

## ✅ Quick Test

After deployment, test it:

```bash
# Test backend
curl https://your-backend-url.vercel.app/api/health

# Should return:
# {"status":"ok","version":"2.0.0","database":"connected","openai_configured":true}
```

Then visit your frontend URL and send a test message!

---

## 🐛 Troubleshooting

**Not logged in?**
```bash
vercel login
```

**Script fails?**
- Use Method 1 (Dashboard) instead
- Or follow manual steps above

**Environment variables not working?**
- Make sure to redeploy after adding variables
- Check variable names are exact (case-sensitive)
- Frontend variables must start with `NEXT_PUBLIC_`

**Need help?**
- See [DEPLOY_STEP_BY_STEP.md](./DEPLOY_STEP_BY_STEP.md) for detailed guide
- Check Vercel dashboard logs for errors

---

## 🎉 Success!

Once deployed, you'll have:
- ✅ Live chatbot at frontend URL
- ✅ API at backend URL  
- ✅ API docs at `/docs`
- ✅ Health check at `/api/health`

**Share your chatbot URL with the world!** 🌟
