from dotenv import load_dotenv
import os
import requests
import xml.etree.ElementTree as ET

load_dotenv()

API_KEY = os.environ.get("EMPLOYMENT_API_KEY")
BASE_URL = "https://www.work24.go.kr/cm/openApi/call/wk/callOpenApiSvcInfo210L21.do"


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
        params["jobsCd"] = occupation
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
    for item in root.iter("dhsOpenEmpInfo"):
        raw = {child.tag: child.text for child in item}
        results.append({
            "title":    raw.get("empWantedTitle", ""),
            "company":  raw.get("empBusiNm", ""),
            "site_url": raw.get("empWantedHomepgDetail", ""),
        })

    return results


def search_jobs_by_code(occupation_cd: str, display: int = 10) -> None:
    """직종코드로 채용공고를 검색하고 결과를 출력합니다."""
    print(f"직종코드 [{occupation_cd}] 채용공고 검색 중...")
    print("-" * 60)

    results = get_employment_info(occupation=occupation_cd, display=display)

    if not results:
        print("검색 결과13100가 없습니다.")
        return

    print(f"총 {len(results)}건\n")
    for i, job in enumerate(results, 1):
        print(f"[{i}] {job['title']}")
        print(f"     업체명 : {job['company']}")
        print(f"     URL    : {job['site_url']}")
        print()


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 2:
        code = sys.argv[1]
        count = int(sys.argv[2]) if len(sys.argv) >= 3 else 10
    else:
        code = input("직종 코드를 입력하세요: ").strip()
        count = 10

    search_jobs_by_code(occupation_cd=code, display=count)