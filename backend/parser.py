import json
import fitz
from bs4 import BeautifulSoup

def parse_document(file_bytes, filename):
    """
    Extracts text from MD, TXT, PDF, JSON, HTML documents.
    Used for building knowledge base.
    """
    ext = filename.split(".")[-1].lower()

    # Plain text or markdown
    if ext in ["txt", "md"]:
        return file_bytes.decode("utf-8")

    # JSON
    if ext == "json":
        data = json.loads(file_bytes.decode("utf-8"))
        return json.dumps(data, indent=2)

    # PDF
    if ext == "pdf":
        text = ""
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text()
        return text

    # HTML
    if ext == "html":
        soup = BeautifulSoup(file_bytes, "lxml")
        return soup.prettify()

    return ""
