# 🚀 Complete Deployment Guide v2.0

This guide covers deploying the Mental Coach AI chatbot with all new features including conversation history, database storage, authentication, and integrations.

## 📋 Prerequisites

- ✅ GitHub account with your repository
- ✅ Vercel account (free tier works)
- ✅ OpenAI API key
- ✅ Your code pushed to GitHub

---

## 🎯 Quick Deployment (5 Minutes)

### Step 1: Deploy Backend API

1. Go to [https://vercel.com/new](https://vercel.com/new)
2. Import your repository: `ritazhousmile/The-AI-Engineer-Challenge`
3. Configure:
   - **Project Name:** `mental-coach-api`
   - **Framework Preset:** Other
   - **Root Directory:** Leave empty (root)
   - **Build Command:** Leave empty
   - **Output Directory:** Leave empty

4. **Add Environment Variables** (IMPORTANT):
   
   Click "Environment Variables" and add:

   | Name | Value | Environment |
   |------|-------|-------------|
   | `OPENAI_API_KEY` | `sk-proj-...` (your OpenAI key) | All |
   | `API_KEY` | `your-secure-api-key` (optional, for API protection) | All |
   | `RATE_LIMIT_ENABLED` | `true` | All |
   | `RATE_LIMIT_REQUESTS` | `60` | All |
   | `RATE_LIMIT_WINDOW` | `60` | All |
   | `ALLOWED_ORIGINS` | `*` (or your frontend URL) | All |
   | `DB_PATH` | `/tmp/conversations.db` (Vercel uses /tmp) | All |

5. Click **"Deploy"**

6. **Wait for deployment** (1-2 minutes)

7. **Copy your backend URL** (e.g., `https://mental-coach-api-xyz.vercel.app`)

---

### Step 2: Deploy Frontend

1. Go to [https://vercel.com/new](https://vercel.com/new) again
2. Import the same repository: `ritazhousmile/The-AI-Engineer-Challenge`
3. Configure:
   - **Project Name:** `mental-coach-frontend`
   - **Framework Preset:** Next.js (auto-detected)
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build` (default)
   - **Output Directory:** `.next` (default)

4. **Add Environment Variable**:
   
   | Name | Value | Environment |
   |------|-------|-------------|
   | `NEXT_PUBLIC_API_URL` | Your backend URL from Step 1 | All |

5. Click **"Deploy"**

6. **Wait for deployment** (2-3 minutes)

7. **Copy your frontend URL** (e.g., `https://mental-coach-frontend-xyz.vercel.app`)

---

### Step 3: Update Backend CORS (if needed)

If you set a specific frontend URL, update the backend:

1. Go to your backend project on Vercel
2. Settings → Environment Variables
3. Update `ALLOWED_ORIGINS`:
   ```
   https://mental-coach-frontend-xyz.vercel.app
   ```
4. Redeploy backend

---

## ✅ Test Your Deployment

### Test Backend

```bash
# Health check
curl https://your-backend-url.vercel.app/api/health

# Should return:
# {
#   "status": "ok",
#   "version": "2.0.0",
#   "database": "connected",
#   "openai_configured": true
# }
```

### Test Frontend

1. Visit your frontend URL
2. Send a test message
3. Verify streaming response works
4. Check that conversation persists (send multiple messages)

---

## 🔧 Environment Variables Reference

### Backend Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | - | Your OpenAI API key |
| `API_KEY` | ❌ No | - | API key for authentication |
| `RATE_LIMIT_ENABLED` | ❌ No | `true` | Enable rate limiting |
| `RATE_LIMIT_REQUESTS` | ❌ No | `60` | Requests per window |
| `RATE_LIMIT_WINDOW` | ❌ No | `60` | Time window in seconds |
| `ALLOWED_ORIGINS` | ❌ No | `*` | CORS allowed origins (comma-separated) |
| `DB_PATH` | ❌ No | `conversations.db` | Database path (use `/tmp/` for Vercel) |
| `DEBUG` | ❌ No | `false` | Enable debug mode |

### Frontend Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | ✅ Yes | `http://localhost:8000` | Backend API URL |

---

## 🗄️ Database Considerations

### Vercel (Serverless)

Vercel uses serverless functions, so:
- Database is stored in `/tmp/` directory
- Data is **ephemeral** (may be lost between deployments)
- For production, consider:
  - External database (PostgreSQL, MongoDB)
  - Vercel KV (Redis)
  - Supabase, PlanetScale, or similar

### For Persistent Storage

If you need persistent conversations, consider:

1. **Vercel Postgres** (Recommended)
   - Add via Vercel dashboard
   - Update code to use PostgreSQL instead of SQLite

2. **Supabase** (Free tier available)
   - Create project at supabase.com
   - Get connection string
   - Update database code

3. **MongoDB Atlas** (Free tier available)
   - Create cluster
   - Get connection string
   - Update database code

---

## 🔒 Security Best Practices

### Production Checklist

- [ ] Set `API_KEY` for backend authentication
- [ ] Configure `ALLOWED_ORIGINS` (don't use `*` in production)
- [ ] Enable rate limiting
- [ ] Use HTTPS (automatic on Vercel)
- [ ] Keep API keys secure (never commit to git)
- [ ] Monitor API usage
- [ ] Set up error tracking (Sentry, etc.)

### API Key Generation

Generate a secure API key:
```bash
# Using Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Using OpenSSL
openssl rand -base64 32
```

---

## 🚀 Advanced Deployment Options

### Option 1: Single Vercel Project (Monorepo)

Deploy both frontend and backend in one project:

1. Create `vercel.json` in root:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "frontend/package.json",
      "use": "@vercel/next"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ]
}
```

2. Set environment variables for both

### Option 2: Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ ./api/
COPY .env .

EXPOSE 8000

CMD ["uvicorn", "api.index:app", "--host", "0.0.0.0", "--port", "8000"]
```

Deploy to:
- Railway
- Render
- Fly.io
- DigitalOcean App Platform
- AWS ECS/Fargate
- Google Cloud Run

---

## 🐛 Troubleshooting

### Backend Issues

**Problem:** Database errors
- **Solution:** Use `/tmp/conversations.db` for Vercel, or switch to external database

**Problem:** CORS errors
- **Solution:** Check `ALLOWED_ORIGINS` includes your frontend URL

**Problem:** Rate limit errors
- **Solution:** Adjust `RATE_LIMIT_REQUESTS` or disable temporarily

**Problem:** OpenAI API errors
- **Solution:** Verify `OPENAI_API_KEY` is correct and has credits

### Frontend Issues

**Problem:** Can't connect to API
- **Solution:** Check `NEXT_PUBLIC_API_URL` is correct (no trailing slash)

**Problem:** Build fails
- **Solution:** Check Node.js version (should be 18+)

**Problem:** Environment variables not working
- **Solution:** Variables must start with `NEXT_PUBLIC_` for client-side access

### General Issues

**Problem:** Deployment fails
- **Solution:** Check build logs in Vercel dashboard for specific errors

**Problem:** API returns 500 errors
- **Solution:** Check function logs in Vercel dashboard

---

## 📊 Monitoring & Health Checks

### Health Check Endpoint

Monitor your API:
```bash
curl https://your-api.vercel.app/api/health
```

### Vercel Analytics

1. Enable Vercel Analytics in project settings
2. Monitor:
   - Request volume
   - Response times
   - Error rates

### External Monitoring

Set up uptime monitoring:
- UptimeRobot (free)
- Pingdom
- StatusCake

---

## 🔄 Updating Your Deployment

### Update Code

1. Make changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update feature"
   git push
   ```
3. Vercel automatically redeploys

### Update Environment Variables

1. Go to Vercel project settings
2. Environment Variables
3. Add/update variables
4. Redeploy (automatic or manual)

---

## 📝 Post-Deployment Checklist

- [ ] Backend health check passes
- [ ] Frontend loads correctly
- [ ] Chat functionality works
- [ ] Streaming responses work
- [ ] Conversation history persists (if using database)
- [ ] CORS configured correctly
- [ ] API authentication working (if enabled)
- [ ] Rate limiting configured
- [ ] Error handling works
- [ ] Mobile responsive

---

## 🎉 Success!

Your Mental Coach AI chatbot is now deployed! 

**Next Steps:**
1. Test all features
2. Share your frontend URL
3. Monitor usage and errors
4. Set up integrations (Slack, Discord, etc.)
5. Consider adding analytics

**Share your deployment:**
- Frontend URL: `https://your-frontend.vercel.app`
- Backend API: `https://your-backend.vercel.app`
- API Docs: `https://your-backend.vercel.app/docs`

---

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [Integration Guide](./INTEGRATION_GUIDE.md)
- [Improvements Guide](./IMPROVEMENTS.md)

---

**Need help?** Check the troubleshooting section or review Vercel deployment logs.
