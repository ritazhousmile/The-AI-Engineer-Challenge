# 🚀 Push and Deploy Instructions

## Step 1: Push to GitHub

Since there's a certificate issue with automated push, please push manually:

```bash
git push origin main
```

Or use GitHub Desktop / GitHub website to push your changes.

**What's being pushed:**
- ✅ Next.js security fix (15.0.3 → 15.5.7)
- ✅ All deployment guides
- ✅ Integration examples
- ✅ All improvements

---

## Step 2: Deploy on Vercel

### Option A: Automatic Deployment (If Already Connected)

If your GitHub repo is already connected to Vercel:
1. **Just push to GitHub** - Vercel will automatically redeploy!
2. Go to your Vercel dashboard
3. Watch the deployment happen automatically
4. Done! ✅

### Option B: Manual Redeploy

If you need to manually redeploy:

#### For Frontend:

1. Go to: https://vercel.com/dashboard
2. Click on your **`mental-coach-frontend`** project
3. Go to **"Deployments"** tab
4. Click **"..."** on the latest deployment
5. Click **"Redeploy"**
6. Confirm by clicking **"Redeploy"**
7. Wait 2-3 minutes

#### For Backend:

1. Go to: https://vercel.com/dashboard
2. Click on your **`mental-coach-api`** project
3. Go to **"Deployments"** tab
4. Click **"..."** on the latest deployment
5. Click **"Redeploy"**
6. Confirm by clicking **"Redeploy"**
7. Wait 1-2 minutes

---

## Step 3: Verify Deployment

### Check Frontend:

1. Visit your frontend URL
2. The security error should be gone
3. Test sending a message

### Check Backend:

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

---

## ✅ What's Fixed

- ✅ Next.js updated to 15.5.7 (security fix)
- ✅ CVE-2025-66478 vulnerability patched
- ✅ Ready for deployment

---

## 🎯 Quick Commands

```bash
# Push to GitHub
git push origin main

# Then Vercel will auto-deploy, or manually redeploy in dashboard
```

---

**After pushing, Vercel should automatically detect the changes and redeploy!** 🎉
