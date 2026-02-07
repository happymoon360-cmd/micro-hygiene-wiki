#!/bin/bash

# Micro-Hygiene Wiki 배포 스크립트
# 사용법: ./DEPLOY.sh

set -e

echo "🚀 Micro-Hygiene Wiki 배포 시작"
echo "================================"

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 로그인 확인
echo ""
echo "📋 배포 전 확인 사항"
echo "-------------------"

# Railway 로그인 확인
if ! railway whoami &> /dev/null; then
    echo -e "${YELLOW}⚠️  Railway에 로그인이 필요합니다${NC}"
    echo "   실행: railway login"
    echo ""
    railway login
else
    echo -e "${GREEN}✅ Railway 로그인 확인됨${NC}"
fi

# Vercel 로그인 확인
if ! vercel whoami &> /dev/null; then
    echo -e "${YELLOW}⚠️  Vercel에 로그인이 필요합니다${NC}"
    echo "   실행: vercel login"
    echo ""
    vercel login
else
    echo -e "${GREEN}✅ Vercel 로그인 확인됨${NC}"
fi

echo ""
echo "🔄 백엔드 배포 (Railway)"
echo "------------------------"

cd backend

# Railway 프로젝트 초기화/연결
if [ ! -f .railway/config.json ]; then
    echo "📦 Railway 프로젝트를 초기화합니다..."
    railway init --name "micro-hygiene-wiki"
else
    echo "📦 기존 Railway 프로젝트를 사용합니다"
fi

# 환경 변수 설정
echo ""
echo "⚙️  환경 변수 설정"
echo "   (Railway 대시보드에서도 설정 가능)"

# 필수 환경 변수 체크
if [ -f .env ]; then
    source .env
fi

# 기본값 설정
SECRET_KEY=${SECRET_KEY:-$(openssl rand -base64 32)}
DEBUG=${DEBUG:-False}

echo ""
echo "   다음 환경 변수를 Railway에 설정합니다:"
echo "   - SECRET_KEY"
echo "   - DEBUG=False"
echo "   - ALLOWED_HOSTS"
echo "   - FRONTEND_URL (프론트엔드 배포 후 업데이트)"
echo "   - TURNSTILE_SECRET_KEY"

# 변수 설정
railway variables --set "SECRET_KEY=$SECRET_KEY"
railway variables --set "DEBUG=False"
railway variables --set "ALLOWED_HOSTS=*"

echo ""
echo "🚂 Railway에 배포 중..."
railway up

# 배포된 URL 가져오기
BACKEND_URL=$(railway domain)
echo ""
echo -e "${GREEN}✅ 백엔드 배포 완료!${NC}"
echo "   URL: https://$BACKEND_URL"
echo "   API: https://$BACKEND_URL/api/"

cd ..

echo ""
echo "🎨 프론트엔드 배포 (Vercel)"
echo "---------------------------"

cd frontend

# 환경 변수 설정
echo ""
echo "⚙️  프론트엔드 환경 변수 설정"
echo "   VITE_API_URL=https://$BACKEND_URL/api"

# .env.production 생성
cat > .env.production << EOF
VITE_API_URL=https://$BACKEND_URL/api
VITE_TURNSTILE_SITE_KEY=your-turnstile-site-key
EOF

# Vercel 배포
echo ""
echo "🚀 Vercel에 배포 중..."
vercel --prod

echo ""
echo -e "${GREEN}✅ 프론트엔드 배포 완료!${NC}"

cd ..

echo ""
echo "================================"
echo "🎉 배포 완료!"
echo "================================"
echo ""
echo "📌 다음 단계:"
echo "   1. Cloudflare Turnstile 사이트 키 발급"
echo "   2. Vercel 대시보드에서 VITE_TURNSTILE_SITE_KEY 설정"
echo "   3. Railway 대시보드에서 TURNSTILE_SECRET_KEY 설정"
echo "   4. Railway 대시보드에서 FRONTEND_URL 업데이트"
echo "   5. Google Search Console 등록"
echo ""
echo "📚 자세한 내용은 DEPLOYMENT.md를 참조하세요"
