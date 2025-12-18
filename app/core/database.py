import chromadb
# from groq import Groq
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from core.config import GROQ_API_KEY, GOOGLE_API_KEY

# Groq client
# groq_client = Groq(api_key=GROQ_API_KEY)

# Chroma DB
chroma_client = chromadb.PersistentClient(path="./storage/chroma")
chroma_collection = chroma_client.get_or_create_collection(name="Company-Policy")


# Embedding model
# embeddings_model = GoogleGenerativeAIEmbeddings(
#     model="models/text-embedding-004",
#     task_type="retrieval_document",
#     google_api_key=GOOGLE_API_KEY
# )
