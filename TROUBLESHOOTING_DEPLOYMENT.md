# 🔧 Troubleshooting Deployment - 404 Error

## What's Happening

You're seeing a `404: DEPLOYMENT_NOT_FOUND` error. This typically means one of these things:

1. **Backend is deployed but frontend URL is wrong**
2. **Frontend needs the correct backend URL**
3. **Deployment configuration needs adjustment**

## 🎯 Quick Fix Steps

### Step 1: Check Which Deployment Has the Issue

**Is it the backend or frontend that's showing 404?**

#### If BACKEND shows 404:

The backend should respond at the root URL. Let's redeploy it:

```bash
cd /Users/zhouhuan/ai-bootcamp-challenge/The-AI-Engineer-Challenge
vercel --prod --yes
```

After deployment, test it:
```bash
curl https://your-backend-url.vercel.app/
```

You should see:
```json
{
  "status": "ok",
  "message": "Mental Coach API is running!"
}
```

#### If FRONTEND shows 404:

The frontend might need redeployment:

```bash
cd /Users/zhouhuan/ai-bootcamp-challenge/The-AI-Engineer-Challenge/frontend
vercel --prod --yes
```

---

## 🚀 Clean Deployment from Scratch

Let's do a fresh deployment to ensure everything works:

### 1. Deploy Backend First

```bash
cd /Users/zhouhuan/ai-bootcamp-challenge/The-AI-Engineer-Challenge
vercel --prod --yes
```

**Save the backend URL** you get (e.g., `https://mental-coach-api-abc.vercel.app`)

### 2. Add Backend Environment Variable

```bash
vercel env add OPENAI_API_KEY production
```

Paste your API key when prompted:
```
your-openai-api-key-here
```

Then redeploy to apply:
```bash
vercel --prod --yes
```

### 3. Test Backend

```bash
curl https://your-backend-url.vercel.app/
```

### 4. Deploy Frontend with Backend URL

```bash
cd frontend
vercel env add NEXT_PUBLIC_API_URL production
```

Paste your backend URL (NO trailing slash):
```
https://your-backend-url.vercel.app
```

Deploy:
```bash
vercel --prod --yes
```

---

## 🔍 Verify Deployments

### Check Backend:

```bash
# Test root
curl https://your-backend-url.vercel.app/

# Test API endpoint
curl https://your-backend-url.vercel.app/api

# Test health (should work)
curl -X POST https://your-backend-url.vercel.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

### Check Frontend:

Visit `https://your-frontend-url.vercel.app` in your browser

---

## 🎯 Alternative: Deploy via Vercel Dashboard

If CLI keeps having issues, use the dashboard:

### Backend Deployment:

1. Go to: https://vercel.com/new
2. Select "Import Git Repository"
3. Choose your repository
4. Settings:
   - **Root Directory:** `The-AI-Engineer-Challenge` 
   - **Framework Preset:** Other
   - **Build Command:** Leave empty
   - **Output Directory:** Leave empty
5. Environment Variables:
   - Add `OPENAI_API_KEY` with your key
6. Click Deploy

### Frontend Deployment:

1. Go to: https://vercel.com/new
2. Select same repository
3. Settings:
   - **Root Directory:** `The-AI-Engineer-Challenge/frontend`
   - **Framework Preset:** Next.js (auto-detected)
4. Environment Variables:
   - Add `NEXT_PUBLIC_API_URL` with your backend URL
5. Click Deploy

---

## 📋 What URLs Do You Have?

Please provide:
1. **Backend URL:** ___________________
2. **Frontend URL:** ___________________
3. **Which one shows 404?** ___________________

This will help me diagnose the exact issue!

---

## 🆘 Common Issues

### Issue: "DEPLOYMENT_NOT_FOUND"
**Fix:** The URL might be wrong or deployment failed. Check Vercel dashboard for the correct URL.

### Issue: Backend works but frontend can't connect
**Fix:** Make sure `NEXT_PUBLIC_API_URL` is set in frontend environment variables and redeploy.

### Issue: CORS errors
**Fix:** Already configured! Should work out of the box.

### Issue: API key not working
**Fix:** 
```bash
cd /Users/zhouhuan/ai-bootcamp-challenge/The-AI-Engineer-Challenge
vercel env rm OPENAI_API_KEY production
vercel env add OPENAI_API_KEY production
# Paste key again
vercel --prod --yes
```

---

## 💡 Next Steps

Tell me:
1. Which URL is showing the 404 error?
2. Have you deployed both frontend and backend?
3. What's your backend URL?

I'll help you fix it! 🚀

