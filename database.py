import pymysql

class Database():
	def __init__(self):
		self.connected = False

	def toggleconnect(self):
		if(self.connected):
			self.disconnect()
			print("closed")
		else:
			self.connect()
			print("connect")

	def connect(self):
		self.conn = pymysql.connect(host='127.0.0.1',port=3306 , user='pyPDS', passwd='henkjan', db='PDS')
		self.cur = self.conn.cursor()

	def disconnect(self):
		self.cur.close()
		self.conn.close()

	def getInfo(self, stmnt, arg = None):
		if arg == None:
			self.cur.execute(stmnt)
		else:
			self.cur.execute(stmnt, arg)

		return self.cur.fetchall()

	# insert all domain from a log into the MySQL DB
	# @domainList 
	def insertData(self, domainList, dateLog, logFile):
		y = 0
		#INSERT
		InsertStmt = "INSERT INTO Domainlist (domain, date, logfile, count) VALUES (%s,%s,%s,%s)"
		InsertDate = "INSERT INTO Date_list (Date, Domain_count) VALUES (%s,%s)"
		#UPDATE
		UpdateStmt = "UPDATE Domainlist SET count = %s WHERE domain = %s and date = %s"
		UpdateDomain_count = "UPDATE Date_list SET Domain_count = %s WHERE date = %s"

		try:
			x = self.getInfo("SELECT Domain_count FROM Date_list")[0][0]
			print("x is",x)
		except:
			self.cur.execute(InsertDate, ('2014-05-01', 0))
			x = 0
			print("x is",x)

		for item in domainList.items():	
			try:
				self.cur.execute(InsertStmt, (item[0], dateLog, logFile, item[1]))
				y+=1
			except:
				domainDateExists = self.getInfo("SELECT count FROM Domainlist WHERE domain = %s and date = %s", (item[0] , dateLog))
				if domainDateExists:
					self.cur.execute(UpdateStmt, (item[1] + domainDateExists[0][0], item[0], dateLog))
					y+=1
				else:
					print("is dure ding")

		print("y is", y)
		self.cur.execute(UpdateDomain_count, (x+y, '2014-05-01'))
		#self.cur.executemany(stmt, domainList.items())
		self.conn.commit()

	def deleteData(self):
		print("oei")
#kan eventueel weg
	def insertData1(self, domainList):
		stmt = "INSERT INTO Domainlist (domain, date, logfile, count) VALUES (%s,'2014-05-01' , 'logfile.log' , %s)"
		self.cur.executemany(stmt, domainList.items())
		self.conn.commit()
		#print(domainList)