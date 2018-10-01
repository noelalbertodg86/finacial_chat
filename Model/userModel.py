import sys
import traceback

from ADO.postgresql import postgresql

class user():

    def __init__(self):
        self.ado = postgresql()

    def userLogin(self, params):
        try:
            sql = "select name, user, id from chat.public.user where user_name = '%(user)s'  and password = '%(pass)s' " % params
            userData = self.ado.getDbdata(sql)
            return userData
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
            print('**** Model.user.userLogin %s' % error)

    def createUser(self,params):
        try:
            sql = """INSERT INTO chat.public."user"( name, "lastName", birthday, "user_name", password)
                        VALUES ( '%(name)s', '%(lastName)s', '%(birthday)s', '%(user)s', '%(password)s');""" % params
            return self.ado.execute(sql)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
            print('**** Model.user.createUser %s' % error)
            return False

# if __name__ == '__main__':
#     user_ = user()
#     resul = user_.createUser({'name': 'David', 'lastName': 'Diaz',
#                       'birthday': '2014-07-16', 'user':'david', 'password': 'david'})
#     if resul:
#         print('Usario creado satisfactoriamente')