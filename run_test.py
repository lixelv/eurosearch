import streamlit as st
import sqlite3
import pandas as pd

if 'session_created' not in st.session_state:
    # Код, который выполняется только один раз при создании новой сессии
    df = pd.DataFrame(
        {
            'Id': [9, 8, 7],
            'Name': ['Simon', 'Nini', 'Sokama']
        }
    )
    st.session_state['dataframe'] = df
    st.session_state['session_created'] = True

# Получаем DataFrame из состояния сессии
df = st.session_state['dataframe']

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

user_input = st.sidebar.text_input("Введите поисковый запрос:")
mask = df['Name'].apply(lambda x: user_input.lower() in str(x).lower())
df[mask] = st.data_editor(df[mask])
print(df)