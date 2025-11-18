import streamlit as st
import requests
import json

# Backend URL (FastAPI)
BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Autonomous QA Agent", layout="wide")

st.title("🤖 Autonomous QA Agent for Test Case & Selenium Script Generation")
st.write("Upload project documentation and generate test cases + runnable Selenium scripts.")

# --------------------------------------------------------
# SECTION 1 — File Upload & Knowledge Base Build
# --------------------------------------------------------

st.header("📁 Upload Support Documents + checkout.html")

uploaded_files = st.file_uploader(
    "Upload files (MD, TXT, PDF, JSON, HTML)",
    accept_multiple_files=True
)

if st.button("📚 Build Knowledge Base"):
    if not uploaded_files:
        st.warning("Please upload at least one file.")
    else:
        # Send files to backend
        files_to_send = []
        for f in uploaded_files:
            files_to_send.append(
                ("files", (f.name, f.read(), f"type"))
            )

        res = requests.post(f"{BACKEND_URL}/upload", files=files_to_send)

        if res.status_code == 200:
            st.success("Knowledge Base Built Successfully!")
        else:
            st.error("Failed to build knowledge base. Check backend logs.")


# --------------------------------------------------------
# SECTION 2 — Test Case Generation
# --------------------------------------------------------

st.header("🧠 Generate Test Cases")

user_query = st.text_input(
    "Enter feature query (e.g., 'Generate test cases for discount code')"
)

if st.button("📝 Generate Test Cases"):
    if not user_query:
        st.warning("Please enter a query.")
    else:
        res = requests.post(
            f"{BACKEND_URL}/test-cases",
            params={"query": user_query}
        )
        if res.status_code == 200:
            test_cases_output = res.json()
            st.subheader("Generated Test Cases")
            st.code(test_cases_output, language="json")

            st.session_state["last_test_cases"] = test_cases_output  
        else:
            st.error("Error generating test cases.")


# --------------------------------------------------------
# SECTION 3 — Selenium Script Generation
# --------------------------------------------------------

st.header("🧪 Generate Selenium Test Script")

test_case_input = st.text_area(
    "Paste one test case from the generated output (must be JSON)",
    placeholder='{\n   "Test_ID": "TC-001",\n   ...\n}'
)

if st.button("⚙ Generate Selenium Script"):
    if not test_case_input:
        st.warning("Please paste a test case JSON.")
    else:
        res = requests.post(
            f"{BACKEND_URL}/script",
            params={"test_case": test_case_input}
        )

        if res.status_code == 200:
            script = res.json()
            st.subheader("Generated Selenium Script")
            st.code(script, language="python")
        else:
            st.error("Error generating Selenium script.")
