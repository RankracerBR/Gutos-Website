from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
import pandas as pd
import smtplib


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

def Send_email_warn(destinatario, assunto, mensagem):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    remetente = settings.EMAIL_HOST_USER
    senha = settings.EMAIL_HOST_PASSWORD


    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(remetente, senha)


    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.attach(MIMEText(mensagem, "plain"))


    server.sendmail(remetente, destinatario, msg.as_string())
    server.quit()


df = pd.read_csv('ML_Training/Users_csv/dados_usuarios.csv')


df['marked_words'] = df['username'].apply(Identify_marked_phrases)
df['marked_names'] = df['description'].apply(Identify_marked_phrases)


for index, row in df.iterrows():
    if row['marked_words'] >= limite_palavras_ofensivas or row['marked_names'] >= limite_palavras_ofensivas:
        destinatario = row['email']
        assunto = "Aviso: Conteúdo ofensivo detectado"
        mensagem = f"Prezado usuário,\n\nDetectamos palavras ofensivas em seu texto. Por favor, reveja e edite o conteúdo.\n\nAtenciosamente,\nEquipe do Guto."
        Send_email_warn(destinatario, assunto, mensagem) 


df.to_csv('ML_Training/Users_csv/dados_usuarios_com_palavras_alvo.csv', index=False)
