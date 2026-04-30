# 📍 RegionPath

> 지역 청년의 취업 정보 격차를 해소하는 AI 기반 채용 매칭 플랫폼

![Status](https://img.shields.io/badge/status-in--development-yellow)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 💡 개요

서울 청년 1만 명당 채용공고 412건, 전남 69건 — 약 6배 격차. 비수도권 청년의 43%가 수도권 이주 의향을 밝히며, 이들이 꼽는 이유 1순위는 **적합한 일자리 부족(38.1%)** 이다. 문제는 일자리가 없는 게 아니라, **지역 공고와 청년 스펙 사이의 정보 단절**이다.

RegionPath는 지역별 채용공고 트렌드 시각화, AI 기반 포트폴리오 자동 생성, 공고-포트폴리오 매칭 분석을 하나의 플로우로 연결해 지역 청년이 실질적인 취업 경쟁력을 갖출 수 있도록 돕는다.

**타겟 사용자**

| 사용자 | 상황 | 니즈 |
|---|---|---|
| 지역 취준생 | 지역 공고 정보 부족, 스펙 경쟁력 불확실 | 지역 시장 파악 + 내 경쟁력 확인 |
| 정부·훈련기관 | 지역별 훈련 수요 파악 어려움 | 직종별 수요 데이터 기반 훈련 개설 |

**문제 근거**

- 청년 인구 1만 명당 채용공고: 서울 412건 vs 전남 69건 (국가균형발전지원센터, 2022)
- 비수도권 청년 수도권 이주 의향 43%, 이유 1위 일자리 75% (한국은행, 2022)
- '쉬었음' 청년의 취업 포기 1순위: 적합한 일자리 부족 38.1% (한국고용정보원)
- 경력 위주 채용 구조 20.4%, 과도한 스펙 요건 19.6%로 구직 장벽 (한국노동연구원)

---

## 🚀 주요 기능

| 우선순위 | 기능 | 설명 |
|---|---|---|
| 🔴 P0 | 지역별 공고 트렌드 시각화 | 직종·지역별 채용공고 현황, 수도권 대비 격차 시각화 (고용24 API) |
| 🔴 P0 | AI 포트폴리오 자동 생성 | 스펙 입력 → Claude API 기반 맞춤형 포트폴리오 문서 자동 생성 |
| 🔴 P0 | 공고-포트폴리오 매칭 분석 | 생성된 포폴 ↔ 지역 공고 적합도 분석 + 부족 역량 도출 |
| 🟡 P1 | 맞춤 훈련과정 추천 | 부족 역량 기반 지역 내 HRD-Net 훈련과정 자동 매칭 |
| 🟡 P1 | 지역별 직종 수요 대시보드 | 정부·훈련기관용 지역별 희망 직종 분포 및 훈련 공백 시각화 |
| 🟢 P2 | 수도권 vs 지역 비교 리포트 | 공고 수·연봉·훈련과정 격차 수치 비교 |

### 🗺 국내 지도 시각화 (히트맵)

직종 선택 시 17개 시·도(특별시, 광역시, 도, 특별자치시·도)를 파란색(낮음) ~ 빨간색(높음) 히트맵으로 시각화하며 3개 탭으로 분리 제공한다.

| 탭 | 내용 | 데이터 출처 |
|---|---|---|
| 탭 1 — 채용공고 현황 | 지역별 특정 직종 채용공고 수 | 고용24 OpenAPI |
| 탭 2 — 청년 수요 현황 | 지역별 특정 직종 희망 청년 수 | 서비스 내 사용자 입력 집계 |
| 탭 3 — 미스매치 현황 | 공급(공고) vs 수요(희망자) 격차 | 탭1 - 탭2 교차 분석 |

> 미스매치 지수 = (희망자 수 - 채용공고 수) / 희망자 수 × 100  
> 수치가 높을수록 공급 부족 지역 → 정부·훈련기관의 훈련 개설 우선순위 근거로 활용

---

## 🔄 서비스 플로우

```
[① 트렌드 파악]         [② 포폴 생성]           [③ 매칭 + 훈련 추천]
지역·직종 공고 현황  →   스펙 입력               포폴 ↔ 공고 적합도
수도권 격차 확인         Claude API 포폴 생성     부족 역량 도출
"시장이 어떤가"          "어떻게 보여줄까"        HRD-Net 훈련과정 추천
```

---

## 📦 아키텍처

```
┌──────────────────────────────────┐
│         Next.js Frontend         │
│  트렌드 시각화 / 포폴 생성 / 매칭 │
└────────────────┬─────────────────┘
                 │ REST API
┌────────────────▼─────────────────┐
│          FastAPI Backend         │
│  (메모리 캐싱, 외부 DB 없음)      │
└────┬──────────┬──────────┬───────┘
     │          │          │
┌────▼───┐ ┌───▼────┐ ┌───▼──────┐
│고용24  │ │Claude  │ │HRD-Net   │
│  API   │ │  API   │ │  API     │
│공고수집│ │포폴생성│ │훈련조회  │
└────────┘ └────────┘ └──────────┘
```

---

## 🛠 기술 스택

**Frontend**

![Next.js](https://img.shields.io/badge/Next.js-000000?logo=nextdotjs&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)
![Recharts](https://img.shields.io/badge/Recharts-FF6384?logo=react&logoColor=white)

**Backend**

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)

**AI / 외부 API**

![Anthropic](https://img.shields.io/badge/Claude_API-D97757?logo=anthropic&logoColor=white)
![고용24](https://img.shields.io/badge/고용24_API-0066CC?logoColor=white)
![HRD-Net](https://img.shields.io/badge/HRD--Net_API-00A651?logoColor=white)

**인프라**

![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=githubactions&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?logo=vercel&logoColor=white)

---

## 📁 프로젝트 구조

```
regionpath/
├── frontend/                   # Next.js 앱
│   ├── app/
│   │   ├── trend/              # ① 트렌드 시각화
│   │   ├── portfolio/          # ② 포트폴리오 생성
│   │   └── match/              # ③ 매칭 + 훈련 추천
│   └── components/
├── backend/                    # FastAPI 서버
│   ├── main.py
│   ├── routers/
│   │   ├── trend.py            # 고용24 API 연동
│   │   ├── portfolio.py        # Claude API 포폴 생성
│   │   └── match.py            # 매칭 분석 + HRD-Net
│   └── cache.py                # 메모리 캐싱
├── docs/                       # API 스펙, 기획 문서
└── .github/
    └── workflows/
        ├── frontend.yml
        └── backend.yml
```

---

## 🚀 시작하기

### 사전 요구사항

- Node.js 18+
- Python 3.11+
- 고용24 OpenAPI 키 ([발급](https://www.work24.go.kr))
- HRD-Net API 키 ([발급](https://www.data.go.kr))
- Claude API 키 ([발급](https://console.anthropic.com))

### 환경변수 설정

```bash
# backend/.env
WORK24_API_KEY=your_key
HRDNET_API_KEY=your_key
ANTHROPIC_API_KEY=your_key

# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 로컬 실행

```bash
# 레포 클론
git clone https://github.com/your-org/regionpath.git
cd regionpath

# 백엔드
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# 프론트엔드
cd frontend
npm install
npm run dev
```

---

## 🌿 브랜칭 전략

```
main
└── develop
    ├── feature/trend-*         # 트렌드 시각화
    ├── feature/portfolio-*     # 포트폴리오 생성
    └── feature/match-*         # 매칭 + 훈련 추천
```

- `main`: 배포 브랜치 — 직접 push 금지
- `develop`: 통합 브랜치
- `feature/*`: 기능 단위 개발 → PR → develop 머지

---

## 👥 팀 구성

| 이름 | 담당 |
|---|---|
| 유승환 | 트렌드 시각화, 고용24 API 연동, 인프라 |
| 팀원 2 | 포트폴리오 자동 생성, Claude API 연동 |
| 팀원 3 | 매칭 분석, HRD-Net API 연동, 훈련 추천 |

---

## 📅 개발 일정

| 단계 | 기간 |
|---|---|
| 기획 및 설계 | ~4월 4주 |
| MVP 개발 | 5월 1주 ~ 5월 2주 |
| 공모전 제출 | 5월 2주 말 |

---

## ⚠️ 제약 사항

- **고용24 API**: 실시간 호출 기준, Rate Limit 초과 시 메모리 캐싱으로 대응
- **외부 DB 미사용**: MVP 기준 FastAPI 메모리 캐싱으로 운영, 추후 Redis 전환 예정
- **포트폴리오 저장**: MVP에서는 클라이언트 상태 유지, 세션 종료 시 초기화

---

## 📄 라이선스

MIT