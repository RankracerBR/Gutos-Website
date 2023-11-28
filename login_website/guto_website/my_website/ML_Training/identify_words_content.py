from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import csv

class ProhibitedContentDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = MultinomialNB()
        self.terms_to_detect = ['porn','sex']
        self.labels = [0,1]
        
    def train(self,data,labels):
        X = self.vectorizer.fit_transform(data)
        self.model.fit(X, labels)
    
    def detect_prohibited_content(self, input_text):
        input_vector = self.vectorizer.transform([input_text])
        prediction = self.model.predict(input_vector)
        
        if prediction[0] == 1:
            return "Conteúdo proibido foi detectado"
        else:
            return "Nenhum conteúdo proibido foi detectado"

data = [
    "Este é um texto sem conteúdo proibido",
    "Aqui há palavras proibidas como porn e sex"
]

labels = np.array([0,1])

detector = ProhibitedContentDetector()
detector.train(data,labels)

