#!/bin/bash

# Mental Coach AI - Complete Deployment Script v2.0
# This script deploys both backend and frontend with all new features

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Mental Coach AI - Complete Deployment${NC}"
echo "=========================================="
echo ""

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo -e "${RED}❌ Vercel CLI not found. Installing...${NC}"
    npm install -g vercel
fi

# Check if logged in to Vercel
echo -e "${BLUE}Checking Vercel authentication...${NC}"
if ! vercel whoami &> /dev/null; then
    echo -e "${YELLOW}⚠️  Not logged in to Vercel. Please log in:${NC}"
    vercel login
fi

echo -e "${GREEN}✅ Authenticated with Vercel${NC}"
echo ""

# Get OpenAI API key
echo -e "${YELLOW}📝 Environment Variables Setup${NC}"
echo ""
read -p "Enter your OpenAI API key (sk-proj-...): " OPENAI_KEY
if [ -z "$OPENAI_KEY" ]; then
    echo -e "${RED}❌ OpenAI API key is required!${NC}"
    exit 1
fi

# Step 1: Deploy Backend
echo ""
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${BLUE}Step 1: Deploying Backend API${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo ""

# Check if project exists
cd "$(dirname "$0")"

echo "Deploying backend to Vercel..."
echo ""

# Deploy backend
vercel --prod --yes --name mental-coach-api 2>&1 | tee /tmp/backend_deploy.log

# Extract backend URL from deployment
BACKEND_URL=$(grep -o 'https://[^ ]*\.vercel\.app' /tmp/backend_deploy.log | head -1)

if [ -z "$BACKEND_URL" ]; then
    echo -e "${YELLOW}⚠️  Could not auto-detect backend URL. Please check Vercel dashboard.${NC}"
    read -p "Enter your backend URL manually: " BACKEND_URL
fi

echo ""
echo -e "${GREEN}✅ Backend deployed: ${BACKEND_URL}${NC}"
echo ""

# Add environment variables to backend
echo -e "${BLUE}Adding environment variables to backend...${NC}"

# Set backend environment variables
vercel env add OPENAI_API_KEY production <<< "$OPENAI_KEY" 2>/dev/null || vercel env rm OPENAI_API_KEY production --yes 2>/dev/null; vercel env add OPENAI_API_KEY production <<< "$OPENAI_KEY"
vercel env add DB_PATH production <<< "/tmp/conversations.db" 2>/dev/null || vercel env add DB_PATH production <<< "/tmp/conversations.db"
vercel env add RATE_LIMIT_ENABLED production <<< "true" 2>/dev/null || vercel env add RATE_LIMIT_ENABLED production <<< "true"
vercel env add RATE_LIMIT_REQUESTS production <<< "60" 2>/dev/null || vercel env add RATE_LIMIT_REQUESTS production <<< "60"
vercel env add RATE_LIMIT_WINDOW production <<< "60" 2>/dev/null || vercel env add RATE_LIMIT_WINDOW production <<< "60"
vercel env add ALLOWED_ORIGINS production <<< "*" 2>/dev/null || vercel env add ALLOWED_ORIGINS production <<< "*"

echo -e "${GREEN}✅ Environment variables added${NC}"
echo ""

# Redeploy backend with env vars
echo -e "${BLUE}Redeploying backend with environment variables...${NC}"
vercel --prod --yes 2>&1 | tee /tmp/backend_redeploy.log

echo ""
echo -e "${GREEN}✅ Backend deployment complete!${NC}"
echo ""

# Step 2: Deploy Frontend
echo ""
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${BLUE}Step 2: Deploying Frontend${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo ""

cd frontend

echo "Deploying frontend to Vercel..."
echo ""

# Deploy frontend
vercel --prod --yes --name mental-coach-frontend 2>&1 | tee /tmp/frontend_deploy.log

# Extract frontend URL
FRONTEND_URL=$(grep -o 'https://[^ ]*\.vercel\.app' /tmp/frontend_deploy.log | head -1)

if [ -z "$FRONTEND_URL" ]; then
    echo -e "${YELLOW}⚠️  Could not auto-detect frontend URL. Please check Vercel dashboard.${NC}"
    read -p "Enter your frontend URL manually: " FRONTEND_URL
fi

echo ""
echo -e "${GREEN}✅ Frontend deployed: ${FRONTEND_URL}${NC}"
echo ""

# Add environment variable to frontend
echo -e "${BLUE}Adding environment variable to frontend...${NC}"
vercel env add NEXT_PUBLIC_API_URL production <<< "$BACKEND_URL" 2>/dev/null || vercel env rm NEXT_PUBLIC_API_URL production --yes 2>/dev/null; vercel env add NEXT_PUBLIC_API_URL production <<< "$BACKEND_URL"

echo -e "${GREEN}✅ Environment variable added${NC}"
echo ""

# Redeploy frontend with env var
echo -e "${BLUE}Redeploying frontend with environment variable...${NC}"
vercel --prod --yes 2>&1 | tee /tmp/frontend_redeploy.log

echo ""
echo -e "${GREEN}✅ Frontend deployment complete!${NC}"
echo ""

# Step 3: Test Deployment
echo ""
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${BLUE}Step 3: Testing Deployment${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo ""

echo -e "${YELLOW}Testing backend health check...${NC}"
HEALTH_RESPONSE=$(curl -s "${BACKEND_URL}/api/health" || echo "ERROR")

if echo "$HEALTH_RESPONSE" | grep -q "ok"; then
    echo -e "${GREEN}✅ Backend is healthy!${NC}"
else
    echo -e "${YELLOW}⚠️  Backend health check failed. Please check manually.${NC}"
fi

echo ""
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}Your deployment URLs:${NC}"
echo -e "  Frontend: ${GREEN}${FRONTEND_URL}${NC}"
echo -e "  Backend:  ${GREEN}${BACKEND_URL}${NC}"
echo -e "  API Docs: ${GREEN}${BACKEND_URL}/docs${NC}"
echo -e "  Health:   ${GREEN}${BACKEND_URL}/api/health${NC}"
echo ""
echo -e "${YELLOW}📝 Next Steps:${NC}"
echo "  1. Visit your frontend URL and test the chatbot"
echo "  2. Check backend health: curl ${BACKEND_URL}/api/health"
echo "  3. View API docs: ${BACKEND_URL}/docs"
echo ""
echo -e "${GREEN}Happy deploying! 🚀${NC}"
