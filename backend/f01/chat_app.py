import streamlit as st
import requests
import json

API_URL = "http://127.0.0.1:8001"

st.title("RegionPath — AI 취업 포트폴리오")
st.caption("대화형 인터뷰로 포트폴리오를 만들어드립니다")

# 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "stage" not in st.session_state:
    st.session_state.stage = "job"
if "data" not in st.session_state:
    st.session_state.data = {
        "target": {"job": "", "industry": "", "region": ""},
        "profile": {
            "education": "",
            "skills": [],
            "certificates": [],
            "projects": [],
            "activities": [],
            "training_history": []
        }
    }
if "portfolio" not in st.session_state:
    st.session_state.portfolio = None

# 첫 질문
if not st.session_state.messages:
    st.session_state.messages.append({
        "role": "assistant",
        "content": "안녕하세요! 저는 RegionPath AI입니다 😊\n희망 직무가 무엇인가요? (예: 백엔드 개발자, 데이터 분석가)"
    })

# 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 포트폴리오 완성 시 결과 출력
if st.session_state.portfolio:
    p = st.session_state.portfolio
    st.divider()
    st.subheader("📋 생성된 포트폴리오")
    st.info(p.get("portfolio_summary", ""))
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**💪 강점 태그**")
        for tag in p.get("strength_tags", []):
            st.success(tag)
    with col2:
        st.write("**🎯 NCS 태그**")
        for tag in p.get("ncs_tag_candidates", []):
            st.info(tag)
    
    st.warning(f"⚠️ 보완 필요: {p.get('weakness_hint', '')}")
    st.metric("포트폴리오 완성도", f"{int(p.get('completeness_score', 0) * 100)}%")
    
    if st.button("다시 시작"):
        st.session_state.messages = []
        st.session_state.stage = "job"
        st.session_state.data = {
            "target": {"job": "", "industry": "", "region": ""},
            "profile": {
                "education": "",
                "skills": [],
                "certificates": [],
                "projects": [],
                "activities": [],
                "training_history": []
            }
        }
        st.session_state.portfolio = None
        st.rerun()

# 입력창
if not st.session_state.portfolio:
    user_input = st.chat_input("메시지를 입력하세요...")
    
    if user_input:
        # 사용자 메시지 추가
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        stage = st.session_state.stage
        data = st.session_state.data
        next_msg = ""
        
        # 단계별 처리
        if stage == "job":
            data["target"]["job"] = user_input
            st.session_state.stage = "region"
            next_msg = f"'{user_input}' 직무를 희망하시는군요!\n희망 근무 지역이 어디인가요? (예: 충청권, 대전, 세종)"
        
        elif stage == "region":
            data["target"]["region"] = user_input
            st.session_state.stage = "industry"
            next_msg = "희망 산업 분야를 알려주세요. (예: IT 서비스, 제조, 금융)"
        
        elif stage == "industry":
            data["target"]["industry"] = user_input
            st.session_state.stage = "education"
            next_msg = "학력을 알려주세요. (예: 소프트웨어학과 재학, 컴퓨터공학과 졸업)"
        
        elif stage == "education":
            data["profile"]["education"] = user_input
            st.session_state.stage = "skills"
            next_msg = "보유한 기술 스택을 알려주세요. (예: Python, SQL, FastAPI)"
        
        elif stage == "skills":
            skills = [s.strip() for s in user_input.replace(",", " ").split()]
            data["profile"]["skills"] = skills
            st.session_state.stage = "certificates"
            next_msg = "보유한 자격증이 있나요? (없으면 '없음' 입력)"
        
        elif stage == "certificates":
            if user_input != "없음":
                data["profile"]["certificates"] = [user_input]
            st.session_state.stage = "projects"
            next_msg = "프로젝트 경험이 있나요? 프로젝트 이름을 알려주세요. (없으면 '없음' 입력)"
        
        elif stage == "projects":
            if user_input != "없음":
                data["profile"]["projects"] = [{"name": user_input, "tech_stack": data["profile"]["skills"]}]
            st.session_state.stage = "activities"
            next_msg = "대외활동이나 동아리 경험이 있나요? (없으면 '없음' 입력)"
        
        elif stage == "activities":
            if user_input != "없음":
                data["profile"]["activities"] = [user_input]
            st.session_state.stage = "generating"
            next_msg = "감사합니다! 포트폴리오를 생성하고 있어요... ⏳"
        
        # AI 응답 추가
        st.session_state.messages.append({
            "role": "assistant",
            "content": next_msg
        })
        
        # 포트폴리오 생성
        if st.session_state.stage == "generating":
            try:
                res = requests.post(f"{API_URL}/f01/generate", json=data)
                st.session_state.portfolio = res.json()
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"오류가 발생했어요: {e}"
                })
        
        st.rerun()
