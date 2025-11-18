from openrouter_client import call_llm


def generate_selenium_script(test_case_json, html_code):
    """
    Generates a runnable Selenium Python script based on
    test case + HTML DOM structure.
    """

    prompt = f"""
You are a Selenium Python automation expert.
Generate a *runnable* Selenium script.

Use ONLY the HTML provided.

HTML:
{html_code}

Test Case:
{test_case_json}

Requirements:
- Use Chrome webdriver
- Correct ID/name/CSS selectors
- Explicit waits
- Clear Pass/Fail print statements
- No placeholders—use real selectors from HTML.

Return ONLY Python code.
"""

    return call_llm(prompt)
