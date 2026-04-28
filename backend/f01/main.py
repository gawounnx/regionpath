from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
from agent import generate_portfolio_with_llm
from ncs_mapper import get_ncs_tags, get_ncs_detail
from db import save_portfolio, get_portfolio

load_dotenv()
app = FastAPI(title="RegionPath F-01 API", version="1.0.0")

class Project(BaseModel):
    name: str
    tech_stack: List[str] = []
    description: Optional[str] = ""

class Profile(BaseModel):
    education: Optional[str] = ""
    skills: List[str] = []
    certificates: List[str] = []
    projects: List[Project] = []
    activities: List[str] = []
    training_history: List[str] = []

class Target(BaseModel):
    job: str
    industry: Optional[str] = ""
    region: Optional[str] = ""

class PortfolioRequest(BaseModel):
    target: Target
    profile: Profile

@app.post("/f01/generate")
def generate_portfolio(data: PortfolioRequest):
    try:
        job      = data.target.job
        industry = data.target.industry or ""
        region   = data.target.region or ""

        llm_result = generate_portfolio_with_llm(
            job=job, industry=industry, region=region,
            profile=data.profile.model_dump()
        )

        ncs_tags = get_ncs_tags(job, data.profile.skills)

        f02_projects = [
            {"name": p.name, "tech_stack": p.tech_stack}
            for p in data.profile.projects
        ]

        portfolio = {
            "portfolio_summary":  llm_result["portfolio_summary"],
            "strength_tags":      llm_result["strength_tags"],
            "weakness_hint":      llm_result.get("weakness_hint", ""),
            "completeness_score": (
            (0.25 if data.profile.skills else 0) +
            (0.25 if data.profile.certificates else 0) +
            (0.25 if data.profile.projects else 0) +
            (0.25 if data.profile.education else 0)
             ),
            "skill_tags":         data.profile.skills,
            "ncs_tag_candidates": ncs_tags,
            "next_step_for_f02": {
                "target_job":         job,
                "target_industry":    industry,
                "target_region":      region,
                "skills":             data.profile.skills,
                "certificates":       data.profile.certificates,
                "projects":           f02_projects,
                "ncs_tag_candidates": ncs_tags,
                "weakness_hint":      llm_result.get("weakness_hint", "")
            }
        }

        user_id = save_portfolio(portfolio)
        portfolio["user_id"] = user_id

        return portfolio

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/f01/portfolio/{user_id}")
def get_user_portfolio(user_id: str):
    result = get_portfolio(user_id)
    if not result:
        raise HTTPException(status_code=404, detail="포트폴리오를 찾을 수 없습니다.")
    return result

@app.get("/f01/ncs/{job}")
def get_ncs_info(job: str):
    result = get_ncs_detail(job)
    if not result:
        return {"message": "검색 결과 없음", "data": []}
    return {"data": result}

@app.get("/f01/health")
def health_check():
    return {"status": "ok", "service": "F-01 Portfolio Generator"}
