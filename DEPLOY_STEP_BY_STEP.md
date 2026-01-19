# 🚀 Step-by-Step Deployment Guide

Follow these steps exactly to deploy your Mental Coach AI chatbot.

## 📋 Before You Start

### Prerequisites Checklist
- [ ] GitHub account
- [ ] Code pushed to GitHub (if not, run: `git push origin main`)
- [ ] Vercel account (sign up at https://vercel.com - it's free)
- [ ] OpenAI API key (get it from https://platform.openai.com/api-keys)

---

## 🎯 Step 1: Push Code to GitHub (if needed)

If you haven't pushed your latest changes:

```bash
git push origin main
```

If you get authentication errors, you may need to:
- Use a personal access token
- Or push manually through GitHub Desktop/GitHub website

---

## 🔧 Step 2: Deploy Backend API

### 2.1 Go to Vercel

1. Open: **https://vercel.com/new**
2. Sign in with GitHub (if not already signed in)

### 2.2 Import Repository

1. Click **"Import Git Repository"**
2. Find and select: **`ritazhousmile/The-AI-Engineer-Challenge`**
3. Click **"Import"**

### 2.3 Configure Project Settings

Fill in these settings:

- **Project Name:** `mental-coach-api`
- **Framework Preset:** Click dropdown → Select **"Other"**
- **Root Directory:** Leave empty (use root)
- **Build Command:** Leave empty
- **Output Directory:** Leave empty

### 2.4 Add Environment Variables

**IMPORTANT:** Click **"Environment Variables"** section and add these one by one:

| Variable Name | Value | Environment |
|--------------|-------|------------|
| `OPENAI_API_KEY` | `sk-proj-...` (your OpenAI key) | Production, Preview, Development |
| `DB_PATH` | `/tmp/conversations.db` | Production, Preview, Development |
| `RATE_LIMIT_ENABLED` | `true` | Production, Preview, Development |
| `RATE_LIMIT_REQUESTS` | `60` | Production, Preview, Development |
| `RATE_LIMIT_WINDOW` | `60` | Production, Preview, Development |
| `ALLOWED_ORIGINS` | `*` | Production, Preview, Development |

**How to add:**
1. Click **"Add"** or **"+"** button
2. Enter Variable Name
3. Enter Value
4. Check all three environments (Production, Preview, Development)
5. Click **"Add"**
6. Repeat for each variable

### 2.5 Deploy

1. Scroll down and click **"Deploy"**
2. Wait 1-2 minutes for deployment
3. You'll see a success screen! 🎉

### 2.6 Copy Backend URL

After deployment succeeds:
1. You'll see your deployment URL
2. Copy it! It looks like: `https://mental-coach-api-xyz.vercel.app`
3. **Save this URL** - you'll need it for the frontend

---

## 🎨 Step 3: Deploy Frontend

### 3.1 Go to Vercel Again

1. Open: **https://vercel.com/new** (in a new tab or go back)
2. You'll import the same repository again

### 3.2 Import Repository (Again)

1. Click **"Import Git Repository"**
2. Find and select: **`ritazhousmile/The-AI-Engineer-Challenge`** (same repo)
3. Click **"Import"**

### 3.3 Configure Project Settings

Fill in these settings:

- **Project Name:** `mental-coach-frontend`
- **Framework Preset:** Should auto-detect **"Next.js"** (if not, select it)
- **Root Directory:** Click **"Edit"** → Enter: `frontend`
- **Build Command:** `npm run build` (should be default)
- **Output Directory:** `.next` (should be default)

### 3.4 Add Environment Variable

Click **"Environment Variables"** and add:

| Variable Name | Value | Environment |
|--------------|-------|------------|
| `NEXT_PUBLIC_API_URL` | `https://mental-coach-api-xyz.vercel.app` | Production, Preview, Development |

**Important:** 
- Use your **actual backend URL** from Step 2.6
- **No trailing slash** at the end
- Example: `https://mental-coach-api-xyz.vercel.app` ✅
- Wrong: `https://mental-coach-api-xyz.vercel.app/` ❌

### 3.5 Deploy

1. Click **"Deploy"**
2. Wait 2-3 minutes for deployment
3. Success! 🎉

### 3.6 Copy Frontend URL

After deployment:
1. Copy your frontend URL
2. It looks like: `https://mental-coach-frontend-xyz.vercel.app`
3. **This is your live chatbot!**

---

## ✅ Step 4: Test Your Deployment

### 4.1 Test Backend

Open a terminal and run:

```bash
curl https://your-backend-url.vercel.app/api/health
```

**Expected response:**
```json
{
  "status": "ok",
  "version": "2.0.0",
  "database": "connected",
  "openai_configured": true
}
```

If you see this, backend is working! ✅

### 4.2 Test Frontend

1. Open your frontend URL in a browser
2. You should see the Mental Coach AI interface
3. Type a message: "Hello!"
4. You should see a streaming response
5. Try sending multiple messages to test conversation history

If it works, you're done! 🎉

---

## 🔒 Step 5: Optional - Add Security (Recommended for Production)

### 5.1 Generate API Key

Run this command to generate a secure API key:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Or use this online tool: https://randomkeygen.com/

### 5.2 Add to Backend

1. Go to Vercel Dashboard
2. Click on your **`mental-coach-api`** project
3. Go to **Settings** → **Environment Variables**
4. Add:
   - **Name:** `API_KEY`
   - **Value:** (paste your generated key)
   - **Environments:** All
5. Click **"Save"**
6. Go to **Deployments** tab
7. Click **"..."** on latest deployment → **"Redeploy"**

### 5.3 Update CORS (Optional)

1. In backend environment variables
2. Update `ALLOWED_ORIGINS`:
   - Change from `*` to your frontend URL
   - Example: `https://mental-coach-frontend-xyz.vercel.app`
3. Redeploy backend

---

## 🐛 Troubleshooting

### Backend Issues

**Problem:** Deployment fails
- **Solution:** Check build logs in Vercel dashboard for errors

**Problem:** Health check returns error
- **Solution:** 
  - Check `OPENAI_API_KEY` is correct
  - Check function logs in Vercel dashboard
  - Verify environment variables are set

**Problem:** Database errors
- **Solution:** Make sure `DB_PATH = /tmp/conversations.db`

### Frontend Issues

**Problem:** Can't connect to backend
- **Solution:**
  - Verify `NEXT_PUBLIC_API_URL` matches backend URL exactly
  - No trailing slash
  - Check browser console for CORS errors
  - Verify backend is deployed and working

**Problem:** Build fails
- **Solution:**
  - Check Node.js version (should be 18+)
  - Check build logs in Vercel
  - Verify `frontend/package.json` exists

**Problem:** Environment variable not working
- **Solution:**
  - Must start with `NEXT_PUBLIC_` for client-side access
  - Redeploy after adding variables

### General Issues

**Problem:** Changes not showing
- **Solution:**
  - Push code to GitHub
  - Vercel auto-deploys on push
  - Or manually redeploy in Vercel dashboard

**Problem:** API returns 500 errors
- **Solution:**
  - Check function logs in Vercel
  - Verify OpenAI API key is valid
  - Check OpenAI account has credits

---

## 📊 Your Deployment URLs

After successful deployment, you'll have:

- **Frontend:** `https://mental-coach-frontend-xyz.vercel.app`
- **Backend API:** `https://mental-coach-api-xyz.vercel.app`
- **API Documentation:** `https://mental-coach-api-xyz.vercel.app/docs`
- **Health Check:** `https://mental-coach-api-xyz.vercel.app/api/health`

---

## 🎉 Success Checklist

- [ ] Backend deployed successfully
- [ ] Frontend deployed successfully
- [ ] Backend health check passes
- [ ] Frontend loads correctly
- [ ] Can send messages
- [ ] Streaming responses work
- [ ] Conversation history works (multiple messages)
- [ ] No errors in browser console
- [ ] No errors in Vercel logs

---

## 📚 Next Steps

1. **Share your chatbot:**
   - Share the frontend URL with others
   - Test in incognito mode
   - Test on mobile device

2. **Set up integrations:**
   - Deploy Slack bot (see `integrations/slack_setup.md`)
   - Deploy Discord bot (see `integrations/discord_setup.md`)
   - Embed React widget (see `integrations/react_widget/README.md`)

3. **Monitor:**
   - Check Vercel analytics
   - Monitor API usage
   - Set up error tracking (optional)

4. **Improve:**
   - Add persistent database (Supabase, Vercel Postgres)
   - Set up custom domain
   - Add analytics
   - Optimize performance

---

## 💡 Pro Tips

1. **Keep your URLs safe:**
   - Save them in a document
   - Don't share API keys publicly

2. **Monitor usage:**
   - Check Vercel dashboard regularly
   - Monitor OpenAI API usage
   - Set up alerts if needed

3. **Update easily:**
   - Just push to GitHub
   - Vercel auto-deploys
   - No manual steps needed

---

**🎊 Congratulations! Your Mental Coach AI chatbot is now live!**

Need help? Check:
- [Quick Deploy Guide](./QUICK_DEPLOY_V2.md)
- [Complete Deployment Guide](./DEPLOYMENT_V2.md)
- [Deployment Checklist](./DEPLOY_CHECKLIST.md)
