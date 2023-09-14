import psycopg2
from datetime import datetime

class database():

	def __init__(self):
		self.conn = psycopg2.connect("dbname=locker user=postgres password=tree") 
		self.cur = self.conn.cursor()

	def current_time(self):
		now = datetime.now()   
		return now.strftime("%Y-%m-%d %H:%M:%S")
	
	def close_connection(self):
		self.cur.close()
		self.conn.close()

	def insert_rec(self,website,userid,password):
		query = f"INSERT INTO secureDB VALUES('{website}','{userid}','{password}',TIMESTAMP '{self.current_time()}') "
		self.cur.execute(query)
		self.conn.commit()

	def find_rec(self,website):
		query = f"SELECT * FROM secureDB WHERE website='{website}'"
		self.cur.execute(query)
		res = self.cur.fetchall()
		return res

	def update_entry(self,website,password):
		query = f"UPDATE secureDB set pass='{password}',time=TIMESTAMP '{self.current_time()}' WHERE website='{website}'"
		self.cur.execute(query)
		self.conn.commit()

	def delete_entry(self,website):
		query = f"DELETE FROM secureDB WHERE website='{website}'"
		self.cur.execute(query)

	def check_validity(self):
		self.cur.execute("select * FROM secureDB")
		db_version = self.cur.fetchall()
		for row in db_version:
			if row[3]:
				last_saved_date = datetime.date(row[3])
				today = datetime.strptime(self.current_time(), "%Y-%m-%d %H:%M:%S")
				if (datetime.date(today)-last_saved_date).days > 60:
					print(f"***Change password for {row[0]}***")


