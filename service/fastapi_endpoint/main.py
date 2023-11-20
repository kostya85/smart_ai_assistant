from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pika
import json

# Установка соединения с RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='ticket_add_queue')

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Ticket(BaseModel):
    id: int
    text: str
    endpoint: str

@app.post("/add/")
async def create_ticket(ticket: Ticket):
    # Преобразование объекта обращения в JSON
    message = json.dumps(ticket.dict())

    # Отправка сообщения в очередь
    channel.basic_publish(exchange='', routing_key='ticket_add_queue', body=message)

    print("Сообщение отправлено в RabbitMQ")

    return {"message": "Обращение успешно создано и отправлено в RabbitMQ"}