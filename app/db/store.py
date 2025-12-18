import json
import os
from datetime import datetime
from typing import Dict, Any


DB_DIR = os.path.dirname(__file__)
DB_FILE = os.path.join(DB_DIR, "projects.json")

os.makedirs(DB_DIR, exist_ok=True)

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({}, f)


PROJECTS_DB: Dict[str, Dict[str, Any]] = {}


def _serialize(obj):
    """Convert non-JSON types (datetime)"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj


def _deserialize_project(project: dict):
    """Convert ISO strings back to datetime"""
    if "created_at" in project and isinstance(project["created_at"], str):
        project["created_at"] = datetime.fromisoformat(project["created_at"])
    return project


def load_db():
    """Load projects from JSON file into memory"""
    global PROJECTS_DB

    if not os.path.exists(DB_FILE):
        PROJECTS_DB = {}
        return

    with open(DB_FILE, "r") as f:
        raw = json.load(f)

    PROJECTS_DB = {
        api_key: _deserialize_project(project)
        for api_key, project in raw.items()
    }


def save_db():
    """Persist in-memory DB to JSON file"""
    with open(DB_FILE, "w") as f:
        json.dump(
            PROJECTS_DB,
            f,
            default=_serialize,
            indent=2
        )

