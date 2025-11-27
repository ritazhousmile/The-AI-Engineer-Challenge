# 🚀 Deployment Guide - Mental Coach AI

This guide will walk you through deploying your Mental Coach AI application to Vercel.

## 📋 Prerequisites

- [x] GitHub account (for connecting to Vercel)
- [x] Vercel account (sign up at [vercel.com](https://vercel.com))
- [x] OpenAI API key
- [x] Working local application

## 🎯 Deployment Strategy

We'll deploy in two parts:
1. **Backend API** - FastAPI Python backend
2. **Frontend** - Next.js React application

Both will be deployed to Vercel, and we'll connect them together.

---

## 📦 Part 1: Deploy the Backend API

### Step 1: Navigate to the project root

```bash
cd /Users/zhouhuan/ai-bootcamp-challenge/The-AI-Engineer-Challenge
```

### Step 2: Install Vercel CLI (if not already installed)

```bash
npm install -g vercel
```

### Step 3: Login to Vercel

```bash
vercel login
```

Follow the prompts to authenticate with your Vercel account.

### Step 4: Deploy the Backend

```bash
vercel --prod
```

**Follow the prompts:**
- Set up and deploy? **Y**
- Which scope? Choose your account
- Link to existing project? **N**
- Project name? `mental-coach-api` (or your choice)
- Directory? Press Enter (use current directory)
- Override settings? **N**

### Step 5: Add Environment Variable

After deployment, you need to add your OpenAI API key:

1. Go to your Vercel dashboard: https://vercel.com/dashboard
2. Find your `mental-coach-api` project
3. Go to **Settings** → **Environment Variables**
4. Add a new variable:
   - **Name:** `OPENAI_API_KEY`
   - **Value:** Your OpenAI API key
   - **Environments:** Production, Preview, Development (select all)
5. Click **Save**
6. Redeploy: `vercel --prod` (to apply the environment variable)

### Step 6: Note Your Backend URL

After deployment, you'll see a URL like:
```
https://mental-coach-api.vercel.app
```

**Save this URL!** You'll need it for the frontend.

---

## 🎨 Part 2: Deploy the Frontend

### Step 1: Navigate to the frontend directory

```bash
cd /Users/zhouhuan/ai-bootcamp-challenge/The-AI-Engineer-Challenge/frontend
```

### Step 2: Deploy the Frontend

```bash
vercel --prod
```

**Follow the prompts:**
- Set up and deploy? **Y**
- Which scope? Choose your account
- Link to existing project? **N**
- Project name? `mental-coach-frontend` (or your choice)
- Directory? Press Enter (use current directory)
- Override settings? **N**

### Step 3: Add Environment Variable for Backend URL

After deployment:

1. Go to your Vercel dashboard
2. Find your `mental-coach-frontend` project
3. Go to **Settings** → **Environment Variables**
4. Add a new variable:
   - **Name:** `NEXT_PUBLIC_API_URL`
   - **Value:** Your backend URL (e.g., `https://mental-coach-api.vercel.app`)
   - **Environments:** Production, Preview, Development (select all)
5. Click **Save**
6. Redeploy: `vercel --prod` (to apply the environment variable)

### Step 4: Test Your Deployed Application

After deployment, you'll get a URL like:
```
https://mental-coach-frontend.vercel.app
```

Visit this URL in your browser and test the chat functionality!

---

## 🔧 Alternative: Deploy via GitHub (Recommended for Continuous Deployment)

This method allows automatic deployments when you push to GitHub.

### Step 1: Push to GitHub

If you haven't already, push your code to GitHub:

```bash
cd /Users/zhouhuan/ai-bootcamp-challenge/The-AI-Engineer-Challenge
git add .
git commit -m "Add frontend and backend with streaming support"
git push origin main
```

### Step 2: Connect to Vercel

1. Go to [vercel.com/new](https://vercel.com/new)
2. Click **Import Git Repository**
3. Select your GitHub repository
4. Configure the backend:
   - **Project Name:** `mental-coach-api`
   - **Root Directory:** Leave empty (use root)
   - **Framework Preset:** Other
   - Add environment variable: `OPENAI_API_KEY`
5. Click **Deploy**

### Step 3: Deploy Frontend

1. Go to [vercel.com/new](https://vercel.com/new) again
2. Select the same repository
3. Configure the frontend:
   - **Project Name:** `mental-coach-frontend`
   - **Root Directory:** `frontend`
   - **Framework Preset:** Next.js (auto-detected)
   - Add environment variable: `NEXT_PUBLIC_API_URL` (use your backend URL)
4. Click **Deploy**

---

## ✅ Verification Checklist

After deployment, verify:

- [ ] Backend API is accessible at your Vercel URL
- [ ] Frontend loads without errors
- [ ] Chat functionality works (send a test message)
- [ ] Streaming responses appear in real-time
- [ ] Markdown formatting displays correctly
- [ ] No CORS errors in browser console

---

## 🐛 Troubleshooting

### CORS Errors

If you see CORS errors:
1. Make sure your backend has CORS middleware configured (already done)
2. Verify the `NEXT_PUBLIC_API_URL` is set correctly in frontend

### API Key Not Working

1. Double-check the environment variable name: `OPENAI_API_KEY`
2. Verify it's set for all environments (Production, Preview, Development)
3. Redeploy after adding environment variables

### Streaming Not Working

If streaming doesn't work in production:
1. Check browser console for errors
2. Verify the backend `/api/chat` endpoint is accessible
3. Test the backend directly: `https://your-backend.vercel.app/`

### Build Failures

Frontend build issues:
```bash
# Test locally first
cd frontend
npm run build
```

Backend issues:
- Check that `requirements.txt` includes all dependencies
- Verify Python version compatibility

---

## 🎉 Success!

Once deployed, share your app:
- Post on LinkedIn and tag @AIMakerspace
- Share with friends and colleagues
- Add to your portfolio

**Your deployed URLs:**
- Frontend: `https://your-frontend.vercel.app`
- Backend: `https://your-backend.vercel.app`

---

## 📝 Custom Domain (Optional)

Want a custom domain like `mental-coach.yourdomain.com`?

1. Go to your Vercel project settings
2. Navigate to **Domains**
3. Add your custom domain
4. Follow DNS configuration instructions
5. Wait for SSL certificate provisioning (automatic)

---

## 🔄 Continuous Deployment

With GitHub integration:
- Every push to `main` triggers automatic deployment
- Preview deployments for pull requests
- Automatic rollback if builds fail

---

**Need help?** Check the [Vercel Documentation](https://vercel.com/docs) or reach out to the community!

Built with 💜 by aspiring AI Engineers

