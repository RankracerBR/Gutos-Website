import pandas as pd
import sqlite3

# Conectar-se ao banco de dados SQLite
conn = sqlite3.connect('db.sqlite3')

query = """
SELECT * FROM core_customuser
"""

df = pd.read_sql_query(query, conn)

conn.close()

df.to_csv('ML_Training/Users_csv/dados_usuarios.csv', index=False)

'''
data = df.to_dict(orient='records')

client = MongoClient('localhost',27017)

db = client['test']
collection = db['testusers']

collection.insert_many(data)

client.close()
'''

