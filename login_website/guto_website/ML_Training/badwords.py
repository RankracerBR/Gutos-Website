import pandas as pd
#A partir da identificação das palavras, fazer script para mandar ao email do usuário correspondente avisando sobre os palavrões e criar um sistema para bani-lo
def identify_marked_phrases(text):
    count = 0
    for phrase in marked_phrases:
        count += text.lower().count(phrase.lower())
    return count

df = pd.read_csv('login_website/guto_website/my_website/dados_usuarios.csv')

marked_phrases = ['Caralho','krl','Porra','BCT','Buceta','Olá Mundo!']

df['marked_words'] = df['complete_description'].apply(identify_marked_phrases)

df.to_csv('login_website/guto_website/my_website/dados_usuarios_com_palavras_alvo.csv', index=False)
