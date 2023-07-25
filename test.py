import pandas as pd
import time, random
import sqlite3
from prettytable import PrettyTable

conn = sqlite3.connect('data.db')
cur = conn.cursor()

cur.execute('SELECT MAX(id) FROM data')
for i in range(1, cur.fetchone()[0]+1):
	for _ in range(random.choice(range(0, 30))):
		cur.execute ('INSERT INTO data (name, clapan, raspil, stakan, jumper, cupper_ring) VALUES ((SELECT name FROM data WHERE id = ?), ?, ?, ?, ?, ?)', (i, random.choice([False, True, True]), random.choice([False, True, True]), random.choice([False, True, True]), random.choice([False, True, True]), random.choice([False, True, True])))
conn.commit()
# def compare_pd(df_1, df_2):

# 	df_1.set_index('id', inplace=True)
# 	df_2.set_index('id', inplace=True)
	
# 	diff_df = df_1.compare(df_2)

# 	diff_df = diff_df.xs('self', axis=1, level=1)

# 	# Преобразуем DataFrame в формат "длинный", где каждая строка это пара "id" и "значение".
# 	melted_df = diff_df.reset_index().melt(id_vars='id', var_name='column', value_name='data')

# 	# Преобразуем преобразованный DataFrame в список словарей.
# 	return melted_df.to_dict('records')

# conn = sqlite3.connect('data.db')
# cursor = conn.cursor()
# cursor.execute("UPDATE data SET name='Тmaы лох!' WHERE id=132")
# conn.commit()
# cursor.execute('SELECT * FROM data')

# conn_1 = sqlite3.connect('data_1.db')
# cursor_1 = conn_1.cursor()
# cursor_1.execute('SELECT * FROM data')

# # Тестирование функции
# df_1 = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
# df_2 = pd.DataFrame(cursor_1.fetchall(), columns=[desc[0] for desc in cursor_1.description])

# # Преобразуем преобразованный DataFrame в список словарей.
# result = compare_pd(df_1, df_2)

# print(result)
# zero_rows = df_1.columns[(df_1 == 0).any()].tolist()
# print(zero_rows)