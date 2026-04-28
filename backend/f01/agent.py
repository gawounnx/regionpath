import os, json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

PORTFOLIO_PROMPT = PromptTemplate.from_template("""
당신은 비수도권 청년 취업 포트폴리오 전문가입니다.
아래 구직자 정보를 분석하여 포트폴리오를 생성하세요.

[구직자 정보]
- 희망 직무: {job}
- 희망 산업: {industry}
- 희망 지역: {region}
- 보유 기술: {skills}
- 자격증: {certificates}
- 학력: {education}
- 프로젝트: {projects}
- 활동 이력: {activities}
- 훈련 이력: {training_history}

[출력 형식 — JSON만 출력, 다른 텍스트 없이]
{{
  "portfolio_summary": "구직자의 강점과 목표를 담은 2~3문장 한국어 요약. {region} 지역 취업 시장 특성 반영.",
  "strength_tags": ["실제 보유 스펙 기반 강점 태그 3~5개"],
  "weakness_hint": "희망 직무 대비 가장 보완이 필요한 부분 한 문장",
  "completeness_score": 0.0
}}

작성 기준:
- strength_tags는 실제 입력된 스펙에서만 추출 (과장 금지)
- weakness_hint는 F-02 갭 분석의 시작점이 되므로 구체적으로 작성
- completeness_score: 기술/자격증/프로젝트 각각 0.33점씩 부여
""")

def generate_portfolio_with_llm(
    job: str, industry: str, region: str, profile: dict
) -> dict:
    prompt = PORTFOLIO_PROMPT.format(
        job=job,
        industry=industry or "미입력",
        region=region or "미입력",
        skills=", ".join(profile.get("skills", [])) or "없음",
        certificates=", ".join(profile.get("certificates", [])) or "없음",
        education=profile.get("education", "없음"),
        projects=", ".join([
            p.get("name", "") for p in profile.get("projects", [])
        ]) or "없음",
        activities=", ".join(profile.get("activities", [])) or "없음",
        training_history=", ".join(
            profile.get("training_history", [])
        ) or "없음"
    )

    response = llm.invoke(prompt).content.strip()

    if "```" in response:
        parts = response.split("```")
        response = parts[1] if len(parts) > 1 else response
        if response.lower().startswith("json"):
            response = response[4:].strip()

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {
            "portfolio_summary": f"{region} {industry} 분야 {job} 희망 구직자입니다.",
            "strength_tags": profile.get("skills", [])[:3],
            "weakness_hint": "추가 분석이 필요합니다.",
            "completeness_score": 0.3
        }
