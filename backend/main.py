from fastapi import FastAPI, UploadFile
from parser import parse_document
from embeddings import embed_and_store
from test_case_agent import generate_test_cases
from script_gen import generate_selenium_script


from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global HTML storage
html_code = ""

@app.post("/upload")
async def upload_docs(files: list[UploadFile]):
    """
    Upload docs → parse → embed → store.
    If an HTML file is uploaded, store it separately for Selenium script generation.
    """
    global html_code

    for file in files:
        content = await file.read()
        text = parse_document(content, file.filename)

        if file.filename.endswith(".html"):
            html_code = text

        embed_and_store(text, {"source": file.filename})

    return {"status": "Knowledge Base Built"}

@app.post("/test-cases")
async def create_test_cases(query: str):
    return generate_test_cases(query)

@app.post("/script")
async def create_script(test_case: str):
    return generate_selenium_script(test_case, html_code)
