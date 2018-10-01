import sys
import pika
import traceback
import requests
from config import getconfigValue

queue_ = 'bot'

class Bot():

    def __init__(self):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=queue_)
            self.url = getconfigValue('BOT','url')
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
            print('**** ERROR STARTING BOT %s' % error)

    def execute(self, ch, method, properties, body):
        try:
            result = ''
            if isinstance(body, bytes):
                body = body.decode()
            print('BOT recieve %s' % body)
            response = requests.get(self.url)
            if response.status_code == 200:
                text = response.text.split('\r\n')
                column = text[0].split(',')
                data = text[1].split(',')
                result = 'BOT: APPL quote is $%s per share' % (data[column.index('Close')])
            else:
                result = 'BOT: A error was occur during the stock consult. Error Code: %s' % response.status_code

            print("BOT: result %s" % result)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
            print('**** ERROR %s' % error)
            result = 'BOT: Error getting stock'
        finally:
            result_queue = ':'.join([queue_,body])
            self.send_result(result, result_queue)

    def send_result(self, result, result_queue):
        try:
            self.channel.queue_declare(queue=result_queue)
            self.channel.basic_publish(exchange='', routing_key=result_queue, body=result)
            print('Send bot result...')
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
            print('**** BOT SEND RESULT  %s' % error)


    def run(self):
        self.channel.basic_consume(self.execute, queue=queue_, no_ack=True)
        print('Bot is waiting for messages...')
        self.channel.start_consuming()

bot_ = Bot()
bot_.run()
