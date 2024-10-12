import json
import os
import re

import google.generativeai as genai
from dotenv import load_dotenv


def gemini_llm(question):
    prompt = f"""
    사용자 질문: "{question}"
주의사항:
- 한국어로 답해주세요

"""

    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    llm_model = genai.GenerativeModel("gemini-1.5-flash")
    response = llm_model.generate_content(prompt)
    return response if isinstance(response, str) else response.text


def gemini_llm(question):
    prompt = f"""
    사용자 질문: "{question}"
사용자가 장소를 물어보면 장소에 대한 정보와 위치를 알려주세요
주의사항:
- 한국어로 답해주세요

결과는 아래 JSON 형식으로 출력해주세요:
{{
    "answer": "장소에 대한 설명",
    "location": "사용자가 물어본 장소의 주소. 없으면 null",
}}
"""

    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    llm_model = genai.GenerativeModel("gemini-1.5-flash")
    response = llm_model.generate_content(prompt)
    if isinstance(response, str):
        response_text = response
    elif hasattr(response, "text"):
        response_text = response.text
    else:
        print("LLM 응답에서 문자열을 추출할 수 없습니다.")
        return None, None

    json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
    if json_match:
        json_text = json_match.group(0)
        try:
            extracted_data = json.loads(json_text)

            answer = extracted_data.get("answer", None)
            location = extracted_data.get("location", None)

            return answer, location
        except json.JSONDecodeError:
            print("JSON 파싱에 실패했습니다.")
            return None, None
    else:
        print("LLM 응답에서 JSON을 찾지 못했습니다.")
        return None, None
