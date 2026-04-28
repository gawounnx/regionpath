import os, requests
from dotenv import load_dotenv

load_dotenv()

JOB_API_KEY = os.getenv("WORKNET_KEY_JOB")
JOB_DIC_URL = "https://www.work24.go.kr/cm/openApi/call/wk/callOpenApiSvcInfo310L01.do"

JOB_TO_NCS = {
    "백엔드":    ["응용SW엔지니어링", "서버프로그램구현", "데이터베이스"],
    "프론트엔드": ["UI/UX엔지니어링", "화면구현", "프론트엔드개발"],
    "풀스택":    ["응용SW엔지니어링", "UI/UX엔지니어링", "서버프로그램구현"],
    "데이터분석": ["빅데이터분석", "데이터베이스", "통계분석"],
    "AI":        ["머신러닝", "딥러닝모델링", "빅데이터분석"],
    "클라우드":  ["클라우드인프라구축", "서버프로그램구현"],
    "보안":      ["정보보안관리", "취약점분석"],
    "기계설계":  ["기계설계", "CAD설계"],
    "회계":      ["회계감사", "세무관리"],
    "영업":      ["영업관리", "고객관계관리"],
}

SKILL_TO_NCS = {
    "Python":  ["응용SW엔지니어링", "빅데이터분석"],
    "Java":    ["응용SW엔지니어링", "서버프로그램구현"],
    "Spring":  ["서버프로그램구현"],
    "SQL":     ["데이터베이스"],
    "FastAPI": ["서버프로그램구현"],
    "React":   ["UI/UX엔지니어링"],
    "AWS":     ["클라우드인프라구축"],
    "Docker":  ["클라우드인프라구축"],
    "PyTorch": ["딥러닝모델링"],
}

def fetch_ncs_from_api(keyword: str, count: int = 5) -> list[dict]:
    if not JOB_API_KEY:
        return []
    try:
        params = {
            "authKey":    JOB_API_KEY,
            "returnType": "json",
            "keyword":    keyword,
            "maxCount":   count
        }
        res = requests.get(JOB_DIC_URL, params=params, timeout=5)
        res.raise_for_status()
        data  = res.json()
        items = data.get("searchResultList", [])
        return [
            {
                "unit_name":   item.get("ntcsNm", ""),
                "unit_code":   item.get("ntcsCd", ""),
                "large_name":  item.get("kcsCdNmLarge", ""),
                "medium_name": item.get("kcsCdNmMedium", ""),
                "small_name":  item.get("kcsCdNmSmall", ""),
                "detail_code": item.get("kcsCdDetail", ""),
            }
            for item in items if item.get("ntcsNm")
        ]
    except Exception as e:
        print(f"[NCS API 오류] {e}")
        return []

def get_ncs_tags_local(job: str, skills: list[str]) -> list[str]:
    tags = set()
    for key, values in JOB_TO_NCS.items():
        if key in job:
            tags.update(values)
            break
    for skill in skills:
        if skill in SKILL_TO_NCS:
            tags.update(SKILL_TO_NCS[skill])
    return list(tags)[:5]

def get_ncs_tags(job: str, skills: list[str]) -> list[str]:
    result = fetch_ncs_from_api(job)
    if result:
        return [r["unit_name"] for r in result]
    for skill in skills[:2]:
        result = fetch_ncs_from_api(skill)
        if result:
            return [r["unit_name"] for r in result]
    return get_ncs_tags_local(job, skills)

def get_ncs_detail(job: str) -> list[dict]:
    return fetch_ncs_from_api(job, count=5)
