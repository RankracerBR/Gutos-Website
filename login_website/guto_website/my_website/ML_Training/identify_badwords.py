from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import smtplib

# Define o critério de palavras ofensivas e limite
marked_phrases = ['Caralho', 'krl', 'Porra', 'BCT', 'Buceta', 'pqp', 'Cacete', 'putaquepariu', 'puta que pariu', 'porra', 'kct', 'meu pau']
marked_phrases = [str(phrase) for phrase in marked_phrases]
limite_palavras_ofensivas = 2

# Função para identificar palavras ofensivas
def Identify_marked_phrases(text):
    count = 0
    if isinstance(text, str):
        for phrase in marked_phrases:
            count += text.lower().count(phrase.lower())
    return count

# Função para enviar e-mail de aviso
def Send_email_warn(destinatario, assunto, mensagem):
    # Configuração do servidor SMTP do Gmail ou do seu provedor de e-mail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    remetente = "rankracerbr21@gmail.com"  # Insira seu e-mail aqui
    senha = "pexqzhwcosqimbbf"  # Insira sua senha aqui

    # Conecta ao servidor SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(remetente, senha)

    # Cria a mensagem
    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.attach(MIMEText(mensagem, "plain"))

    # Envia a mensagem
    server.sendmail(remetente, destinatario, msg.as_string())
    server.quit()

# Carrega os dados dos usuários
df = pd.read_csv('ML_Training/Users_csv/dados_usuarios.csv')

# Verifica palavras ofensivas nos campos 'username' e 'description'
df['marked_words'] = df['username'].apply(Identify_marked_phrases)
df['marked_names'] = df['description'].apply(Identify_marked_phrases)

# Analisa se ultrapassa o limite e envia e-mail de aviso
for index, row in df.iterrows():
    if row['marked_words'] >= limite_palavras_ofensivas or row['marked_names'] >= limite_palavras_ofensivas:
        destinatario = row['email']
        assunto = "Aviso: Conteúdo ofensivo detectado"
        mensagem = f"Prezado usuário,\n\nDetectamos palavras ofensivas em seu texto. Por favor, reveja e edite o conteúdo.\n\nAtenciosamente,\nEquipe do Guto."
        Send_email_warn(destinatario, assunto, mensagem)

# Salva o DataFrame atualizado
df.to_csv('ML_Training/Users_csv/dados_usuarios_com_palavras_alvo.csv', index=False)
