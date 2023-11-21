from sklearn.feature_extraction.text import CountVectorizer
import csv

def detect_prohibited_content(input_text):
    terms_to_detect = ['porn', 'sex']
    input_list = [input_text]

    with open('ML_Training/Users_csv/inputs.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Input Text']
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Verificar se é a primeira vez que o arquivo é aberto
        if csvfile.tell() == 0:
            writer.writeheader()

        # Escrever o input no arquivo CSV
        writer.writerow({'Input Text': input_text})
        
    vectorizer = CountVectorizer(vocabulary=terms_to_detect)
    input_matrix = vectorizer.fit_transform(input_list)

    # Transforma a matriz esparsa em uma matriz densa
    input_matrix_dense = input_matrix.toarray()

    # Obtém a contagem de cada palavra
    word_counts = input_matrix_dense.sum(axis=0)

    for term, count in zip(terms_to_detect, word_counts):
        if count > 0:
            return f"O termo '{term}' foi detectado no input."

    return "Nenhum termo foi detectado."
