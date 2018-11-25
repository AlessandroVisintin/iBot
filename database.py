import sys
import sqlite3
from sqlite3 import Error

# Database name
DB_NAME = 'iBot.db'

class Database(object):
	'''
	Manage the database of account-names gathered.
	Every table contains people that are likely to prefer
		a defined argument, given by the table-name.
	Every table is composed by four columns:
	N | F | M | L

	N: account name
	F: have we already collected the followers/following of this account? (y/n)
	M: have we already sent a private message to this account? (y/n)
	L: have we already liked some photos of this account? (y/n)
	'''

	def __init__(self, tb_name):
		'''
		Initialize a connection to a table inside the database

		:type tb_name: string
		:param tb_name: table to connect
		'''
		try:
			self.tb = tb_name
			self.con = sqlite3.connect(DB_NAME)

			if not self.tb in self.table_names():
				r = raw_input(
						('{} doesn\'t exists yet. '
						'Do you want to create it? '
						'(y/n) -> ').format(self.tb)) 
				if r == 'y':
					if not self._exe_sql( 
						('create table if not exists {} '
						'(n text PRIMARY KEY, '
						'f text NOT NULL, '
						'm text NOT NULL, '
						'l text NOT NULL)').format(self.tb)):
						sys.exit()
				else:
					sys.exit()	
		except Error as e:
			print(e)
			sys.exit()

	def __del__(self):
		''' 
		Close the connection before deleting the object 
		'''
		self.commit()
		self.con.close()

	def _exe_sql(self, query):
		'''
		Execute the sql statement inside the database.

		:type query: string
		:param query: sql statement to execute
		:rtype: SQLite Cursor object
		:return: SQLite Cursor object if operation has gone well,
			an empty list otherwise.
		'''
		try:
			c = self.con.cursor()
			c.execute(query)
			return c
		except Error as e:
			print(e)
			return []

	def commit(self):
		"""
		Commit all the queries done. Important to save results!!!
		"""
		self.con.commit()

	def table_names(self):
		"""
		Return list of tables inside the database
		"""
		q = 'select name from sqlite_master where type="table"'
		c = self._exe_sql(q)
		if not c:
			return c

		r = []
		for i in c.fetchall(): 
			r.append(i[0])
		return r

	def count(self):
		'''
		Count number of rows inside the table.
		'''
		q = 'select Count() from {}'.format(self.tb)
		c = self._exe_sql(q)
		if not c:
			return c
		return c.fetchone()[0]

	def all(self):
		"""
		Select all rows inside table

		:rtype: list
		:return: list containing the requested entry, 
			an empty list otherwise
		"""
		q = 'select * from {}'.format(self.tb)
		c = self._exe_sql(q)
		if not c:
			return c 
		return c.fetchall()

	def _by_one_column(self, column, value):
		"""
		Select accounts by value of column

		:type column: string
		:param column: column in which to find value
		:type value: string
		:param value: value to search for inside column
		:rtype: list
		:return: list containing the requested entry, 
			an empty list otherwise
		"""
		q = "select * from {} where {} = '{}'".format(self.tb, column, value)
		c = self._exe_sql(q)
		if not c:
			return c 
		return c.fetchall()

	def by_name(self, name):
		"""
		Select an account by name inside the table

		:type name: string
		:param name: account name to find inside the table
		:rtype: list
		:return: list containing the requested entry,
			an empty list otherwise
		"""
		return self._by_one_column('n', name)

	def by_follow(self, value):
		return self._by_one_column('f', value)

	def by_message(self, value):
		return self._by_one_column('m', value)

	def by_like(self, value):
		return self._by_one_column('l', value)

	def _update_one_column(self, name, column, value):
		"""
		Update one column of name using value

		:type name: string
		:param name: account to update
		:type column: string
		:param column: column to update
		:type value: string
		:param value: value to search for inside column
		:rtype: bool
		:return: True if operation has gone well, False otherwise
		"""
		q = "update {} set {} = '{}' where n = '{}'".format(self.tb, column, value, name)
		self._exe_sql(q)

	def up_follow(self, name, value):
		self._update_one_column(name, 'f', value)

	def up_msg(self, name, value):
		self._update_one_column(name, 'm', value)

	def up_like(self, name, value):
		self._update_one_column(name, 'l', value)

	def insert(self, name, follow='n', msg='n', like='n'):
		"""
		Insert a new entry inside the table

		:type name: string
		:param name: name of account
		:type follow: string
		:param follow: value for follow (y/n)
		:type msg: string
		:param msg: value for msg (y/n)
		:type like: string
		:param like: value for like (y/n)
		"""
		q = "insert or ignore into {}(n,f,m,l) values('{}','{}','{}','{}')".format(
			self.tb, 
			name, 
			follow, 
			msg, 
			like
		)
		self._exe_sql(q)

	def insert_many(self, name_list):
		"""
		Insert multiple entry inside the table

		:type name_list: string
		:param name_list: list of names to add with default values
		"""
		q = "insert or ignore into {}(n,f,m,l) values".format(self.tb)
		l = len(name_list)
		for i in range(l - 1):
			q += u"('{}','n','n','n'),".format(name_list[i])
		q += u"('{}','n','n','n');".format(name_list[l-1])
		self._exe_sql(q)

	def delete(self, name):
		"""
		Delete a row from the table

		:type name: string
		:param name: name of account
		"""
		q = "delete from {} where n = '{}'".format(self.tb, name)
		self._exe_sql(q)

if __name__ == '__main__':
	n = raw_input("Write table to open -> ")
	db = Database(n)
	print("You are connected to table {}".format(n))
	print("Variable 'db' ready to use")