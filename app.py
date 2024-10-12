import datetime

import folium
import streamlit as st
import streamlit.components.v1 as components
from streamlit_folium import st_folium

from modules.gemini_llm import gemini_llm
from modules.kakaomap import kakaomap, location_to_coordinate


def log_interaction(user_input, response):
    with open("chat_log.txt", "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] User: {user_input}\n")
        log_file.write(f"[{timestamp}] Bot: {response}\n\n")


st.title("장소 알려주는 챗봇")
st.write("주소를 입력해주세요")


user_input = st.text_input("당신의 질문:")


if user_input:
    answer, location = gemini_llm(user_input)
    st.write(f"챗봇: {answer}")
    y, x = location_to_coordinate(location)
    if y != None:
        map_center = [y, x]
        m = folium.Map(location=map_center, zoom_start=15)

        icon_url = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png"
        custom_icon = folium.CustomIcon(icon_url, icon_size=(30, 40))
        folium.Marker(location=map_center, popup=map_center, icon=custom_icon).add_to(m)

        # Streamlit에 Folium 지도 표시
        st_folium(m, width=700, height=500)

    log_interaction(user_input, answer)
