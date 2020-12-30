import json

import pika

from main import db, Product
from settings import RABBITMQ_URL

params = pika.URLParameters(RABBITMQ_URL)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')

def callback(ch, method, properties, body):
    print('Receive in main')
    try:
        data = json.loads(body)
        print(data)
        if properties.content_type == 'product_created':
            product = Product(id=data['id'], title=data['title'], image=data['image'])
            db.session.add(product)
            db.session.commit()
            print('Product Created')

        if properties.content_type == 'product_updated':
            product = Product.query.get(id=data)
            product.title = data['title']
            product.image = data['image']
            db.session.commit()
            print('Product Updated')

        if properties.content_type == 'product_deleted':
            product = Product.query.get(data)
            db.session.delete(product)
            db.session.commit()
            print('Product Deleted')
    except:
        pass

channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Starting Consuming')

channel.start_consuming()

channel.close()