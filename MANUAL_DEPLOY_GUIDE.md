# 🎯 Manual Deployment Guide - Do This Yourself

Your code is ready on GitHub! Now **YOU** need to deploy it through the Vercel Dashboard. I can't access your Vercel account, so follow these exact steps:

---

## 🚀 Step-by-Step Deployment

### **Part 1: Deploy the Frontend**

#### Step 1: Open Vercel in Your Browser

1. Open your web browser
2. Go to: **https://vercel.com/new**
3. Make sure you're logged in to Vercel

#### Step 2: Import Your GitHub Repository

You'll see a page that says "Import Git Repository"

1. Look for your repository in the list: **`ritazhousmile/The-AI-Engineer-Challenge`**
   - If you don't see it, click "Add GitHub Account" or "Import Git Repository"
   - Connect your GitHub account if needed
2. Once you see your repository, click the **"Import"** button next to it

#### Step 3: Configure the Frontend

You'll now see a configuration screen. Fill it out like this:

**Project Settings:**
- **Project Name:** Type `mental-coach-frontend` (or any name you prefer)
- **Framework Preset:** Should say "Next.js" automatically
- **Root Directory:** 
  - Click the **"Edit"** button 
  - Type: `frontend`
  - Click "Continue" or "Save"
- **Build Command:** Leave as `npm run build`
- **Output Directory:** Leave as `.next`
- **Install Command:** Leave as `npm install`

**Environment Variables:**
- Skip this for now (we'll add it later)

#### Step 4: Click "Deploy"

1. Scroll down to the bottom
2. Click the big blue **"Deploy"** button
3. Wait 2-3 minutes while it builds

You'll see:
- "Building..." with a progress indicator
- Logs scrolling by
- Finally: "Your project is ready!" with confetti 🎉

#### Step 5: Copy Your Frontend URL

After deployment succeeds:
- You'll see a preview image of your site
- Below it, there's a URL like: `https://mental-coach-frontend-abc123.vercel.app`
- **COPY THIS URL** - write it down somewhere!

---

### **Part 2: Deploy the Backend**

#### Step 1: Go Back to Import Page

1. Go to: **https://vercel.com/new**
2. You'll see the import page again

#### Step 2: Import Same Repository Again

1. Find **`ritazhousmile/The-AI-Engineer-Challenge`** in the list
2. Click **"Import"** again (yes, same repo!)

#### Step 3: Configure the Backend

**Project Settings:**
- **Project Name:** Type `mental-coach-api`
- **Framework Preset:** Select "Other"
- **Root Directory:** Leave this EMPTY (don't change it)
- **Build Command:** Leave empty
- **Output Directory:** Leave empty

**Environment Variables (IMPORTANT!):**
- Scroll down to "Environment Variables" section
- Click **"Add New"** or the **+** button
- Fill in:
  - **KEY:** `OPENAI_API_KEY`
  - **VALUE:** Paste your OpenAI API key here (starts with sk-proj...)
  - **ENVIRONMENTS:** Make sure all three are checked (Production, Preview, Development)
- Click **"Add"**

#### Step 4: Click "Deploy"

1. Scroll down
2. Click **"Deploy"** button
3. Wait 1-2 minutes

#### Step 5: Copy Your Backend URL

After deployment:
- You'll see success screen
- Copy the URL like: `https://mental-coach-api-xyz789.vercel.app`
- **WRITE THIS DOWN TOO!**

---

### **Part 3: Connect Frontend to Backend**

#### Step 1: Go to Your Dashboard

1. Go to: **https://vercel.com/dashboard**
2. You should now see TWO projects:
   - `mental-coach-frontend`
   - `mental-coach-api`

#### Step 2: Configure Frontend Environment Variable

1. Click on **`mental-coach-frontend`** project
2. Click the **"Settings"** tab at the top
3. In the left sidebar, click **"Environment Variables"**
4. Click **"Add New"** button
5. Fill in:
   - **KEY:** `NEXT_PUBLIC_API_URL`
   - **VALUE:** Paste your backend URL here (the one you copied in Part 2, Step 5)
   - Make sure there's NO trailing slash at the end
   - Example: `https://mental-coach-api-xyz789.vercel.app` ✅
   - NOT: `https://mental-coach-api-xyz789.vercel.app/` ❌
   - **ENVIRONMENTS:** Check all three boxes
6. Click **"Save"**

#### Step 3: Redeploy Frontend

1. Click the **"Deployments"** tab at the top
2. You'll see your deployment listed (most recent at top)
3. On the right side, click the **three dots (...)** button
4. Click **"Redeploy"**
5. A popup appears, click **"Redeploy"** again to confirm
6. Wait 1-2 minutes for redeployment

---

### **Part 4: Test Your App!**

#### Visit Your Frontend

1. Go to your frontend URL (from Part 1, Step 5)
2. You should see your beautiful Mental Coach AI interface!

#### Test the Chat

1. Type a message like: "Hello, I'm feeling stressed"
2. Click Send or press Enter
3. Watch the AI response stream in with markdown formatting!

---

## ✅ Verification Checklist

Check off each item:

- [ ] Opened https://vercel.com/new in my browser
- [ ] Imported repository for frontend
- [ ] Set Root Directory to `frontend`
- [ ] Deployed frontend successfully
- [ ] Copied frontend URL
- [ ] Imported repository for backend
- [ ] Added `OPENAI_API_KEY` environment variable to backend
- [ ] Deployed backend successfully
- [ ] Copied backend URL
- [ ] Added `NEXT_PUBLIC_API_URL` to frontend settings
- [ ] Redeployed frontend
- [ ] Tested the chat and it works!

---

## 📝 Your URLs

Write them down here after deployment:

**Frontend URL:** _________________________________

**Backend URL:** _________________________________

---

## 🐛 Troubleshooting

### "I don't see my repository"

- Make sure you're logged into Vercel
- Click "Add GitHub Account" to connect
- Authorize Vercel to access your repositories

### "Build failed"

- Check the build logs in Vercel dashboard
- Most common issue: Root Directory not set correctly for frontend
- Frontend should have Root Directory = `frontend`
- Backend should have Root Directory = empty

### "Frontend loads but chat doesn't work"

- Make sure you added `NEXT_PUBLIC_API_URL` to frontend
- Make sure you redeployed frontend after adding the variable
- Check that backend URL has no trailing slash

### "Backend deployment failed"

- Make sure `OPENAI_API_KEY` is set correctly
- Check that your API key is valid
- Look at the Function Logs in Vercel dashboard

---

## 🎉 Success!

Once it's working:

1. ✅ Share your frontend URL
2. ✅ Test the chat with friends
3. ✅ Post on LinkedIn
4. ✅ Tag @AIMakerspace
5. ✅ Add to your portfolio!

---

**You got this!** 💪 Follow the steps carefully and let me know if you get stuck on any specific step!

