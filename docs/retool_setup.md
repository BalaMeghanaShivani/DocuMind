# 🛠️ DocuMind Retool Admin Dashboard

This guide explains how to build an internal admin dashboard for DocuMind using **Retool**.

## 1. Setup Resources

### A. Connect DocuMind API
1. Go to **Resources** > **Create New** > **REST API**.
2. **Name:** `DocuMind API`
3. **Base URL:** `http://localhost:8000` (or your deployed backend URL).
   - *Note: If running locally, you may need to use `host.docker.internal` or ngrok.*
4. **Headers:** None required for this hackathon version.

### B. Connect Sanity GraphQL
1. Go to **Resources** > **Create New** > **GraphQL**.
2. **Name:** `DocuMind Sanity`
3. **Base URL:** `https://<YOUR_PROJECT_ID>.api.sanity.io/v1/graphql/production/default`
4. **Authorization:** Bearer Token (use your `SANITY_TOKEN`).

---

## 2. Build with Retool Assist 🤖

Use **Retool Assist** (the AI helper) to generate components instantly. Paste these prompts into the chat window:

### 🧩 Documents Table
> "Create a table component that lists all documents. Use a REST query to GET /documents called 'getDocuments'. Add columns for Title, Doc Type, Status, and Created At. Add a text input to filter the table by title."

### 📝 JSON Explorer
> "Add a JSON Explorer component to the right of the table. When a row is selected in the table, show the 'structured_data' field of the selected row in this explorer."

### 📄 PDF Preview
> "Add a PDF Viewer component below the JSON Explorer. Bind its file source to the 'pdf_path' of the selected row in the table."

### 🔄 Action Buttons
> "Add a button 'Regenerate PDF' above the table. When clicked, trigger a POST request to '/process-text' using the selected row's raw text (if available) or trigger a re-run of the generation pipeline."
