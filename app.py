import datetime

import streamlit as st

from modules.gemini_llm import gemini_llm


def log_interaction(user_input, response):
    with open("chat_log.txt", "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] User: {user_input}\n")
        log_file.write(f"[{timestamp}] Bot: {response}\n\n")


st.title("챗봇")
st.write("질문을 입력해 보세요!")


user_input = st.text_input("당신의 질문:")


if user_input:
    response = gemini_llm(user_input)
    st.write(f"챗봇: {response}")

    log_interaction(user_input, response)
