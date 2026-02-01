#!/bin/bash

# Health Check Script for Local Testing
# This script verifies that the deployment configuration is correct

echo "=== Micro-Hygiene Wiki Health Check ==="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print check results
print_check() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $2"
    else
        echo -e "${RED}✗${NC} $2"
    fi
}

# Check 1: Verify Django settings.py syntax
echo "Checking Django settings.py..."
cd backend
python -m py_compile config/settings.py > /dev/null 2>&1
print_check $? "Django settings.py syntax is valid"
cd ..

# Check 2: Verify requirements.txt exists and has necessary packages
echo ""
echo "Checking backend dependencies..."
if [ -f "backend/requirements.txt" ]; then
    print_check 0 "requirements.txt exists"
    grep -q "Django" backend/requirements.txt && print_check 0 "Django included"
    grep -q "dj-database-url" backend/requirements.txt && print_check 0 "dj-database-url included"
    grep -q "django-cors-headers" backend/requirements.txt && print_check 0 "django-cors-headers included"
    grep -q "psycopg2-binary" backend/requirements.txt && print_check 0 "psycopg2-binary included"
    grep -q "gunicorn" backend/requirements.txt && print_check 0 "gunicorn included"
else
    print_check 1 "requirements.txt exists"
fi

# Check 3: Verify Procfile exists
echo ""
echo "Checking Procfile..."
if [ -f "backend/Procfile" ]; then
    print_check 0 "Procfile exists"
    grep -q "gunicorn" backend/Procfile && print_check 0 "Procfile has gunicorn command"
else
    print_check 1 "Procfile exists"
fi

# Check 4: Verify .env.example files
echo ""
echo "Checking environment variable examples..."
if [ -f "backend/.env.example" ]; then
    print_check 0 "backend/.env.example exists"
else
    print_check 1 "backend/.env.example exists"
fi

if [ -f "frontend/.env.example" ]; then
    print_check 0 "frontend/.env.example exists"
else
    print_check 1 "frontend/.env.example exists"
fi

# Check 5: Verify Vercel configuration
echo ""
echo "Checking Vercel configuration..."
if [ -f "frontend/vercel.json" ]; then
    print_check 0 "vercel.json exists"
    grep -q "Vite" frontend/vercel.json && print_check 0 "vercel.json configured for Vite"
else
    print_check 1 "vercel.json exists"
fi

# Check 6: Verify frontend package.json
echo ""
echo "Checking frontend configuration..."
if [ -f "frontend/package.json" ]; then
    print_check 0 "frontend/package.json exists"
    grep -q '"build"' frontend/package.json && print_check 0 "Build script exists"
    grep -q '"preview"' frontend/package.json && print_check 0 "Preview script exists"
else
    print_check 1 "frontend/package.json exists"
fi

# Check 7: Verify deployment documentation
echo ""
echo "Checking deployment documentation..."
if [ -f "DEPLOYMENT.md" ]; then
    print_check 0 "DEPLOYMENT.md exists"
    grep -q "Railway" DEPLOYMENT.md && print_check 0 "Railway instructions included"
    grep -q "Render" DEPLOYMENT.md && print_check 0 "Render instructions included"
    grep -q "Vercel" DEPLOYMENT.md && print_check 0 "Vercel instructions included"
else
    print_check 1 "DEPLOYMENT.md exists"
fi

# Check 8: Verify Django apps structure
echo ""
echo "Checking Django project structure..."
if [ -f "backend/manage.py" ]; then
    print_check 0 "manage.py exists"
else
    print_check 1 "manage.py exists"
fi

if [ -d "backend/apps/wiki" ]; then
    print_check 0 "Wiki app directory exists"
else
    print_check 1 "Wiki app directory exists"
fi

echo ""
echo "=== Health Check Complete ==="
echo ""
echo "If all checks passed, your deployment configuration is ready!"
echo ""
echo "Next steps:"
echo "1. Follow DEPLOYMENT.md for platform-specific instructions"
echo "2. Set environment variables in Railway/Render and Vercel"
echo "3. Deploy and test your application"
