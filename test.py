import pandas as pd
from sqlalchemy import create_engine

# Загрузите данные из Excel в DataFrame
df = pd.read_excel('data.xlsx')  # Укажите здесь свой путь к файлу

# Создайте подключение к базе данных
engine = create_engine('sqlite:///Z:/GitHub/europoisk/data.db')

# Запишите данные из DataFrame в таблицу в базе данных
df.to_sql('data', engine, if_exists='replace', index=False)  # Заменил 'table_name' на 'data', поскольку вы указали, что таблица называется 'data'
