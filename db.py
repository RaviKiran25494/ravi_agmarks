import MySQLdb

class Db():

  def __init__(self):
       # print(‘DB is initiated’)
       self.conn = MySQLdb.connect(user="root", password="", database="agmark")
       # print(‘DB is created’)
       # print(self.conn)

  def execute(self, query):
       cur = self.conn.cursor()
       cur.execute(query)
       result = cur.fetchall()
       return result

  def commit(self):
       self.conn.commit()

  def close(self):
       self.conn.close()