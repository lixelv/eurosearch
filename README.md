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

    st.data_editor(df, hide_index=True)
    #  st.markdown(df.to_html(index=False), unsafe_allow_html=True)
else:
    st.write("Результаты не найдены.")

```
run_test.py:
```python
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
```
run_write.py:
```python
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
