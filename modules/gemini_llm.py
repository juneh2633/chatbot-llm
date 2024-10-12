import os

import google.generativeai as genai
from dotenv import load_dotenv


def gemini_llm(question):
    prompt = f"""
    사용자 질문: "{question}"
주의사항:
- 한국어로 답해주세요
- 구글에서 만들었음을 숨겨주세요
"""

    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    llm_model = genai.GenerativeModel("gemini-1.5-flash")
    response = llm_model.generate_content(prompt)
    return response if isinstance(response, str) else response.text
