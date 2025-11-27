# 🚀 Quick Deployment Steps

You're logged into Vercel! Now follow these steps to deploy your app.

## ✨ Option 1: Deploy via Vercel Dashboard (Easiest!)

This is the **recommended approach** for first-time deployment.

### Step 1: Push to GitHub (if not already done)

Open a terminal and run:

```bash
cd /Users/zhouhuan/ai-bootcamp-challenge/The-AI-Engineer-Challenge
git add .
git commit -m "Add Mental Coach AI with streaming and markdown support"
git push origin main
```

### Step 2: Deploy Frontend via Vercel Dashboard

1. Go to: **https://vercel.com/new**
2. Click **"Import Git Repository"**
3. Select your repository: `ai-bootcamp-challenge` or `The-AI-Engineer-Challenge`
4. Configure the project:
   - **Project Name:** `mental-coach-frontend` (or any name you like)
   - **Root Directory:** Click **"Edit"** and set to: `The-AI-Engineer-Challenge/frontend`
   - **Framework Preset:** Next.js (should auto-detect)
   - **Build Command:** `npm run build` (default)
   - **Output Directory:** `.next` (default)
5. Click **"Deploy"**

Wait for the build to complete (2-3 minutes). You'll get a URL like:
```
https://mental-coach-frontend.vercel.app
```

### Step 3: Deploy Backend via Vercel Dashboard

1. Go to: **https://vercel.com/new** again
2. Select the **same repository**
3. Configure the project:
   - **Project Name:** `mental-coach-api`
   - **Root Directory:** Click **"Edit"** and set to: `The-AI-Engineer-Challenge`
   - **Framework Preset:** Other
4. Before deploying, add environment variable:
   - Click **"Environment Variables"**
   - Name: `OPENAI_API_KEY`
   - Value: `your-openai-api-key-here`
   - Click **"Add"**
5. Click **"Deploy"**

You'll get a backend URL like:
```
https://mental-coach-api.vercel.app
```

### Step 4: Connect Frontend to Backend

1. Go to your **frontend project** in Vercel dashboard
2. Click **"Settings"** → **"Environment Variables"**
3. Add a new variable:
   - Name: `NEXT_PUBLIC_API_URL`
   - Value: Your backend URL (e.g., `https://mental-coach-api.vercel.app`)
   - Select all environments (Production, Preview, Development)
4. Click **"Save"**
5. Go to **"Deployments"** tab
6. Click the **"..."** menu on the latest deployment → **"Redeploy"**

### Step 5: Test Your App! 🎉

Visit your frontend URL and test the chat! It should now work with streaming and markdown formatting.

---

## 💻 Option 2: Deploy via CLI (Alternative)

If you prefer the command line:

### Step 1: Deploy Frontend

Open a **new terminal** (not in Cursor) and run:

```bash
cd /Users/zhouhuan/ai-bootcamp-challenge/The-AI-Engineer-Challenge/frontend
vercel login
vercel --prod
```

Follow the prompts:
- Set up and deploy? **Y**
- Which scope? Select your account
- Link to existing project? **N**
- Project name? `mental-coach-frontend`
- Override settings? **N**

### Step 2: Deploy Backend

In the same terminal:

```bash
cd /Users/zhouhuan/ai-bootcamp-challenge/The-AI-Engineer-Challenge
vercel --prod
```

Follow the prompts:
- Set up and deploy? **Y**
- Project name? `mental-coach-api`
- Override settings? **N**

### Step 3: Add Environment Variables

**For Backend:**
```bash
cd /Users/zhouhuan/ai-bootcamp-challenge/The-AI-Engineer-Challenge
vercel env add OPENAI_API_KEY production
# Paste your API key when prompted
vercel --prod  # Redeploy to apply
```

**For Frontend:**
```bash
cd /Users/zhouhuan/ai-bootcamp-challenge/The-AI-Engineer-Challenge/frontend
vercel env add NEXT_PUBLIC_API_URL production
# Paste your backend URL when prompted
vercel --prod  # Redeploy to apply
```

---

## 🎯 Quick Checklist

- [ ] Code pushed to GitHub
- [ ] Frontend deployed to Vercel
- [ ] Backend deployed to Vercel
- [ ] `OPENAI_API_KEY` added to backend environment variables
- [ ] `NEXT_PUBLIC_API_URL` added to frontend environment variables
- [ ] Frontend redeployed after adding environment variable
- [ ] Tested the deployed app

---

## 🐛 Troubleshooting

**Build fails?**
- Check the build logs in Vercel dashboard
- Make sure the root directory is set correctly

**API not working?**
- Verify environment variables are set
- Check that backend URL doesn't have trailing slash
- Look at Function Logs in Vercel dashboard

**CORS errors?**
- Already configured! Should work out of the box

---

## 📝 Your URLs

After deployment, save these URLs:

**Frontend:** https://your-frontend.vercel.app
**Backend:** https://your-backend.vercel.app

Share your frontend URL with the world! 🌟

---

**Pro Tip:** With GitHub integration, every time you push code, Vercel automatically redeploys! 🔄

