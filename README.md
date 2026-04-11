# 🔍 Multimodal Financial RAG System

A fully free and open-source Retrieval-Augmented Generation (RAG) system
for analyzing financial documents (Tesla reports) including text, tables,
and charts.

---

## 🧠 What This Does

- Ingests Tesla financial PDF reports
- Extracts text, tables, and chart descriptions
- Stores everything in a local vector database
- Answers financial questions with grounded, cited responses

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| PDF Processing | PyMuPDF, Unstructured OSS |
| Vision (Charts) | Google Gemini 1.5 Flash (free) |
| Embeddings | sentence-transformers (local) |
| Vector DB | ChromaDB (local) |
| LLM | Google Gemini 1.5 Flash (free) |
| API | FastAPI |

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd multimodal-financial-rag
```

### 2. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 5. Run the API
```bash
uvicorn app.api.main:app --reload
```

---

## 📁 Project Structure

multimodal-financial-rag/
├── app/
│   ├── ingestion/      # PDF processing pipeline
│   ├── processing/     # Chunking & metadata
│   ├── embeddings/     # Vector generation
│   ├── vectorstore/    # ChromaDB storage
│   ├── retrieval/      # RAG query pipeline
│   ├── llm/            # LLM abstraction
│   ├── vision/         # Vision model abstraction
│   └── api/            # FastAPI endpoints
├── config/             # Settings & configuration
├── data/               # Raw and processed data
├── tests/              # Unit & integration tests
├── scripts/            # Utility scripts
└── docs/               # Documentation

---

## 📖 Documentation

- [Architecture](docs/architecture.md)
- [Setup Guide](docs/setup.md)
- [API Reference](docs/api_reference.md)
- [Model Choices](docs/model_choices.md)

---

## ⚠️ Requirements

- Python 3.10+
- Google Gemini API key (free at makersuite.google.com)
- macOS / Linux / Windows