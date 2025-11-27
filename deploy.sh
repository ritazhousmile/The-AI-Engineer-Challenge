#!/bin/bash

echo "🚀 Mental Coach AI Deployment Script"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Deploy Frontend
echo -e "${BLUE}Step 1: Deploying Frontend...${NC}"
echo ""
cd frontend

echo "Running: vercel --prod"
echo ""
echo "When prompted, answer:"
echo "  - Set up and deploy? Y"
echo "  - Which scope? [Select your account]"
echo "  - Link to existing project? N"
echo "  - What's your project's name? mental-coach-frontend (or press Enter)"
echo "  - In which directory is your code located? ./ (press Enter)"
echo "  - Want to modify these settings? N"
echo ""
read -p "Press Enter to start frontend deployment..."

vercel --prod

FRONTEND_URL=$?
echo ""
echo -e "${GREEN}✅ Frontend deployed!${NC}"
echo "Copy the Production URL shown above - you'll need it for the backend!"
echo ""
read -p "Press Enter to continue to backend deployment..."

# Step 2: Deploy Backend
echo ""
echo -e "${BLUE}Step 2: Deploying Backend...${NC}"
echo ""
cd ..

echo "Running: vercel --prod"
echo ""
echo "When prompted, answer:"
echo "  - Set up and deploy? Y"
echo "  - Which scope? [Select your account]"
echo "  - Link to existing project? N"
echo "  - What's your project's name? mental-coach-api (or press Enter)"
echo "  - In which directory is your code located? ./ (press Enter)"
echo "  - Want to modify these settings? N"
echo ""
read -p "Press Enter to start backend deployment..."

vercel --prod

echo ""
echo -e "${GREEN}✅ Backend deployed!${NC}"
echo ""

# Step 3: Instructions for environment variables
echo -e "${YELLOW}📋 Next Steps:${NC}"
echo ""
echo "1. Add OPENAI_API_KEY to backend:"
echo "   vercel env add OPENAI_API_KEY production"
echo "   Then paste: your-openai-api-key-here"
echo ""
echo "2. Add NEXT_PUBLIC_API_URL to frontend:"
echo "   cd frontend"
echo "   vercel env add NEXT_PUBLIC_API_URL production"
echo "   Then paste your backend URL"
echo ""
echo "3. Redeploy both projects:"
echo "   vercel --prod (in root directory)"
echo "   cd frontend && vercel --prod (in frontend directory)"
echo ""
echo -e "${GREEN}🎉 Deployment complete!${NC}"

