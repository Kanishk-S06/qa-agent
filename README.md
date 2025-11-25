# 🧪 AI-Powered QA Assistant  
### Automated Test Case Generator, RAG-based Validator, and Selenium Script Generator

This project implements an **AI-driven Quality Assurance Assistant** capable of:
- Extracting information from uploaded files (PDF, text, HTML)
- Running **Retrieval-Augmented Generation (RAG)** for grounded answers  
- Automatically generating **structured test cases**
- Generating **Selenium Python scripts** for UI automation
- Answering technical questions based strictly on indexed project files

The system uses **FastAPI** for the backend, **Sentence Transformers** for embeddings, **ChromaDB** for vector search, and OpenRouter for LLM calls.

---

## 📌 **Features**

### 🔍 1. Document Ingestion & Parsing
Upload documents (PDF, HTML, text).  
The backend:
- Extracts text using **PyMuPDF**, BeautifulSoup, and custom parsing logic.
- Splits content into chunks.
- Creates **embeddings using Sentence Transformers**.
- Stores them in **ChromaDB** for retrieval.

### 🧠 2. Retrieval-Augmented Generation (RAG)
Queries are answered using:
- Semantic search over embedded documents
- Context-aware LLM responses  
- Strict grounding (no hallucinations)

### 📝 3. AI-Generated Test Cases
Given a query such as:
> “Generate test cases for login module”

The system retrieves context and returns JSON-formatted test cases:
```json
[
  {
    "Test_ID": "TC-001",
    "Feature": "Login",
    "Scenario": "Valid login",
    "Steps": ["Open page", "Enter credentials", "Click Login"],
    "Expected": "User is redirected",
    "Grounded_In": "Source paragraph..."
  }
]
```

### 🧪 4. Selenium Script Generator
Given test case JSON + HTML DOM:
- Creates **fully runnable Selenium Python scripts**
- Uses explicit waits
- Uses real selectors
- No placeholder code

### 🤖 5. Test Case to Script Pipeline
Your `test_case_agent.py` builds the pipeline:
```
Query → RAG → Test Case JSON → Selenium Script
```

---

# 📂 **Project Structure**

```
backend/
│── main.py                 # FastAPI server
│── embeddings.py           # Embedding + storage logic
│── rag.py                  # RAG pipeline
│── parser.py               # PDF/HTML/text extractors
│── openrouter_client.py    # LLM API wrapper
│── script_gen.py           # Selenium script generator
│── test_case_agent.py      # Full test case generation workflow
│── requirements.txt
```

---

# ⚙️ **Installation**

### **1. Install dependencies**
(Use Python 3.9–3.10 if possible)

```bash
pip install -r requirements.txt
```

### **2. Add your API key**
Create a `.env` file:

```
OPENROUTER_API_KEY=your_key_here
```

---

# ▶️ **Running the Backend**

```bash
python -m uvicorn main:app --reload
```

Backend runs at:
```
http://127.0.0.1:8000
```

---

# 🔧 **Core Files Explained**

## **1. embeddings.py**
- Loads SentenceTransformer model  
- Embeds text chunks  
- Stores them into ChromaDB  
- Used during both upload & query  
*(file automatically cited from user input)*

## **2. parser.py**
- Extracts text from:
  - PDFs (PyMuPDF)
  - HTML (BeautifulSoup)
  - Plain text files
- Cleans + normalizes content

## **3. rag.py**
- Performs semantic search  
- Returns **context** for LLM grounding  
- Powers test-case generation & question answering

## **4. openrouter_client.py**
- Wraps OpenRouter API calls  
- Ensures consistent model + headers  
- Used across all generators

## **5. script_gen.py**
Generates fully runnable Selenium Python scripts using:
- Explicit waits  
- ChromeDriver  
- Real selectors from provided HTML  
- Pass/Fail logs

## **6. test_case_agent.py**
Pipeline:
1. Retrieve context  
2. Generate test cases  
3. Validate grounding  
4. Produce Selenium scripts  

---

# 🧪 **API Endpoints**

### **Upload File**
```
POST /upload
```

### **Ask a Question (RAG Q&A)**
```
POST /ask
```

### **Generate Test Cases**
```
POST /generate-testcase
```

### **Generate Selenium Script**
```
POST /generate-script
```

---

# 🎥 **Video Demo Guidelines (15 minutes max)**

Suggested flow:
1. **Introduction** (1 min)  
2. **Folder structure walkthrough** (1–2 min)  
3. **Backend architecture overview** (2 min)  
4. **Workflow demo**  
   - Upload → Embedding → Query → Test Cases → Script (6–7 min)  
5. **Show code highlights** (2–3 min)  
6. **If deployed, show live deployment** (optional)  
7. **Outro + summary** (30 sec)

---

# 🚀 **Future Enhancements**
- Add auth for uploaded files  
- Add UI test runner  
- Add support for multi-file cross-linking  
- Add model selection in UI  

---

# 📜 **License**
MIT License

