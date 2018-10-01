import pika


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()



channel.queue_declare(queue='bot')
channel.basic_publish(exchange='', routing_key='bot', body='123456')
print('Bot is being invoke...')
connection.close()