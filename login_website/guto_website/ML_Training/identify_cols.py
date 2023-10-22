import pandas as pd
import sqlite3

# Conecte-se ao arquivo SQLite
conn = sqlite3.connect('login_website/guto_website/my_website/db.sqlite3')

# Execute uma consulta SQL para extrair os dados que você deseja converter em CSV
# Substitua 'sua_tabela' pelo nome da tabela que deseja converter
query = "SELECT complete_email,complete_description,registration_date FROM CadastroUsuario"

# Use o Pandas para ler os dados do SQLite em um DataFrame
df = pd.read_sql_query(query, conn)

# Feche a conexão com o arquivo SQLite
conn.close()

# Salve o DataFrame como um arquivo CSV
df.to_csv('login_website/guto_website/my_website/dados_usuarios.csv', index=False)

