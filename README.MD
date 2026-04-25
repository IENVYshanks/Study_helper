# Study Helper

Study Helper is a document-based learning assistant. Users upload PDF or text documents, then ask questions and receive answers grounded in the uploaded content.

## Backend Flow

1. User uploads a document.
   - PDF file
   - Text document
   - File is sent to the FastAPI backend

2. Backend receives the file.
   - Validate file type
   - Store the file temporarily or permanently
   - Create a document record

3. Extract text.
   - PDF: extract readable text
   - Text file: read content directly

4. Preprocess text.
   - Clean text
   - Remove extra spaces
   - Split text into chunks

5. Generate embeddings.
   - Convert each chunk into vector embeddings

6. Store chunks in a vector database.
   - Store chunk text
   - Store embedding
   - Store metadata:
     - User ID
     - Document ID
     - File name
     - Chunk number

7. User sends a chat query.
   - Query is sent to the FastAPI chat endpoint

8. Retrieve relevant chunks.
   - Convert the user query into an embedding
   - Search the vector database
   - Fetch the most relevant document chunks

9. Send context to the LLM.
   - Pass the user question and retrieved chunks to the chat model

10. Generate an answer.
    - LLM answers using the uploaded document context

11. Return the response.
    - FastAPI sends the generated answer back to the user

## Simple Flow

User uploads PDF/text -> FastAPI receives file -> extract text -> chunk text -> create embeddings -> store in vector DB -> user asks question -> retrieve relevant chunks -> send to LLM -> return answer.

## Project Structure

```text
app/
  api/
    routes/
      chat.py              # Chat endpoint
      documents.py         # Document upload endpoint
  core/
    config.py              # App settings
  models/
    chunk.py               # Chunk domain model
    document.py            # Document domain model
  schemas/
    chat.py                # Chat request/response schemas
    documents.py           # Document response schemas
  services/
    chat_service.py        # Query embedding, retrieval, answer generation
    document_service.py    # Upload processing pipeline
    embedding_service.py   # Local deterministic embedding service
    llm_service.py         # LLM answer generation adapter
    storage_service.py     # File storage
    text_extraction_service.py
    text_processing_service.py
    vector_store.py        # In-memory vector database
  main.py                  # FastAPI app entrypoint
```

## Run Locally

This project targets Python 3.14.

Create and activate a Python 3.14 virtual environment, then install dependencies:

```bash
python3.14 -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Open the interactive API docs:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Upload Document

```http
POST /api/documents/upload
```

Form fields:

- `file`: PDF or TXT document
- `user_id`: optional user ID, defaults to `demo-user`

### Chat

```http
POST /api/chat
```

Request body:

```json
{
  "question": "What is this document about?",
  "user_id": "demo-user",
  "document_id": "optional-document-id"
}
```

## Notes

The current implementation uses:

- Local file storage in `storage/uploads`
- In-memory vector storage
- Deterministic local embeddings for development
- A simple LLM adapter stub that returns retrieved context

For production, replace the embedding service, vector store, and LLM service with real providers such as OpenAI embeddings, Qdrant/Pinecone/Chroma/FAISS, and a chat model.
