# 🚀 Deploy Your App NOW - Step by Step

Your code is on GitHub! Now let's deploy it via the Vercel Dashboard.

## 📦 Part 1: Deploy the Frontend

### Step 1: Go to Vercel

Open this link in your browser:
**https://vercel.com/new**

### Step 2: Import Your Repository

1. You'll see "Import Git Repository"
2. Find and select: **`ritazhousmile/The-AI-Engineer-Challenge`**
3. Click **"Import"**

### Step 3: Configure Frontend Settings

You'll see a configuration screen. Set these:

- **Project Name:** `mental-coach-frontend` (or any name you like)
- **Framework Preset:** Next.js (should auto-detect)
- **Root Directory:** Click **"Edit"** → Enter: `frontend`
- **Build Command:** `npm run build` (default, leave it)
- **Output Directory:** `.next` (default, leave it)
- **Install Command:** `npm install` (default, leave it)

### Step 4: Leave Environment Variables Empty (for now)

We'll add them after deployment.

### Step 5: Click "Deploy"!

Wait 2-3 minutes. You'll see a success screen with confetti! 🎉

**Copy your frontend URL!** It will look like:
```
https://mental-coach-frontend-xyz.vercel.app
```

---

## 🔧 Part 2: Deploy the Backend

### Step 1: Go to Vercel Again

Open: **https://vercel.com/new**

### Step 2: Import Same Repository

1. Select: **`ritazhousmile/The-AI-Engineer-Challenge`** again
2. Click **"Import"**

### Step 3: Configure Backend Settings

- **Project Name:** `mental-coach-api`
- **Framework Preset:** Other
- **Root Directory:** Leave empty (use root directory)
- **Build Command:** Leave empty
- **Output Directory:** Leave empty

### Step 4: Add Environment Variable

**IMPORTANT:** Before deploying, add your API key:

1. Scroll down to **"Environment Variables"**
2. Click **"Add"** or the + button
3. Fill in:
   - **Name:** `OPENAI_API_KEY`
   - **Value:** Paste your OpenAI API key (the one starting with sk-proj...)
   - **Environment:** Select all (Production, Preview, Development)
4. Click **"Add"**

### Step 5: Click "Deploy"!

Wait 1-2 minutes for deployment.

**Copy your backend URL!** It will look like:
```
https://mental-coach-api-xyz.vercel.app
```

---

## 🔗 Part 3: Connect Frontend to Backend

### Step 1: Go to Your Frontend Project

1. Go to: https://vercel.com/dashboard
2. Click on your **`mental-coach-frontend`** project

### Step 2: Add Backend URL

1. Go to **"Settings"** tab
2. Click **"Environment Variables"** in the left sidebar
3. Click **"Add New"**
4. Fill in:
   - **Name:** `NEXT_PUBLIC_API_URL`
   - **Value:** Your backend URL (e.g., `https://mental-coach-api-xyz.vercel.app`)
   - **Environment:** Select all (Production, Preview, Development)
5. Click **"Save"**

### Step 3: Redeploy Frontend

1. Go to **"Deployments"** tab
2. Find the latest deployment (top of the list)
3. Click the **"..."** menu button
4. Click **"Redeploy"**
5. Confirm by clicking **"Redeploy"**

Wait 1-2 minutes...

---

## ✅ Part 4: Test Your App!

### Visit Your Frontend URL

Go to your frontend URL:
```
https://mental-coach-frontend-xyz.vercel.app
```

### Test the Chat

1. You should see the beautiful Mental Coach AI interface
2. Try sending a message: "Hello, how are you?"
3. Watch the response stream in real-time with markdown formatting!

---

## 🎯 Quick Checklist

- [ ] Frontend deployed to Vercel
- [ ] Backend deployed to Vercel  
- [ ] `OPENAI_API_KEY` added to backend
- [ ] `NEXT_PUBLIC_API_URL` added to frontend
- [ ] Frontend redeployed after adding environment variable
- [ ] Tested the app and it works!

---

## 📝 Your Deployment URLs

**Frontend:** https://mental-coach-frontend-xyz.vercel.app  
**Backend:** https://mental-coach-api-xyz.vercel.app

**Share your frontend URL with the world!** 🌟

Post on LinkedIn, tag @AIMakerspace, and celebrate! 🎉

---

## 🐛 If Something Goes Wrong

### Frontend shows error page:
- Check that `NEXT_PUBLIC_API_URL` is set correctly
- Make sure it doesn't have a trailing slash
- Redeploy after adding the environment variable

### Backend API not responding:
- Verify `OPENAI_API_KEY` is set in backend environment variables
- Check the Function Logs in Vercel dashboard
- Make sure the key is valid

### CORS errors:
- Already configured! Should work automatically

### Still stuck?
- Check the build logs in Vercel dashboard
- Look for error messages
- The logs will tell you exactly what went wrong

---

## 🎉 Success!

Once everything is deployed and working:

1. Take a screenshot
2. Post on LinkedIn
3. Tag @AIMakerspace
4. Share your deployed URL
5. Add it to your portfolio!

**You just built and deployed your first AI-powered application with streaming and markdown support!** 🚀✨

Congratulations! 🎊

