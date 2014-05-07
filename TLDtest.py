#!/usr/bin/env python
# PassiveDNSSearcher [PDS]
# version 1.0
# devoleped in Python v3
# tested in Mac OS X Mavericks and UBUNTU 12.04
# born Thursday 27 March 2014 A.D.				  
# made by Olaf Elzinga & Nick de Bruijn Van Melis En Mariekerke	

import sys, collections

import subprocess
import tldextract, pymysql
import time, datetime
from database import Database

#log = open('passivedns_test.log','r')
dateLog = '2014-05-01'
logFile = 'test.log'
log = open(logFile,'r')

t0 = time.time()
class Pds():
	def __init__(self, db):
		self.db = db

	def passiveDNS_logHandler(self):
		print(date(year))
		subprocess.call(["df","-h"])

	def domainGathering(self):
		#make a list to store all domains
		data = self.db.getInfo("SELECT * FROM Domainlist")
		domainList={}
		#take al domains and place in the list "domainList"
		for line in log:
			array = (line.split('||')) #split each line get from passiveDNS logf ile
			#Top Level Domain [TLD]
			tld = tldextract.extract(array[4])
			tldsuffix = tld.suffix
			tld = tld.domain + '.' + tldsuffix
			if not tldsuffix:
				tld = "not existing"
			self.fillList(domainList, str(tld))
		self.db.insertData(domainList, dateLog, logFile)

	def fillList(self, x, y):
		if y not in x:
			x[y] = 1
		else:
			x[y] += 1

def main():
	#open session
	db = Database()
	db.toggleconnect()
	#act
	pds = Pds(db)
	pds.passiveDNS_logHandler()
	#pds.domainGathering()
	#close session
	db.disconnect()	
	#count time of all funtions
	latestTime=time.time() - t0
	print("time to run",latestTime)



if __name__ == "__main__":	main()