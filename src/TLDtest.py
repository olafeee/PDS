#!/usr/bin/env python
# PassiveDNSSearcher [PDS]
# version 1.0
# devoleped in Python v3
# tested in Mac OS X Mavericks and UBUNTU 12.04
# born Thursday 27 March 2014 A.D.				  
# made by Olaf Elzinga & Nick de Bruijn Van Melis En Mariekerke	
# real comments are in english. Test comments are in dutch so when we release our tool the dutch comments will be deleted

# log aanmaken met eventueel error

# python standard /// downloaded /// own 
import subprocess, os, time ,sys
import tldextract, pymysql
from database import Database

#log = open('passivedns_test.log','r')
dateLog = '2014-05-01'
storeDB = True

t0 = time.time()
class Pds():
	def __init__(self, db):
		self.db = db

	#map fucntie checke en aanmaken vind ik nog niet super. Later dus nog kijken wat er beter kan ;)
	def passiveDNS_logHandler(self, storeDB = False):
		year = time.strftime("%Y")
		month = time.strftime("%B")
		day = time.strftime("%d")
		mapArchive = "log"

		if not os.path.isdir(mapArchive+"/"+year):
			subprocess.call(["mkdir", mapArchive+"/"+year])

		if not os.path.isdir(mapArchive+"/"+year+"/"+month):
			subprocess.call(["mkdir", mapArchive+"/"+year+"/"+month])
		
		if not os.path.isdir(mapArchive+"/"+year+"/"+month+"/"+day):
			subprocess.call(["mkdir", mapArchive+"/"+year+"/"+month+"/"+day])
			subprocess.call(["cp", "/var/log/passivedns.log", mapArchive+"/"+year+"/"+month+"/"+day+"/"])# change cp for mv
			if storeDB==True:
				print("wel in db opslaan")
				logDir = mapArchive+"/"+year+"/"+month+"/"+day+"/passivedns.log"
				log = open(logDir,'r')
				logHandler = self.domainGathering(log, logDir)
				print(logHandler)

			else:
				print("niet in db opslaan")#err

			if logHandler:
				subprocess.call(["gzip","-S", year+"-"+month+"-"+day+".gz", mapArchive+"/"+year+"/"+month+"/"+day+"/passivedns.log"])

			#gzip -S ".`date +%s`.gz" /var/log/passivedns-archive/passivedns.log 
		else:
			print("map already existststs")#log file eventueel

	def domainGathering(self, log, logDir):
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
		return self.db.insertData(domainList, dateLog, logDir)

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
	pds.passiveDNS_logHandler(storeDB)
	#close session
	db.disconnect()	
	#count time of all funtions
	latestTime=time.time() - t0
	print("time to run",latestTime)



if __name__ == "__main__":	main()