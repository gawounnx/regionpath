from dotenv import load_dotenv
import os
import requests
import xml.etree.ElementTree as ET

load_dotenv()

API_KEY = os.environ.get("EMPLOYMENT_API_KEY")
BASE_URL = "https://www.work24.go.kr/cm/openApi/call/wk/callOpenApiSvcInfo210L01.do"


def get_employment_info(
    region: str = None,
    occupation: str = None,
    keyword: str = None,
    education: str = None,
    career: str = None,
    sal_tp: str = None,
    min_pay: int = None,
    max_pay: int = None,
    start_page: int = 1,
    display: int = 100,
) -> list[dict]:
    """
    워크넷 채용공고 목록을 반환합니다.

    Args:
        region     : 근무지역 코드 (예: "11" 서울, "26" 부산)
        occupation : 직종 코드
        keyword    : 키워드 검색
        education  : 학력 코드 (00~07)
        career     : 경력 코드 (N: 신입, E: 경력, Z: 무관)
        sal_tp     : 임금형태 (D: 일급, H: 시급, M: 월급, Y: 연봉)
        min_pay    : 최소 급여 (sal_tp 입력 시 필수)
        max_pay    : 최대 급여 (sal_tp 입력 시 필수)
        start_page : 시작 페이지 (기본 1, 최대 1000)
        display    : 페이지당 결과 수 (기본 100, 최대 100)

    Returns:
        채용공고 dict 리스트. 주요 키:
            - wantedAuthNo  : 구인인증번호
            - company       : 회사명
            - title         : 채용제목
            - sal           : 급여
            - region        : 근무지역
            - regDt         : 등록일자
            - wantedInfoUrl : 워크넷 채용정보 URL
    """
    params = {
        "authKey":    API_KEY,
        "callTp":     "L",
        "returnType": "XML",
        "startPage":  start_page,
        "display":    display,
    }
    if region:
        params["region"] = region
    if occupation:
        params["occupation"] = occupation
    if keyword:
        params["keyword"] = keyword
    if education:
        params["education"] = education
    if career:
        params["career"] = career
    if sal_tp:
        params["salTp"] = sal_tp
        params["minPay"] = min_pay
        params["maxPay"] = max_pay

    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()

    root = ET.fromstring(response.content)

    error = root.findtext("error")
    if error:
        raise RuntimeError(f"API 오류: {error}")

    results = []
    for item in root.iter("wanted"):
        results.append({child.tag: child.text for child in item})

    return results


# ── 디버깅 ────────────────────────────────────────────────────────────────────
def _debug():
    print("=" * 60)
    print("1. 환경변수 확인")
    print(f"   EMPLOYMENT_API_KEY: {'설정됨 (' + API_KEY[:10] + '...)' if API_KEY else '없음 (.env 확인 필요)'}")
    print(f"   BASE_URL          : {BASE_URL}")
    print()

    print("2. 원시 응답 확인 (파라미터 없이)")
    params_raw = {
        "authKey": API_KEY,
        "callTp": "L",
        "returnType": "XML",
        "startPage": 1,
        "display": 3,
    }
    resp = requests.get(BASE_URL, params=params_raw, timeout=10)
    print(f"   상태코드: {resp.status_code}")
    print(f"   응답:\n{resp.text[:400]}")
    print()

    root = ET.fromstring(resp.content)
    error = root.findtext("error")
    if error:
        print(f"[오류] API 응답 에러: {error}")
        print()
        print("해결 방법:")
        print("  1. https://www.work24.go.kr/cm/e/a/0110/listOpenApiSvcInfo.do 접속")
        print("  2. '채용정보 API' 활용신청")
        print("  3. 승인 후 발급 키를 .env의 EMPLOYMENT_API_KEY에 업데이트")
        return

    print("3. 키워드 검색 테스트 (keyword='백엔드', display=5)")
    try:
        results = get_employment_info(keyword="백엔드", display=5)
        print(f"   채용공고 {len(results)}건\n")
        for i, job in enumerate(results, 1):
            print(f"   [{i}] {job.get('company', '-')} - {job.get('title', '-')}")
            print(f"        지역: {job.get('region', '-')} | 급여: {job.get('sal', '-')} | 등록일: {job.get('regDt', '-')}")
    except RuntimeError as e:
        print(f"   {e}")
    print()

    print("4. 지역 필터 테스트 (region='11', 서울)")
    try:
        results = get_employment_info(region="11", display=3)
        print(f"   서울 채용공고 {len(results)}건")
    except RuntimeError as e:
        print(f"   {e}")
    print("=" * 60)


if __name__ == "__main__":
    _debug()