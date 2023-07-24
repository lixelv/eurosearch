import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="Европоиск ввод",
    page_icon="✒️",
    layout="wide",
    initial_sidebar_state="expanded"
)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

user_input = st.sidebar.text_input("Введите поисковый запрос:")

# Новые виджеты ввода данных для добавления или обновления записей
record_input = st.sidebar.text_input("Введите новую запись:")
update_input = st.sidebar.text_input("Введите обновленную запись:")
record_id_input = st.sidebar.text_input("Введите ID записи для обновления:")

# Если введена новая запись, вставляем ее в базу данных
if record_input:
    cursor.execute("INSERT INTO data (name) VALUES (?)", (record_input,))
    conn.commit()

# Если введены обновленная запись и ID записи, обновляем запись в базе данных
if update_input and record_id_input:
    cursor.execute("UPDATE data SET name = ? WHERE id = ?", (update_input, record_id_input))
    conn.commit()

cursor.execute("SELECT * FROM data")
results = cursor.fetchall()
column_names = [desc[0] for desc in cursor.description]

if results:
    df = pd.DataFrame(results, columns=column_names)
    mask = df['name'].apply(lambda x: user_input.lower() in str(x).lower())
    st.data_editor(df, hide_index=True)
    print(df)
else:
    st.write("Результаты не найдены.")