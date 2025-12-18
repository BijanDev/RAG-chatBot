# Back4App Deployment Guide

This project has been adapted for Back4App deployment. However, there are important considerations:

## Architecture

The FastAPI application has been converted to Parse Cloud Functions. However, the RAG (Retrieval-Augmented Generation) functionality using ChromaDB, LangChain, and Python ML libraries requires special handling.

## Components

### 1. Parse Cloud Functions (`cloud/main.js`)
- `registerWebsite` - Register new projects
- `initKeys` - Initialize API keys for projects
- `uploadPdf` - Upload PDF files (stored in Parse Files)
- `listPdfs` - List PDFs for a project
- `deletePdf` - Delete PDFs
- `chat` - Chat/RAG endpoint (requires external service)

### 2. Parse Classes
The following Parse classes will be created automatically:
- **Project** - Stores project information and API keys
- **PDF** - Stores PDF metadata and file references

## Important Notes

### RAG Service Limitation
The RAG functionality (PDF processing, ChromaDB indexing, embeddings, LLM queries) uses Python-specific libraries:
- ChromaDB
- LangChain
- Google Generative AI
- Groq

These cannot run directly in Parse Cloud Code (Node.js). You have two options:

#### Option 1: External Python Service (Recommended)
Keep your FastAPI service running separately (e.g., on Heroku, Railway, or another Python hosting service) and call it from Parse Cloud Functions.

Update the `chat` function in `cloud/main.js` to call your Python service:

```javascript
Parse.Cloud.define("chat", async (request) => {
  const { api_key, question } = request.params;
  const project = await getProjectByApiKey(api_key);

  const response = await Parse.Cloud.httpRequest({
    url: 'https://your-python-service.com/chat',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${api_key}`
    },
    body: JSON.stringify({
      question: question
    })
  });

  return JSON.parse(response.text);
});
```

#### Option 2: Migrate to JavaScript
Rewrite the RAG logic using JavaScript equivalents:
- Use a JavaScript vector database (e.g., Pinecone, Weaviate)
- Use JavaScript LLM libraries
- This requires significant refactoring

## Deployment Steps

1. **Deploy Cloud Code to Back4App:**
   ```bash
   # The deployment will be done via Back4App MCP tools
   ```

2. **Migrate Existing Data:**
   - Your existing `projects.json` data needs to be migrated to Parse Objects
   - Use the Back4App dashboard or a migration script

3. **Configure Environment:**
   - Set up Parse classes (Project, PDF) in Back4App dashboard
   - Configure file storage settings

4. **Set up External RAG Service (if using Option 1):**
   - Deploy your FastAPI service separately
   - Update the `chat` function to call it

## API Usage

After deployment, use Parse REST API or SDK:

### Register Project
```bash
curl -X POST https://parseapi.back4app.com/functions/registerWebsite \
  -H "X-Parse-Application-Id: YOUR_APP_ID" \
  -H "X-Parse-REST-API-Key: YOUR_REST_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Acme Corp",
    "site_name": "Acme Policy Bot",
    "website_url": "https://acme.org"
  }'
```

### Chat
```bash
curl -X POST https://parseapi.back4app.com/functions/chat \
  -H "X-Parse-Application-Id: YOUR_APP_ID" \
  -H "X-Parse-REST-API-Key: YOUR_REST_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "pk_live_...",
    "question": "What is the vacation policy?"
  }'
```

## Next Steps

1. Deploy the cloud code to Back4App
2. Migrate existing project data
3. Set up the external RAG service or adapt the RAG logic to JavaScript
4. Test all endpoints


