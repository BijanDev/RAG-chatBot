from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
from datetime import datetime
from fastapi import Depends
from app.core.security import get_current_project
# from db.store import PROJECTS_DB, save_db
import app.db.store as store


router = APIRouter(prefix="/projects", tags=["Projects"])

# -------- Schemas --------
class RegisterWebsiteRequest(BaseModel):
    company_name: str
    site_name: str
    website_url: str
    company_size: Optional[str] = None  # e.g. 1-10, 10-50, 50-200
    industry: Optional[str] = None
    contact_email: Optional[EmailStr] = None

class RegisterWebsiteResponse(BaseModel):
    project_id: str
    api_key: str
    created_at: datetime

# -------- Helpers --------
def generate_api_key() -> str:
    return f"pk_live_{uuid.uuid4().hex}"

# -------- API --------
@router.post("/register", response_model=RegisterWebsiteResponse)
def register_website(data: RegisterWebsiteRequest):

    for existing in store.PROJECTS_DB.values():
        if any([
            existing.get("website_url") == data.website_url,
            existing.get("site_name") == data.site_name,
            existing.get("company_name") == data.company_name,
            existing.get("contact_email") == data.contact_email if data.contact_email else False
        ]):
            raise HTTPException(
                status_code=400,
                detail="Duplicate project detected."
            )



    project_id = str(uuid.uuid4())
    api_key = generate_api_key()

    store.PROJECTS_DB[api_key] = {
        "project_id": project_id,
        "company_name": data.company_name,
        "site_name": data.site_name,
        "website_url": data.website_url,
        "company_size": data.company_size,
        "industry": data.industry,
        "contact_email": data.contact_email,
        "created_at": datetime.utcnow(),
        "is_active": True
    }

    store.save_db()  # ✅ persist

    return {
        "project_id": project_id,
        "api_key": api_key,
        "created_at": store.PROJECTS_DB[api_key]["created_at"]
    }


# -------- Schema --------
class InitKeysRequest(BaseModel):
    gemini_api_key: str
    groq_api_key: str


# -------- Route --------
@router.post("/init-keys")
def init_keys(
    data: InitKeysRequest,
    project=Depends(get_current_project)
):
    api_key = project["api_key"]
    store.PROJECTS_DB[api_key]["gemini_key"] = data.gemini_api_key
    store.PROJECTS_DB[api_key]["groq_key"] = data.groq_api_key

    store.save_db()  # ✅ persist

    return {
        "message": "LLM keys saved successfully"
    }
