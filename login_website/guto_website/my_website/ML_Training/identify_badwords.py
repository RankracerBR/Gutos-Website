from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import smtplib

#A partir da identificação das palavras, fazer script para mandar ao email do usuário correspondente avisando sobre os palavrões e criar um sistema para bani-lo
#Depois fazer um script para que isso seja automatico, através da lib os ou subprocess

total_palavras_ofensivas = 0
limite_palavras_ofensivas = 1

def identify_marked_phrases(text):
    count = 0
    for phrase in marked_phrases:
        count += text.lower().count(phrase.lower())
    return count

# Função para enviar um e-mail de aviso
def enviar_email_aviso(destinatario, assunto, mensagem):
    # Configuração do servidor SMTP do Gmail ou do seu provedor de e-mail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Substitua pelo seu endereço de e-mail e senha
    remetente = ""
    senha = ""

    # Crie um objeto SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)

    # Inicie a conexão com o servidor
    server.starttls()

    # Faça login na conta do remetente
    server.login(remetente, senha)

    # Crie a mensagem
    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = assunto

    # Adicione o corpo da mensagem
    msg.attach(MIMEText(mensagem, "plain"))

    # Envie a mensagem
    server.sendmail(remetente, destinatario, msg.as_string())

    # Encerre a conexão com o servidor
    server.quit()

df = pd.read_csv('dados_usuarios.csv')

marked_phrases = ['Caralho','krl','Porra','BCT','Buceta','Olá Mundo!','pqp','Cacete','putaquepariu','puta que pariu']

df['marked_words'] = df['descricao_anterior'].apply(identify_marked_phrases)

df.to_csv('dados_usuarios_com_palavras_alvo.csv', index=False)

total_palavras_ofensivas = df['marked_words'].sum()

# Itere sobre os usuários e envie e-mails de aviso se excederem o limite de palavras ofensivas
for index, row in df.iterrows(): #fazer somatório por coluna
    if row['marked_words'] >= limite_palavras_ofensivas:
        destinatario = row['email_do_usuario']
        assunto = "Aviso: Conteúdo ofensivo detectado"
        mensagem = f"Prezado usuário,\n\nDetectamos palavras ofensivas em seu texto. Por favor, reveja e edite o conteúdo.\n\nAtenciosamente,\nEquipe do Guto."
        enviar_email_aviso(destinatario, assunto, mensagem)

# Exiba o total de palavras ofensivas
total_palavras_ofensivas = df['marked_words'].sum()
print(f"Total de palavras ofensivas: {total_palavras_ofensivas}")