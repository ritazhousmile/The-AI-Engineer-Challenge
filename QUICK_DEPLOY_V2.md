# ⚡ Quick Deploy Guide - 5 Minutes

Fastest way to deploy your Mental Coach AI chatbot with all new features!

## 🚀 Step-by-Step (Copy & Paste Ready)

### 1️⃣ Deploy Backend (2 minutes)

1. **Go to:** https://vercel.com/new
2. **Import:** Your GitHub repo (`ritazhousmile/The-AI-Engineer-Challenge`)
3. **Settings:**
   - Project Name: `mental-coach-api`
   - Framework: **Other**
   - Root Directory: (leave empty)
   - Build Command: (leave empty)
   - Output Directory: (leave empty)

4. **Environment Variables** (Click "Environment Variables" → Add each):

```
OPENAI_API_KEY = sk-proj-your-key-here
DB_PATH = /tmp/conversations.db
RATE_LIMIT_ENABLED = true
RATE_LIMIT_REQUESTS = 60
RATE_LIMIT_WINDOW = 60
ALLOWED_ORIGINS = *
```

5. **Click "Deploy"** → Wait 1-2 minutes
6. **Copy Backend URL:** `https://mental-coach-api-xyz.vercel.app`

---

### 2️⃣ Deploy Frontend (2 minutes)

1. **Go to:** https://vercel.com/new (again)
2. **Import:** Same repo
3. **Settings:**
   - Project Name: `mental-coach-frontend`
   - Framework: **Next.js** (auto-detected)
   - Root Directory: `frontend`
   - Build Command: `npm run build` (default)
   - Output Directory: `.next` (default)

4. **Environment Variable:**

```
NEXT_PUBLIC_API_URL = https://mental-coach-api-xyz.vercel.app
```
*(Use your actual backend URL from step 1)*

5. **Click "Deploy"** → Wait 2-3 minutes
6. **Copy Frontend URL:** `https://mental-coach-frontend-xyz.vercel.app`

---

### 3️⃣ Test (1 minute)

**Test Backend:**
```bash
curl https://your-backend-url.vercel.app/api/health
```

Should return:
```json
{
  "status": "ok",
  "version": "2.0.0",
  "database": "connected",
  "openai_configured": true
}
```

**Test Frontend:**
- Visit your frontend URL
- Send a message
- Verify it works! 🎉

---

## ✅ That's It!

Your chatbot is now live! 

**Your URLs:**
- Frontend: `https://mental-coach-frontend-xyz.vercel.app`
- Backend: `https://mental-coach-api-xyz.vercel.app`
- API Docs: `https://mental-coach-api-xyz.vercel.app/docs`

---

## 🔒 Optional: Add Security

For production, add to backend environment variables:

```
API_KEY = your-secure-random-key-here
ALLOWED_ORIGINS = https://your-frontend-url.vercel.app
```

Generate API key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 🐛 Quick Troubleshooting

**Backend not working?**
- Check OpenAI API key is correct
- Check function logs in Vercel dashboard

**Frontend can't connect?**
- Verify `NEXT_PUBLIC_API_URL` matches backend URL exactly
- Check no trailing slash in URL
- Check browser console for errors

**Database errors?**
- Make sure `DB_PATH = /tmp/conversations.db` for Vercel

---

## 📚 Need More Details?

- Full guide: [DEPLOYMENT_V2.md](./DEPLOYMENT_V2.md)
- Checklist: [DEPLOY_CHECKLIST.md](./DEPLOY_CHECKLIST.md)
- Troubleshooting: [TROUBLESHOOTING_DEPLOYMENT.md](./TROUBLESHOOTING_DEPLOYMENT.md)

---

**🎉 Happy Deploying!**
