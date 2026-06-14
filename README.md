# Python Programming Q&A Assistant

## Overview

This project is a Python Programming Q&A Assistant built using a Retrieval-Augmented Generation (RAG) pipeline. It answers Python-related questions by retrieving relevant information from a Stack Overflow Python Q&A dataset and generating grounded responses using the Grok (xAI) API.

## Tech Stack

* Python
* FastAPI
* LangChain
* ChromaDB
* Grok (xAI)
* Pydantic
* ngrok (for public deployment)

## Dataset

Stack Overflow - Python Questions & Answers

https://www.kaggle.com/datasets/stackoverflow/pythonquestions

## Project Structure

```text
Python-QA-Assistant/
├── main.py
├── rag_pipeline.py
├── data_loader.py
├── requirements.txt
├── README.md
├── test_results.md
├── .env.example
└── chroma_db/
```

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd Python-QA-Assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file

```env
GROQ_API_KEY=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
```

### 4. Run the application

```bash
uvicorn main:app --reload
```

## Deployment

The application has been deployed using ngrok and is publicly accessible at:

**https://oppressive-meryl-unsummable.ngrok-free.dev**

### API Documentation (Swagger UI)

**Local:**

```text
http://127.0.0.1:8000/docs
```

**Deployed:**

```text
https://oppressive-meryl-unsummable.ngrok-free.dev/docs
```

## API Endpoints

### GET /health

Response:

```json
{
  "status": "healthy"
}
```

### POST /ask

Request:

```json
{
  "question": "What is a Python list?"
}
```

## Testing

The API was tested using 8 different queries, including:

* Python programming questions
* Invalid inputs
* Edge cases
* Out-of-domain queries

Results are available in `test_results.md`.

## Future Improvements

* Source citations
* Better retrieval strategies
* Conversation memory
* Docker deployment
* Authentication and rate limiting
* Cloud deployment (AWS/Azure/GCP)

## Author

**Suryansh Ujjwal**
