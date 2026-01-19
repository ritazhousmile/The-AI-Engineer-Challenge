# ✅ Deployment Checklist

Use this checklist to ensure everything is configured correctly before and after deployment.

## 📋 Pre-Deployment Checklist

### Code Preparation
- [ ] All code committed to GitHub
- [ ] No sensitive data in code (API keys, tokens)
- [ ] `.env` files in `.gitignore`
- [ ] All dependencies listed in `requirements.txt` / `package.json`

### Backend Preparation
- [ ] `api/index.py` is ready
- [ ] Database initialization code works
- [ ] Error handling implemented
- [ ] CORS configured
- [ ] Rate limiting configured (optional)

### Frontend Preparation
- [ ] `frontend/` directory ready
- [ ] Environment variables documented
- [ ] API URL configuration ready
- [ ] Build command works locally

---

## 🔧 Backend Deployment Checklist

### Vercel Configuration
- [ ] Project name set: `mental-coach-api`
- [ ] Framework: Other
- [ ] Root directory: (empty/root)
- [ ] Build command: (empty)
- [ ] Output directory: (empty)

### Environment Variables
- [ ] `OPENAI_API_KEY` - Your OpenAI API key
- [ ] `API_KEY` - Optional API key for authentication
- [ ] `RATE_LIMIT_ENABLED` - Set to `true` or `false`
- [ ] `RATE_LIMIT_REQUESTS` - Number (e.g., `60`)
- [ ] `RATE_LIMIT_WINDOW` - Seconds (e.g., `60`)
- [ ] `ALLOWED_ORIGINS` - Your frontend URL or `*`
- [ ] `DB_PATH` - `/tmp/conversations.db` (for Vercel)

### Post-Deployment
- [ ] Backend URL copied
- [ ] Health check works: `/api/health`
- [ ] API docs accessible: `/docs`
- [ ] Test chat endpoint works
- [ ] Database initializes correctly

---

## 🎨 Frontend Deployment Checklist

### Vercel Configuration
- [ ] Project name set: `mental-coach-frontend`
- [ ] Framework: Next.js
- [ ] Root directory: `frontend`
- [ ] Build command: `npm run build`
- [ ] Output directory: `.next`

### Environment Variables
- [ ] `NEXT_PUBLIC_API_URL` - Your backend URL (no trailing slash)

### Post-Deployment
- [ ] Frontend URL copied
- [ ] Frontend loads correctly
- [ ] Can send messages
- [ ] Streaming responses work
- [ ] Conversation history works
- [ ] Mobile responsive
- [ ] No console errors

---

## 🔗 Integration Checklist

### Backend CORS
- [ ] `ALLOWED_ORIGINS` includes frontend URL
- [ ] Or set to `*` for development (not recommended for production)

### Connection Test
- [ ] Frontend can reach backend
- [ ] No CORS errors in browser console
- [ ] API calls succeed

---

## 🔒 Security Checklist

### API Security
- [ ] `API_KEY` set (recommended for production)
- [ ] `ALLOWED_ORIGINS` configured (not `*` in production)
- [ ] Rate limiting enabled
- [ ] HTTPS enabled (automatic on Vercel)

### Secrets Management
- [ ] No API keys in code
- [ ] All secrets in environment variables
- [ ] `.env` files not committed to git

---

## 📊 Testing Checklist

### Backend Tests
- [ ] Health endpoint: `GET /api/health`
- [ ] Chat endpoint: `POST /api/chat`
- [ ] Conversation endpoint: `GET /api/conversations/{id}`
- [ ] Webhook endpoint: `POST /api/webhook`
- [ ] Error handling works

### Frontend Tests
- [ ] Send message
- [ ] Receive streaming response
- [ ] Multiple messages (conversation context)
- [ ] Clear chat button
- [ ] Error messages display
- [ ] Loading states work

### Integration Tests
- [ ] Slack bot (if deployed)
- [ ] Discord bot (if deployed)
- [ ] React widget (if embedded)

---

## 🐛 Troubleshooting Checklist

If something doesn't work:

### Backend Issues
- [ ] Check Vercel function logs
- [ ] Verify environment variables
- [ ] Test API locally first
- [ ] Check OpenAI API key is valid
- [ ] Verify database path is correct

### Frontend Issues
- [ ] Check browser console for errors
- [ ] Verify `NEXT_PUBLIC_API_URL` is correct
- [ ] Check network tab for API calls
- [ ] Verify backend is accessible
- [ ] Check CORS configuration

### Database Issues
- [ ] Verify `DB_PATH` is `/tmp/conversations.db` for Vercel
- [ ] Check function logs for database errors
- [ ] Consider external database for persistence

---

## 📝 Post-Deployment

### Documentation
- [ ] Update README with deployment URLs
- [ ] Document environment variables
- [ ] Add deployment notes

### Monitoring
- [ ] Set up health check monitoring
- [ ] Monitor error rates
- [ ] Track API usage
- [ ] Set up alerts (optional)

### Sharing
- [ ] Frontend URL ready to share
- [ ] Test in incognito mode
- [ ] Test on mobile device
- [ ] Share with team/users

---

## 🎯 Quick Test Commands

```bash
# Test backend health
curl https://your-backend.vercel.app/api/health

# Test backend chat (with API key if set)
curl -X POST https://your-backend.vercel.app/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"message": "Hello"}'

# Test frontend
# Just visit the URL in your browser
```

---

## ✅ Final Checklist

- [ ] Everything from above completed
- [ ] All tests passing
- [ ] No errors in logs
- [ ] Ready for users
- [ ] Documentation updated

**🎉 Deployment Complete!**

---

**Need help?** Check:
- [Deployment Guide](./DEPLOYMENT_V2.md)
- [Troubleshooting Guide](./TROUBLESHOOTING_DEPLOYMENT.md)
- Vercel deployment logs
