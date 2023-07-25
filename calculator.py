import streamlit as st
from math import *

st.set_page_config(
    page_title="Калькулятор",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# st.markdown("""
# <style>
# footer {visibility: hidden;}
# header {visibility: hidden;}
# </style>
# """, unsafe_allow_html=True)

text = st.sidebar.text_input('🔢 Введите математическое выражение:').replace('^', '**')
if text != '':
    st.sidebar.markdown(f'<font size=64>Ответ: `{eval(text)}`</font>', unsafe_allow_html=True)
else:
    st.sidebar.markdown(f'<font size=64>Введите выражение</font>', unsafe_allow_html=True)