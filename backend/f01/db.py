import json, uuid
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = "./chroma_db"
COLLECTION  = "portfolios"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(
    collection_name=COLLECTION,
    embedding_function=embeddings,
    persist_directory=CHROMA_PATH
)

def save_portfolio(portfolio: dict) -> str:
    user_id = str(uuid.uuid4())
    text = (
        f"{portfolio.get('portfolio_summary', '')} "
        f"{' '.join(portfolio.get('strength_tags', []))} "
        f"{' '.join(portfolio.get('ncs_tag_candidates', []))}"
    )
    vectorstore.add_texts(
        texts=[text],
        metadatas=[{
            "user_id": user_id,
            "data": json.dumps(portfolio, ensure_ascii=False)
        }],
        ids=[user_id]
    )
    return user_id

def get_portfolio(user_id: str) -> dict | None:
    try:
        result = vectorstore.get(ids=[user_id])
        if result and result["metadatas"]:
            return json.loads(result["metadatas"][0]["data"])
        return None
    except Exception:
        return None
