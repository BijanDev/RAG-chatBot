import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from core.config import PDF_FOLDER
from core.database import chroma_collection
from services.rag_service import save_and_process_pdf, get_file_info
from core.security import get_current_project

router = APIRouter()

@router.post("/upload_pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    project=Depends(get_current_project)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    pdf_name = file.filename.replace(".pdf", "")

    # Check if this name already exists in DB
    # existing_ids = chroma_collection.get(where={"source": pdf_name})
    existing_ids = chroma_collection.get(
        where={
            # "source": pdf_name,
            "project_id": project["project_id"]
        }
    )

    if len(existing_ids["ids"]) > 0:
        raise HTTPException(status_code=400, detail="PDF with this name already exists.")

    total_chunks = await save_and_process_pdf(file, pdf_name, project)

    return {
        "message": "PDF uploaded and indexed successfully.", 
        "pdf_name": pdf_name, 
        "total_chunks": total_chunks
    }


@router.delete("/delete_pdf/{pdf_name}")
async def delete_pdf(
    pdf_name: str,
    project=Depends(get_current_project)
):
    project_id = project["project_id"]

    where_clause = {
        "$and": [
            {"source": pdf_name},
            {"project_id": project_id}
        ]
    }

    # Check if PDF exists for THIS project only
    existing = chroma_collection.get(where=where_clause)

    if not existing["ids"]:
        raise HTTPException(
            status_code=404,
            detail="PDF not found for this project."
        )

    

    # Delete embeddings ONLY for this project
    chroma_collection.delete(
        where=where_clause
    )

    # Optionally delete file (only if no other project uses it)
    pdf_file_path = os.path.join(PDF_FOLDER, f"{pdf_name}.pdf")
    if os.path.exists(pdf_file_path):
        os.remove(pdf_file_path)

    return {
        "message": f"PDF '{pdf_name}' deleted successfully."
    }


@router.post("/reupload_pdf")
async def reupload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    pdf_name = file.filename.replace(".pdf", "")

    # Delete old records if exist
    existing = chroma_collection.get(where={"source": pdf_name})
    if len(existing["ids"]) > 0:
        chroma_collection.delete(where={"source": pdf_name})

    total_chunks = await save_and_process_pdf(file, pdf_name)

    return {"message": "PDF reuploaded and reindexed successfully.", "pdf_name": pdf_name}



@router.get("/list_pdfs")
def list_pdfs(project=Depends(get_current_project)):
    project_id = project["project_id"]

    results = chroma_collection.get(
        where={"project_id": project_id}
    )

    pdfs = {}

    for metadata in results.get("metadatas", []):
        pdf_name = metadata.get("source")
        if not pdf_name:
            continue

        if pdf_name not in pdfs:
            file_path = os.path.join(PDF_FOLDER, f"{pdf_name}.pdf")
            size, date = get_file_info(file_path)

            pdfs[pdf_name] = {
                "filename": pdf_name,
                "size": size,
                "date": date
            }

    return {
        "pdfs": sorted(
            pdfs.values(),
            key=lambda x: x["date"],
            reverse=True
        )
    }

