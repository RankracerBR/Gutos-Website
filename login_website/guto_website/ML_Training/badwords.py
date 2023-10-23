from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import smtplib

#A partir da identificação das palavras, fazer script para mandar ao email do usuário correspondente avisando sobre os palavrões e criar um sistema para bani-lo
#Depois fazer um script para que isso seja automatico, através da lib os ou subprocess

def identify_marked_phrases(text):
    count = 0
    for phrase in marked_phrases:
        count += text.lower().count(phrase.lower())
    return count

def send_warning_email(user_email):
    email_server = 'smtp.gmail.com'
    email_port = 587
    email_username = ''
    email_password = ''
    
    subject = 'Aviso'
    body = 'Detectamos conteúdo ofensivo em sua descrição de usuário. Por favor, faça as alterações necessárias'
    sender_email = 'rankracerbr21@gmail.com'
    receiver_email = user_email
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    
    try:
        server = smtplib.SMTP(email_server,email_port)
        server.starttls()
        server.login(email_username, email_password)
    except Exception as e:
        print('Erro ao enviar o email:',str(e))

df = pd.read_csv('login_website/guto_website/my_website/dados_usuarios.csv')

marked_phrases = ['Caralho','krl','Porra','BCT','Buceta','Olá Mundo!','pqp','Cacete']

df['marked_words'] = df['descricao_anterior'].apply(identify_marked_phrases)

df.to_csv('login_website/guto_website/my_website/dados_usuarios_com_palavras_alvo.csv', index=False)

for index, row in df.iterrows():
    if row['marked_words']:
        user_email = row['email_do_usuario']
        send_warning_email(user_email)
