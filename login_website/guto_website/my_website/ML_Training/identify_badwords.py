from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
import pandas as pd
import smtplib
import django
import sys
import os


def setup_django():
    current_dir = os.path.dirname(__file__)
    core_dir = os.path.abspath(os.path.join(current_dir, '..'))
    sys.path.append(core_dir)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_website.settings')
    django.setup()


def Identify_marked_phrases(text, marked_phrases):
    count = 0
    if isinstance(text, str):
        for phrase in marked_phrases:
            count += text.lower().count(phrase.lower())
    return count


def Send_email_warn(destinatario, assunto, mensagem):
    smtp_server = settings.EMAIL_HOST
    smtp_port = settings.EMAIL_PORT
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


def ban_user(username, models):
    user = models.CustomUser.objects.get(username=username)
    user_ban, created = models.UserBan.objects.get_or_create(user=user)
    user_ban.is_banned = True
    user_ban.ban_reason = "Palavras ofensivas detectadas automaticamente"
    user_ban.save()


def run_code():
    from core import models

    marked_phrases = [
        'Caralho', 'krl', 'Porra', 'BCT', 'Buceta', 'pqp',
        'Cacete', 'putaquepariu', 'puta que pariu', 'porra',
        'kct', 'meu pau'
    ]

    marked_phrases = [str(phrase) for phrase in marked_phrases]
    limite_palavras_ofensivas = 2

    df = pd.read_csv('ML_Training/Users_csv/dados_usuarios.csv')

    def count_marked_phrases(text):
        return Identify_marked_phrases(text, marked_phrases)

    df['marked_words'] = df['username'].apply(count_marked_phrases)
    df['marked_names'] = df['description'].apply(count_marked_phrases)

    for index, row in df.iterrows():
        if (
            row['marked_words'] >= limite_palavras_ofensivas or
            row['marked_names'] >= limite_palavras_ofensivas
        ):
            destinatario = row['email']
            assunto = "Aviso: Conteúdo ofensivo detectado"
            mensagem = (
                "Prezado usuário,\n\nDetectamos palavras ofensivas "
                "em seu texto. Por favor, reveja e edite o conteúdo."
                "\n\nAtenciosamente,\nEquipe do Guto."
            )
            try:
                Send_email_warn(destinatario, assunto, mensagem)
                ban_user(row['username'], models)
            except ModuleNotFoundError:
                Send_email_warn.smtp_server = os.getenv('EMAIL_HOST')
                Send_email_warn.smtp_port = os.getenv('EMAIL_PORT')
                Send_email_warn.remetente = os.getenv('EMAIL_HOST_USER')
                Send_email_warn.senha = os.getenv('EMAIL_HOST_PASSWORD')

    df.to_csv('ML_Training/Users_csv/dados_usuarios_com_palavras_alvo.csv', index=False)

    return marked_phrases

if __name__ == "__main__":
    setup_django()
    run_code()
