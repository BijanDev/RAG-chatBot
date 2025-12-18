# Back4App Access Information

## 🌐 Your App URLs

### Parse REST API Endpoint (Main Access)
**Base URL:** `https://parseapi.back4app.com`

This is how you access your Parse Cloud Functions.

### Web Hosting URL
**Preview URL:** `https://preview-ragchatbot-tlcbhz.b4a.app`
- ⚠️ **Note:** This is a preview URL that expires on: 2025-12-18T06:59:15.535Z
- For a permanent URL, you'll need to configure a custom domain in Back4App dashboard

---

## 🔑 Your App Credentials

```
Application ID: RHgQk1lCAS2mybB5ZLa7OPaMsFv3g2mpFECwQ7RC
REST API Key:   hjXlrBPIDj4iH5WoYNTd4DKYC5GSmi4g8km7j2HM
Master Key:     FeZyWrL0kJvBXDS4jDdnTPoymFyuLGcwjQztjDTJ
JavaScript Key: s7HLsTZfixH6etBX8Bz9SJNZ0JrmT863JBs0ystF
```

---

## 📡 How to Access Your Cloud Functions

### 1. Register a New Project
```bash
curl -X POST https://parseapi.back4app.com/functions/registerWebsite \
  -H "X-Parse-Application-Id: RHgQk1lCAS2mybB5ZLa7OPaMsFv3g2mpFECwQ7RC" \
  -H "X-Parse-REST-API-Key: hjXlrBPIDj4iH5WoYNTd4DKYC5GSmi4g8km7j2HM" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Acme Corp",
    "site_name": "Acme Policy Bot",
    "website_url": "https://acme.org",
    "company_size": "10-50",
    "industry": "SaaS",
    "contact_email": "admin@acme.com"
  }'
```

### 2. Initialize API Keys
```bash
curl -X POST https://parseapi.back4app.com/functions/initKeys \
  -H "X-Parse-Application-Id: RHgQk1lCAS2mybB5ZLa7OPaMsFv3g2mpFECwQ7RC" \
  -H "X-Parse-REST-API-Key: hjXlrBPIDj4iH5WoYNTd4DKYC5GSmi4g8km7j2HM" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "pk_live_YOUR_API_KEY",
    "gemini_api_key": "YOUR_GEMINI_KEY",
    "groq_api_key": "YOUR_GROQ_KEY"
  }'
```

### 3. Chat (Ask Questions)
```bash
curl -X POST https://parseapi.back4app.com/functions/chat \
  -H "X-Parse-Application-Id: RHgQk1lCAS2mybB5ZLa7OPaMsFv3g2mpFECwQ7RC" \
  -H "X-Parse-REST-API-Key: hjXlrBPIDj4iH5WoYNTd4DKYC5GSmi4g8km7j2HM" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "pk_live_YOUR_API_KEY",
    "question": "What is the vacation policy?"
  }'
```

### 4. List PDFs
```bash
curl -X POST https://parseapi.back4app.com/functions/listPdfs \
  -H "X-Parse-Application-Id: RHgQk1lCAS2mybB5ZLa7OPaMsFv3g2mpFECwQ7RC" \
  -H "X-Parse-REST-API-Key: hjXlrBPIDj4iH5WoYNTd4DKYC5GSmi4g8km7j2HM" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "pk_live_YOUR_API_KEY"
  }'
```

### 5. Upload PDF
```bash
curl -X POST https://parseapi.back4app.com/functions/uploadPdf \
  -H "X-Parse-Application-Id: RHgQk1lCAS2mybB5ZLa7OPaMsFv3g2mpFECwQ7RC" \
  -H "X-Parse-REST-API-Key: hjXlrBPIDj4iH5WoYNTd4DKYC5GSmi4g8km7j2HM" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "pk_live_YOUR_API_KEY",
    "pdf_name": "policy-document",
    "file": {
      "name": "policy.pdf",
      "data": "BASE64_ENCODED_FILE_DATA",
      "contentType": "application/pdf"
    }
  }'
```

---

## 🌍 Back4App Dashboard

Access your app dashboard at:
**https://www.back4app.com/dashboard**

Login and navigate to your "RAG ChatBot" app to:
- View logs
- Monitor usage
- Configure settings
- Manage data
- Set up custom domain for web hosting

---

## 📝 Important Notes

1. **Parse Cloud Functions** are accessed via the Parse REST API endpoint (`https://parseapi.back4app.com/functions/...`)

2. **Web Hosting** is for static files/web apps. To deploy a frontend, you would use the web hosting feature.

3. **RAG Service**: Remember that the chat function currently needs your Python RAG service to be running separately. Update the `chat` function in `cloud/main.js` to call your Python service URL.

4. **Security**: Never expose your Master Key in client-side code. Use REST API Key for client requests.

---

## 🧪 Test Your Deployment

Quick test to verify your cloud functions are working:

```bash
curl -X POST https://parseapi.back4app.com/functions/registerWebsite \
  -H "X-Parse-Application-Id: RHgQk1lCAS2mybB5ZLa7OPaMsFv3g2mpFECwQ7RC" \
  -H "X-Parse-REST-API-Key: hjXlrBPIDj4iH5WoYNTd4DKYC5GSmi4g8km7j2HM" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Test Company",
    "site_name": "Test Site",
    "website_url": "https://test.com"
  }'
```

If successful, you'll receive a response with `project_id` and `api_key`.

