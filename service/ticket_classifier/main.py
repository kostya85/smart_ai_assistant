import pika
import pickle
import json
import os

import pandas as pd

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

# Установка соединения с RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Создание очереди
channel.queue_declare(queue='ticket_add_queue')

# Загрузка модели
with open(os.path.dirname(os.path.abspath(__file__)) + '/models/logistic_regression/model.pkl', 'rb') as file: 
    model = pickle.load(file)

def classify_ticket(ticket):
    X = ticket.complaint_text

    count_vect = CountVectorizer()
    X_vect = count_vect.fit_transform(X)

    tfidf_transformer = TfidfTransformer()
    X_tfidf = tfidf_transformer.fit_transform(X_vect)

    # Классификация обращения с помощью модели LogisticRegression
    predicted_class = model.predict(X_tfidf)[0]

    return predicted_class

def callback(ch, method, properties, body):
    # Получение сообщения из очереди
    message = json.loads(body)

    # Обработка полученного объекта обращения
    ticket_id = message['id']
    ticket_text = message['text']

    # Исходный словарь
    ticket = {
        'complaint_text': ticket_text
    }

    # Создание DataFrame из словаря
    df = pd.DataFrame(ticket, index=[0])
    df['complaint_text'] = df['complaint_text'].astype(str)

    predicted_class = classify_ticket(df)
    
    # Ваш код для обработки объекта обращения
    print(f"Получен объект обращения. ID: {ticket_id}, Текст: {ticket_text}")

# Подписка на получение сообщений из очереди
channel.basic_consume(queue='ticket_add_queue', on_message_callback=callback, auto_ack=True)

print("Ожидание сообщений из RabbitMQ...")
channel.start_consuming()