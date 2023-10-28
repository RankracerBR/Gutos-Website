from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import smtplib

#Critérios
total_palavras_ofensivas = 0
limite_palavras_ofensivas = 2

total_nomes_ofensivos = 0
limite_nomes_ofensivos = 2

#Verificador
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

#Lê o arquivo
df = pd.read_csv('ML_Training/Users_csv/dados_usuarios.csv')

#Palavras proibidas
marked_phrases = ['Caralho','krl','Porra','BCT','Buceta','Olá Mundo!','pqp','Cacete','putaquepariu','puta que pariu','porra','kct','meu pau']

#Verifica Nome e Descrição anterior
df['marked_words'] = df['descricao_anterior'].apply(identify_marked_phrases)
df['marked_names'] = df['nome_anterior'].apply(identify_marked_phrases)

#Converte para .csv os dados
df.to_csv('ML_Training/Users_csv/dados_usuarios_com_palavras_alvo.csv', index=False)

#Faz a soma das palavras
total_palavras_ofensivas = df['marked_words'].sum()
total_nomes_ofensivos = df['marked_names'].sum()

#Analisa se o somatório das colunas é maior que o limite e então manda o email caso ultrapasse
for index, row in df.iterrows():
    if row['marked_words'] >= limite_palavras_ofensivas or row['marked_names'] >= limite_nomes_ofensivos:
        destinatario = row['email_do_usuario']
        assunto = "Aviso: Conteúdo ofensivo detectado"
        mensagem = f"Prezado usuário,\n\nDetectamos palavras ofensivas em seu texto. Por favor, reveja e edite o conteúdo.\n\nAtenciosamente,\nEquipe do Guto."
        enviar_email_aviso(destinatario, assunto, mensagem)


print(f"Total de palavras ofensivas: {total_palavras_ofensivas}")
