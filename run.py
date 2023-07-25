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


if 'session_created' in st.session_state:
    # Создаем подключение к SQLite
    st.session_state['session_created'] = True

# Пользовательский ввод в боковой панели
md = ''
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

en = True

st.set_page_config(
    page_title="Европоиск",
    page_icon="💾",
    layout="wide",
    initial_sidebar_state="expanded"
)

hide_streamlit_style = """
    <style>
    #MainMenu {visibility: visible}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

toggle_state = st.sidebar.checkbox('Включить режим таблицы', key='toggle_button', value=True)
user_input = st.sidebar.text_input("Введите поисковый запрос:")

if user_input:
    # Формируем и выполняем SQL-запрос поиска
    cursor.execute("SELECT * FROM data WHERE LOWER(name) LIKE '%' || LOWER(?) || '%'", (user_input,))
else:
    # Если пользователь не ввел поисковый запрос, выбираем все данные
    if not toggle_state:
        st.markdown('# Введите запрос в левом окне.')
    cursor.execute("SELECT * FROM data")

results = make_bool(make_tup_lis(cursor.fetchall()))

# Получаем названия колонок из cursor.description
column_names = [desc[0] for desc in cursor.description[:2]] + ['Клапан', 'Распылитель', 'Стакан', 'Пружина', 'Медное кольцо']

# Если есть результаты, отображаем их в виде DataFrame
if not toggle_state and results and user_input:
    cursor.execute("""SELECT name,
           COUNT(name) as total_count,
           SUM(case when clapan = 0 then 1 else 0 end) as missing_clapan,
           SUM(case when raspil = 0 then 1 else 0 end) as missing_raspil,
           SUM(case when stakan = 0 then 1 else 0 end) as missing_stakan,
           SUM(case when jumper = 0 then 1 else 0 end) as missing_jumper,
           SUM(case when cupper_ring = 0 then 1 else 0 end) as missing_cupper_ring
    FROM data
    WHERE LOWER(name) LIKE '%' || LOWER(?) || '%'
    GROUP BY name;
    """, (user_input,))
    results_ = cursor.fetchall()
    for i in results_:
        md += f'## {i[0]} <font size=10>Σ <font color="#FFFF00">{i[1]}</font></font>\n'
        # Выведите названия строк
        for k, v in zip(['Клапан', 'Распылитель', 'Стакан', 'Пружина', 'Медное кольцо'], i[2:]):
            md += f'- <font size=6 color="#FF0000"><b>{k} </font><font size=6>{v}</b></font>\n' if v != 0 else f'- <font size=6 color="#00FF00"><b>{k}</b></font>\n'
        # st.dataframe(df, hide_index=True, use_container_width=True)

    st.markdown(md if md else "# Форсунки в полном составе!", unsafe_allow_html=True)
elif toggle_state and results:
    df = pd.DataFrame(results, columns=column_names)

    st.dataframe(df, hide_index=True, use_container_width=True)
elif user_input:
    st.markdown("# Ничего не найдено")
