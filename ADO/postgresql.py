import sys
import traceback
import psycopg2

from config import getconfigValue

conn = None
class postgresql:

    def __init__(self):
        try:
            self.host = getconfigValue('DATABASE', 'host')
            self.user = getconfigValue('DATABASE', 'user')
            self.password = getconfigValue('DATABASE', 'pass')
            self.dataBase = getconfigValue('DATABASE', 'database')
            self.port = getconfigValue('DATABASE', 'port')
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect("host=%s port=%s user=%s password=%s dbname=%s" % \
                                         (self.host, self.port, self.user, self.password, self.dataBase))

            self.cursor = self.conn.cursor()
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
            print('**** DatabaseError: %s' % error)

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
            print('**** Execute DatabaseError: %s' % error)
            return False

    def getDbdata(self, sql):
        try:
            result = []
            self.cursor.execute(sql)
            while True:
                row = self.cursor.fetchone()
                if row: result.append(row)
                if row == None:
                   break
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
            print('**** getDbdata DatabaseError: %s' % error)
        finally:
            return result

# if __name__ == '__main__':
#     q = postgresql()
