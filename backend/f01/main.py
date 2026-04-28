from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import chat, clear_session
import uuid

app = FastAPI()

class ChatRequest(BaseModel):
    session_id: str | None = None  # 없으면 새 세션 시작
    message: str

class ChatResponse(BaseModel):
    session_id: str
    status: str          # "in_progress" | "complete"
    message: str
    portfolio: dict | None = None

@app.post("/f01/chat", response_model=ChatResponse)
def f01_chat(req: ChatRequest):
    # 세션 ID 없으면 새로 발급
    session_id = req.session_id or str(uuid.uuid4())
    
    try:
        result = chat(session_id, req.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return ChatResponse(
        session_id=session_id,
        status=result["status"],
        message=result["message"],
        portfolio=result.get("portfolio")
    )

@app.delete("/f01/session/{session_id}")
def delete_session(session_id: str):
    clear_session(session_id)
    return {"message": "세션 삭제 완료"}

# 기존 엔드포인트 — F-02 연동용으로 유지
@app.get("/f01/portfolio/{session_id}")
def get_portfolio(session_id: str):
    """F-02가 호출해서 포트폴리오 가져가는 엔드포인트"""
    # TODO: Chroma DB 연동 후 저장된 포트폴리오 반환
    return {"message": "추후 Chroma DB 연동 예정", "session_id": session_id}
