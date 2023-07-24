run.py:
```python
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="Европоиск",
    page_icon="💾",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Скрываем меню и подвал с помощью CSS
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Создаем подключение к SQLite
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Пользовательский ввод в боковой панели
user_input = st.sidebar.text_input("Введите поисковый запрос:")

if user_input:
    # Формируем и выполняем SQL-запрос поиска
    cursor.execute("SELECT * FROM data WHERE LOWER(name) LIKE '%' || LOWER(?) || '%'", (user_input,))
else:
    # Если пользователь не ввел поисковый запрос, выбираем все данные
    cursor.execute("SELECT * FROM data")

results = cursor.fetchall()

# Получаем названия колонок из cursor.description
column_names = [desc[0] for desc in cursor.description]

# Если есть результаты, отображаем их в виде DataFrame
if results:
    df = pd.DataFrame(results, columns=column_names)

    st.dataframe(df, width=1080)
    #  st.markdown(df.to_html(index=False), unsafe_allow_html=True)
else:
    st.write("Результаты не найдены.")

```
test.py:
```python
import pandas as pd
from sqlalchemy import create_engine

# Загрузите данные из Excel в DataFrame
df = pd.read_excel('data.xlsx')  # Укажите здесь свой путь к файлу

# Создайте подключение к базе данных
engine = create_engine('sqlite:///Z:/GitHub/europoisk/data.db')

# Запишите данные из DataFrame в таблицу в базе данных
df.to_sql('data', engine, if_exists='replace', index=False)  # Заменил 'table_name' на 'data', поскольку вы указали, что таблица называется 'data'

```
