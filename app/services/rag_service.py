import os
import shutil
import uuid
from datetime import datetime
from fastapi import UploadFile, HTTPException
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from core.config import PDF_FOLDER
from core.database import chroma_collection
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from groq import Groq


def get_embeddings_model(GOOGLE_API_KEY):
    return GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        task_type="retrieval_document",
        google_api_key=GOOGLE_API_KEY
    )

def get_file_info(file_path):
    """Helper to get file size and modified date."""
    try:
        # Get size
        size_bytes = os.path.getsize(file_path)
        if size_bytes >= 1024 * 1024:
            size_str = f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            size_str = f"{size_bytes / 1024:.0f} KB"
        
        # Get modification time
        mtime = os.path.getmtime(file_path)
        date_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
        return size_str, date_str
    except FileNotFoundError:
        return "Unknown", "Unknown"
    

async def save_and_process_pdf(file: UploadFile, pdf_name: str, project):
    # Save uploaded file
    pdf_path = os.path.join(PDF_FOLDER, file.filename)
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Load & process
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)

    all_texts = [doc.page_content for doc in chunks]

    batch_size = 20 
    total_chunks = len(all_texts)

    print(f"Processing {total_chunks} chunks for {pdf_name}...")
    
    for i in range(0, total_chunks, batch_size):
        # Get batch of texts
        batch_texts = all_texts[i : i + batch_size]

        # Embedding model
        embeddings_model = get_embeddings_model(project["gemini_key"])
        
        # Embed this batch (Send to Google)
        batch_vectors = embeddings_model.embed_documents(batch_texts)
        
        # Create IDs and Metadata for this batch
        batch_ids = [str(uuid.uuid4()) for _ in range(len(batch_texts))]
        # batch_metadata = [{"source": pdf_name} for _ in range(len(batch_texts))]
        batch_metadata = [
            {
                "source": pdf_name,
                "project_id": project["project_id"]
            }
            for _ in range(len(batch_texts))
        ]


        # Store in Chroma
        chroma_collection.add(
            ids=batch_ids,
            documents=batch_texts,
            embeddings=batch_vectors,
            metadatas=batch_metadata
        )
        print(f"Processed batch {i} to {i+len(batch_texts)}")
    
    return total_chunks

    

def query_llm(question: str, project):
    # Query embedding
    embeddings_model = get_embeddings_model(project["gemini_key"])
    query_embedding = embeddings_model.embed_query(question)
    groq_key = project["groq_key"]

    # Retrieve only documents belonging to this PDF
    result = chroma_collection.query(
        query_embeddings=query_embedding,
        n_results=5,
        where={
            "project_id": project["project_id"]
        }
    )

    context_docs = result["documents"][0]
    context_str = "\n\n".join(context_docs)

    groq_client = Groq(api_key=groq_key)

    # Build prompt
    prompt = f"""
    You are a dedicated AI assistant for Company Policy. You must answer the user's question using ONLY the provided context text below.
    
    CRITICAL INSTRUCTIONS:
    1. Answer strictly based on the provided Context.
    2. Do NOT use any outside knowledge, common sense, or information not present in the Context.
    3. If the answer is not explicitly stated in the Context, you MUST say: "I cannot answer this based on the provided document."
    4. **Be extremely precise with numbers, dates, and conditions. Do not round up or simplify limits (e.g., if the text says "less than 10", do not say "10").**
    5. Do not speculate or make up information.
    6. Keep your answer concise and direct.
    7. If the question is Hello, Hii, Hey etc., you can reply with a simple "Hello! How can I help you?"
    8. If the question is Thank you, you can reply with a simple "You're welcome!"

    # CONTEXT:
    {context_str}
    
    QUESTION:
    {question}

    ANSWER:
    """

    # Call Groq LLM
    completion = groq_client.chat.completions.create(
        model="moonshotai/kimi-k2-instruct-0905",  # Your chosen model
        messages=[
            {"role": "system", "content": "Answer strictly from the policy document."},
            {"role": "user", "content": prompt}
        ]
    )

    answer = completion.choices[0].message.content
    return answer
