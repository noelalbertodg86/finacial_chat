import sys
import traceback

from ADO.postgresql import postgresql


class chatMessageModel():

    def __init__(self):
        self.ado = postgresql()

    def saveMessage(self, params):
        try:
            sql = """INSERT INTO chat.public."chatMessage"(message, "chatRoom", "idUser")
                      VALUES ('%(message)s', 'DEFAULT', '%(userId)s');""" % params
            return self.ado.execute(sql)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
            print('**** Model.chatMessageModel.saveMessage %s' % error)
            return False

# if __name__ == '__main__':
#     msg = chatMessageModel()
#     resul = msg.saveMessage({'userId': 1, 'user':'noel', 'message': 'asdfghjk', 'chatRoom': ''})
#     if resul:
#         print('Usario creado satisfactoriamente')
