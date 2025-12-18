from fastapi import APIRouter
from services.rag_service import query_llm
from core.security import get_current_project
from fastapi import Depends
from pydantic import BaseModel

router = APIRouter()


class QuestionRequest(BaseModel):
    question: str


@router.post("/chat")
def ask_question(data: QuestionRequest, project=Depends(get_current_project)):
    question = data.question
    answer = query_llm(question, project)

    return {
        "question": question,
        "answer": answer
    }
