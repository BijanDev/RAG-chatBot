from fastapi import Header, HTTPException, Depends
# from db.store import PROJECTS_DB
import db.store as store


def get_current_project(authorization: str = Header(...)):
    """
    Extracts API key from Authorization header and
    returns the associated project.
    """
    # print(authorization)

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid Authorization header format"
        )

    api_key = authorization.replace("Bearer ", "").strip()

    project = store.PROJECTS_DB.get(api_key)
    
    if not project:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if not project.get("is_active", True):
        raise HTTPException(status_code=403, detail="API key inactive")

    # ✅ attach api_key so downstream code knows it
    project["api_key"] = api_key

    return project
