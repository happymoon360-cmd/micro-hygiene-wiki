# 🚀 Render.com 배포 완벽 가이드

## 📋 준비사항

- GitHub 계정 (Render는 GitHub 연동 필수)
- 본 프로젝트를 GitHub에 푸시 (선택사항이나 권장)

---

## 1단계: Render.com 가입

### 1.1 계정 생성
1. https://render.com 접속
2. **"Get Started for Free"** 클릭
3. **GitHub로 계속하기** 선택
4. GitHub 계정으로 로그인 및 권한 허용

### 1.2 조직/개인 선택
- 개인 프로젝트: **"Personal Account"** 선택
- 팀: 팀 계정 생성

---

## 2단계: Blueprint 배포 (가장 쉬운 방법)

### 2.1 render.yaml 사용 (권장)

이 프로젝트에 이미 `render.yaml`이 준비되어 있습니다.

1. Render 대시보드 → **"Blueprints"** 탭
2. **"New Blueprint Instance"** 클릭
3. GitHub 저장소 선택:
   - GitHub에 프로젝트를 푸시한 경우: 해당 저장소 선택
   - 또는 "Upload"로 직접 업로드

### 2.2 수동 설정 (Blueprint 없이)

만약 Blueprint가 안 되면 수동으로:

#### 2.2.1 PostgreSQL 데이터베이스 생성
1. Dashboard → **"New"** → **"PostgreSQL"**
2. 설정:
   - Name: `micro-hygiene-wiki-db`
   - Region: `Singapore` (가장 가까움)
   - Plan: **Free**
3. **"Create Database"** 클릭
4. 생성 후 **"Internal Database URL"** 복사 (나중에 필요)

#### 2.2.2 Web Service 생성
1. Dashboard → **"New"** → **"Web Service"**
2. GitHub 저장소 연결 또는 업로드
3. 설정:
   - Name: `micro-hygiene-wiki-api`
   - Region: `Singapore`
   - Runtime: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2`
   - Plan: **Free**
4. **"Create Web Service"** 클릭

---

## 3단계: 환경 변수 설정

### 3.1 필수 환경 변수

Web Service → **"Environment"** 탭에서 설정:

| 키 | 값 | 설명 |
|----|-----|------|
| `SECRET_KEY` | `openssl rand -base64 32` | Django 비밀키 |
| `DEBUG` | `False` | 디버그 모드 비활성화 |
| `ALLOWED_HOSTS` | `*` | 모든 호스트 허용 |
| `DATABASE_URL` | (자동 설정됨) | PostgreSQL 연결 URL |
| `FRONTEND_URL` | `https://frontend-hrhbee6px-seokjuns-projects-98431b2d.vercel.app` | Vercel 프론트엔드 URL |
| `DISABLE_COLLECTSTATIC` | `1` | static 수집 일시 비활성화 |

### 3.2 Turnstile 설정 (선택)

나중에 Cloudflare에서 키 발급 후:

| 키 | 값 |
|----|-----|
| `TURNSTILE_SECRET_KEY` | `0x4AAAAAA...` |

---

## 4단계: 마이그레이션 실행

### 4.1 Shell 접속
1. Web Service → **"Shell"** 탭
2. 다음 명령어 실행:

```bash
# 마이그레이션
python manage.py migrate --noinput

# 기본 데이터 로드 (선택)
python manage.py seed_tips

# 슈퍼유저 생성 (선택)
python manage.py createsuperuser
```

---

## 5단계: Vercel API URL 업데이트

백엔드 배포 완료 후:

### 5.1 API URL 확인
- Render Dashboard에서 배포된 URL 확인
- 예: `https://micro-hygiene-wiki-api.onrender.com`

### 5.2 Vercel 환경 변수 업데이트

```bash
cd frontend

# .env.production 업데이트
echo "VITE_API_URL=https://micro-hygiene-wiki-api.onrender.com/api" > .env.production
echo "VITE_TURNSTILE_SITE_KEY=your-turnstile-site-key" >> .env.production

# Vercel에 환경 변수 설정
vercel env add VITE_API_URL production
# 값 입력: https://micro-hygiene-wiki-api.onrender.com/api

# 재배포
vercel --prod
```

### 5.3 Render FRONTEND_URL 업데이트

Render Dashboard → Web Service → Environment:
- `FRONTEND_URL` → 실제 Vercel URL로 업데이트

---

## 6단계: 배포 확인

### 6.1 API 테스트

```bash
# 카테고리 목록
curl https://micro-hygiene-wiki-api.onrender.com/api/categories/

# 팁 목록
curl https://micro-hygiene-wiki-api.onrender.com/api/tips/
```

### 6.2 프론트엔드 확인
- 브라우저에서 Vercel URL 접속
- 팁 목록이 로드되는지 확인

---

## 🔄 자동 배포 설정

### Git 연동 시
1. GitHub에 코드 푸시
2. Render가 자동으로 재배포
3. 마이그레이션은 수동으로 실행 필요

### 마이그레이션 자동화 (선택)

`render.yaml`에 이미 포함됨:
```yaml
startCommand: "python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2"
```

---

## ⚠️ 주의사항

### Free Tier 제한
- **Web Service**: 15분 이상 요청 없으면 슬립 (첫 요청 시 30초 지연)
- **PostgreSQL**: 90일 후 또는 1GB 도달 시 삭제
- **월 750시간** 무료 (한 달 전체)

### 슬립 방지 (Keep Alive)
UptimeRobot 등으로 5분마다 ping:
- URL: `https://micro-hygiene-wiki-api.onrender.com/api/categories/`

---

## 🐛 문제 해결

### 500 Internal Server Error
```bash
# Render Dashboard → Logs 확인
# 또는 Shell에서:
python manage.py check
python manage.py migrate --noinput
```

### Database 연결 오류
- `DATABASE_URL` 자동 설정 확인
- 수동 설정 시 Internal Database URL 사용

### CORS 오류
- Render의 `FRONTEND_URL`이 정확한 Vercel 도메인인지 확인
- `ALLOWED_HOSTS`에 `*` 설정되어 있는지 확인

### Static 파일 404
- 현재는 `DISABLE_COLLECTSTATIC=1`로 비활성화
- 필요시 whitenoise 설정 추가

---

## 📞 지원

- Render 문서: https://render.com/docs
- Django on Render: https://render.com/docs/deploy-django
- PostgreSQL on Render: https://render.com/docs/databases
