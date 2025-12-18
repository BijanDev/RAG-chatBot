import os
import dotenv

dotenv.load_dotenv()

PDF_FOLDER = "./uploaded_pdfs"
os.makedirs(PDF_FOLDER, exist_ok=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
