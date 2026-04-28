from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
import json, os

SYSTEM_PROMPT = """
당신은 비수도권 청년 구직자의 취업 포트폴리오를 만들어주는 AI 인터뷰어입니다.

아래 항목들을 자연스러운 대화로 순서대로 수집하세요:
1. 희망 직무 (job)
2. 희망 지역 (region)  
3. 보유 기술 스택 (skills)
4. 자격증 (certificates)
5. 프로젝트 경험 (projects)
6. 국비훈련 이수 이력 (training_history)

모든 항목 수집이 완료되면 반드시 아래 형식의 JSON을 출력하세요:
[PORTFOLIO_COMPLETE]
{
  "profile": {
    "job": "",
    "region": "",
    "skills": [],
    "certificates": [],
    "projects": [{"name": "", "tech_stack": []}],
    "training_history": []
  },
  "ncs_tags": [],
  "portfolio_summary": "",
  "strength_tags": [],
  "completeness_score": 0.0
}

ncs_tags는 직무에 맞는 NCS 능력단위명으로 채우세요. (예: 응용SW엔지니어링, 데이터베이스)
completeness_score는 0.0~1.0 사이로, 항목 충실도에 따라 채우세요.
아직 수집 중이면 자연스럽게 다음 질문을 이어가세요.
"""

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# 세션별 메모리 저장소
session_memories: dict[str, ConversationBufferMemory] = {}

def get_or_create_memory(session_id: str) -> ConversationBufferMemory:
    if session_id not in session_memories:
        session_memories[session_id] = ConversationBufferMemory(
            return_messages=True
        )
    return session_memories[session_id]

def chat(session_id: str, user_message: str) -> dict:
    memory = get_or_create_memory(session_id)
    
    chain = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=False
    )
    
    # 첫 메시지면 시스템 프롬프트 주입
    if len(memory.chat_memory.messages) == 0:
        full_message = SYSTEM_PROMPT + "\n\n사용자: " + user_message
    else:
        full_message = user_message
    
    response = chain.predict(input=full_message)
    
    # 포트폴리오 완성 여부 체크
    if "[PORTFOLIO_COMPLETE]" in response:
        try:
            json_str = response.split("[PORTFOLIO_COMPLETE]")[1].strip()
            portfolio_data = json.loads(json_str)
            return {
                "status": "complete",
                "message": response.split("[PORTFOLIO_COMPLETE]")[0].strip(),
                "portfolio": portfolio_data
            }
        except json.JSONDecodeError:
            pass
    
    return {
        "status": "in_progress",
        "message": response,
        "portfolio": None
    }

def clear_session(session_id: str):
    if session_id in session_memories:
        del session_memories[session_id]
