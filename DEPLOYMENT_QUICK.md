# 🚀 Micro-Hygiene Wiki 빠른 배포 가이드

## 사전 준비

1. [Railway](https://railway.app) 계정 생성
2. [Vercel](https://vercel.com) 계정 생성
3. [Cloudflare](https://dash.cloudflare.com) 계정 생성 (Turnstile용)

## CLI 로그인

```bash
# Railway 로그인
railway login

# Vercel 로그인
vercel login
```

## 방법 1: 자동 배포 스크립트 사용

```bash
# 프로젝트 루트에서
chmod +x DEPLOY.sh
./DEPLOY.sh
```

## 방법 2: 수동 배포

### 1. 백엔드 배포 (Railway)

```bash
cd backend

# 프로젝트 초기화 (처음 한 번)
railway init --name "micro-hygiene-wiki"

# 환경 변수 설정
railway variables --set "SECRET_KEY=$(openssl rand -base64 32)"
railway variables --set "DEBUG=False"
railway variables --set "ALLOWED_HOSTS=*"

# 배포
railway up

# 배포된 URL 확인
railway domain
```

### 2. 프론트엔드 배포 (Vercel)

```bash
cd frontend

# 환경 변수 파일 생성
cat > .env.production << EOF
VITE_API_URL=https://your-railway-domain.railway.app/api
VITE_TURNSTILE_SITE_KEY=your-turnstile-site-key
EOF

# 배포
vercel --prod
```

## 환경 변수 설정

### Railway (백엔드)

| 변수 | 설명 | 예시 |
|------|------|------|
| `SECRET_KEY` | Django 비밀키 | 자동 생성 권장 |
| `DEBUG` | 디버그 모드 | `False` |
| `ALLOWED_HOSTS` | 허용 호스트 | `*` 또는 도메인 |
| `FRONTEND_URL` | 프론트엔드 URL | `https://your-app.vercel.app` |
| `TURNSTILE_SECRET_KEY` | Cloudflare Turnstile | `0x...` |
| `DATABASE_URL` | DB URL | Railway 자동 설정 |

### Vercel (프론트엔드)

| 변수 | 설명 | 예시 |
|------|------|------|
| `VITE_API_URL` | API URL | `https://...railway.app/api` |
| `VITE_TURNSTILE_SITE_KEY` | Turnstile 사이트 키 | `0x...` |

## Cloudflare Turnstile 설정

1. [Cloudflare Dashboard](https://dash.cloudflare.com) → Turnstile
2. "Add Site" 클릭
3. 사이트 이름: `Micro-Hygiene Wiki`
4. 도메인: `localhost`, `your-vercel-domain.vercel.app`
5. Widget 모드: `Managed`
6. 키 복사:
   - **Site Key** → Vercel `VITE_TURNSTILE_SITE_KEY`
   - **Secret Key** → Railway `TURNSTILE_SECRET_KEY`

## 배포 후 확인 사항

### 백엔드 확인
```bash
# Railway 로그 확인
railway logs

# 데이터베이스 마이그레이션 확인
railway run python manage.py migrate

# 슈퍼유저 생성 (선택)
railway run python manage.py createsuperuser
```

### 프론트엔드 확인
```bash
# Vercel 대시보드에서 배포 상태 확인
vercel list
```

### API 테스트
```bash
# 팁 목록 조회
curl https://your-railway-domain.railway.app/api/tips/

# 카테고리 목록 조회
curl https://your-railway-domain.railway.app/api/categories/
```

## 문제 해결

### CORS 오류
Railway 대시보드에서 `FRONTEND_URL`을 정확한 Vercel 도메인으로 설정

### 500 Internal Server Error
```bash
# Railway 로그 확인
railway logs
```

### 데이터베이스 연결 오류
Railway는 자동으로 PostgreSQL을 프로비저닝합니다. `DATABASE_URL`이 자동 설정되는지 확인.

## 🎉 배포 완료 후

1. **Google Search Console** 등록
2. **Google Analytics** 설정 (선택)
3. **마케팅 자료** 준비 (`marketing/` 폴더 참고)
4. **Reddit/TikTok** 홍보 시작

---

## 📞 지원

- Railway 문서: https://docs.railway.app
- Vercel 문서: https://vercel.com/docs
- Django 배포: https://docs.djangoproject.com/en/stable/howto/deployment/
