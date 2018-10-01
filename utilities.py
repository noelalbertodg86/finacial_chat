import pika
import uuid
import sys
import traceback

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

queue_ = 'bot'

class Utilities:

    def __init__(self, connections=None):
        self.idmensaje = str(uuid.uuid1())
        self.connections = connections

    def invokeBot(self, queue=queue_, body = 'start'):

        #invoque bot
        channel.queue_declare(queue=queue)
        channel.basic_publish(exchange='', routing_key=queue, body=self.idmensaje)

        #wait and send  the bot response
        self.get_bot_resul()


    def get_bot_resul(self):
        try:
            result_queue = ':'.join(['bot', self.idmensaje])
            channel.queue_declare(queue=result_queue)
            print('BotResponse is waiting for messages...')
            channel.basic_consume(self.send_message, queue=result_queue, no_ack=True)
            channel.start_consuming()
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
            print('**** ERROR in get_bot_resul %s' % error)

    def send_message(self, ch, method, properties, body):
        try:
            print('Send Bot response to conected client: %s' % body.decode())
            for connection in self.connections:
                    connection.send(body)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
            print('**** ERROR in send_message %s' % error)




def userdb():
    return [{'user': 'noel', 'age': 32, 'birthday': '1986-01-27', 'pass': '123'},
            {'user': 'user', 'age': 30, 'birthday': '1988-05-12', 'pass': 'admin'}]


#print(get_settings_value('BOT', 'url'))
# u = Utilities({})
# u.invokeBot()
