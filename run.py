
import streamlit as st
import sqlite3
import pandas as pd

def make_tup_lis(lis):
    lis = list(lis)
    for i in range(len(lis)):
        lis[i] = list(lis[i])
    return lis

def make_bool(lis):
    for i in range(len(lis)):
        for i_ in range(len(lis[i])):
            lis[i][i_] = bool(lis[i][i_]) if i_ >= 2 else lis[i][i_]
    return lis

if 'session_created'  in st.session_state:
    st.set_page_config(
        page_title="Европоиск",
        page_icon="💾",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Создаем подключение к SQLite
    st.session_state['session_created'] = True

# Пользовательский ввод в боковой панели
md = ''
conn = sqlite3.connect('data.db')
cursor = conn.cursor()
user_input = st.sidebar.text_input("Введите поисковый запрос:")

hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if user_input:
    # Формируем и выполняем SQL-запрос поиска
    cursor.execute("SELECT * FROM data WHERE LOWER(name) LIKE '%' || LOWER(?) || '%'", (user_input,))
else:
    # Если пользователь не ввел поисковый запрос, выбираем все данные
    cursor.execute("SELECT * FROM data")

results = make_bool(make_tup_lis(cursor.fetchall()))

# Получаем названия колонок из cursor.description
column_names = [desc[0] for desc in cursor.description[:2]] + ['Клапан', 'Распылитель', 'Стакан', 'Пружина', 'Медное кольцо']

# Если есть результаты, отображаем их в виде DataFrame
if len(results) <= 5 and results:
    for i in results:
        df = pd.DataFrame([i], columns=column_names)
        # Используйте метод any() для проверки, есть ли хотя бы одно True (т.е. значение 0) в каждой строке
        zero_rows = df.columns[(df == False).any()].tolist()
        md += f'### Отсутствует запчасть у {i[1].split(" ")[-1]}.\n' if zero_rows else ''
        # Выведите названия строк
        for row in zero_rows:
             md += f'- <font size=6 color="#FF0000"><b>{row}</b></font>\n'
        # st.dataframe(df, hide_index=True, use_container_width=True)

    st.markdown(md if md else "# Форсунка в полном составе!", unsafe_allow_html=True)
elif results:
    df = pd.DataFrame(results, columns=column_names)

    st.dataframe(df, hide_index=True, use_container_width=True)
else:
    st.markdown("# Ничего не найдено")
