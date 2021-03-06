#!/usr/bin/python
import MySQLdb
import bcrypt
import sys

# choose from {end_develop,backtest_develop,end_real,backtest_real}
# corresponding backup database will also be resetted
dataBaseToReset = "backtest_real";

# if you are about to reset a non-develop database, please enter the password below 
# AND CLEAR PASSWORD AGAIN BEFORE SAVING THE SCRIPT AFTER LAST USE
password = "guikwwdplnvccbsitkhr";

# hashed password to validate password
hashedPassword = "$2b$12$Zc4Tc1EYEhdAbYVT0xhlouHsZKA6NO7EybtVe8wfsc6AAjkPR6MNK";

if dataBaseToReset ==  "end_real" or dataBaseToReset == "backtest_real":
	if bcrypt.hashpw(password, hashedPassword) == hashedPassword:
		print("Password validated, " + dataBaseToReset + " database will now be reset.")
	else:
		sys.exit("Invalid password, script terminated.")
else: 
	print(dataBaseToReset + " database will now be reset.")


conn = MySQLdb.connect(host="localhost", user="root", passwd="crvfttngdsntwrk")

# cursor object
cur = conn.cursor() 

# tables


query = "DROP DATABASE IF EXISTS " + dataBaseToReset + "; "

query += "CREATE DATABASE " + dataBaseToReset + "; "

query += "USE " + dataBaseToReset + "; "

query += ("CREATE TABLE portfolio("
	"id int NOT NULL AUTO_INCREMENT,"
	"name varchar(30) UNIQUE NOT NULL,"
	"capital int NOT NULL,"
	"PRIMARY KEY (id));")

query += ("CREATE TABLE user("
	"id int NOT NULL AUTO_INCREMENT,"
	"name varchar(30) NOT NULL UNIQUE,"
	"passwordHashed varchar(100),"
	"PRIMARY KEY (id));")

query += ("CREATE TABLE stock("
	"id int NOT NULL AUTO_INCREMENT,"
	"name varchar(50) NOT NULL,"
	"ticker varchar(30) NOT NULL UNIQUE,"
	"PRIMARY KEY (id));")

query += ("CREATE TABLE stockCategory("
	"id int NOT NULL AUTO_INCREMENT,"
	"stock int NOT NULL,"
	"criterium varchar(20) NOT NULL,"
	"value varchar(30) NOT NULL,"
	"FOREIGN KEY (stock) REFERENCES stock(id),"
	"PRIMARY KEY (id));")

query += ("CREATE TABLE method("
	"id int NOT NULL AUTO_INCREMENT,"
	"name varchar(20) NOT NULL UNIQUE,"
	"description varchar(150),"
	"PRIMARY KEY (id));")

query += ("CREATE TABLE strategy("
	"id int NOT NULL AUTO_INCREMENT,"
	"name varchar(20) NOT NULL UNIQUE,"
	"method int NOT NULL,"
	"isActive boolean NOT NULL DEFAULT TRUE,"
	"parameters varchar(100) NOT NULL DEFAULT '',"
	"FOREIGN KEY (method) REFERENCES method(id),"
	"PRIMARY KEY (id));")

query += ("CREATE TABLE strategyEditHistory("
	"id int NOT NULL AUTO_INCREMENT,"
	"strategy int NOT NULL,"
	"editor int NOT NULL,"
	"timestamp TIMESTAMP NOT NULL DEFAULT NOW(),"
	"newParameters varchar(100) NOT NULL DEFAULT '',"
	"FOREIGN KEY (strategy) REFERENCES strategy(id),"
	"FOREIGN KEY (editor) REFERENCES user(id),"
	"PRIMARY KEY (id));")

# TODO winst op deze transactie toevoegen aan transaction? 

if dataBaseToReset == "end_develop" or dataBaseToReset == "end_real":

	query += ("CREATE TABLE transaction("
		"id int NOT NULL AUTO_INCREMENT,"
		"stock int NOT NULL,"
		"isBuy boolean NOT NULL,"
		"numOfStock int NOT NULL,"
		"timestamp TIMESTAMP NOT NULL DEFAULT NOW(),"
		"operator int NOT NULL,"
		"price float NOT NULL,"
		"transactionCost float NOT NULL,"
		"portfolio int NOT NULL,"
		"FOREIGN KEY (stock) REFERENCES stock(id),"
		"FOREIGN KEY (operator) REFERENCES user(id),"
		"FOREIGN KEY (portfolio) REFERENCES portfolio(id),"
		"PRIMARY KEY (id));")

if dataBaseToReset == "backtest_develop" or dataBaseToReset == "backtest_real":

	query += ("CREATE TABLE simulation("
		"id int NOT NULL AUTO_INCREMENT,"
		"name varchar(30) NOT NULL UNIQUE,"
		"description varchar(60) NOT NULL DEFAULT '',"
		"owner int NOT NULL,"
		"strategy int NOT NULL,"
		"timestampStart TIMESTAMP NOT NULL DEFAULT NOW()," # TODO ook datetime maken? en ook checken voor de rest van script
		"timestampEnd DATETIME," # er kan maar 1 fiel zijn met als default NOW()
		"totalGain float,"
		"totalReturn float," # return is een reserved word in SQL
		"status varchar(8) NOT NULL,"
		"PID int,"
		"progress int NOT NULL DEFAULT 0,"
		"FOREIGN KEY (strategy) REFERENCES strategy(id),"
		"FOREIGN KEY (owner) REFERENCES user(id),"
		"PRIMARY KEY (id));")

query += ("CREATE TABLE webAppLoginHistory("
	"id int NOT NULL AUTO_INCREMENT,"	
	"succeeded boolean NOT NULL DEFAULT TRUE,"
	"user int NOT NULL,"
	"timestamp TIMESTAMP NOT NULL DEFAULT NOW(),"
	"FOREIGN KEY (user) REFERENCES user(id),"
	"PRIMARY KEY (id));")

query += ("CREATE TABLE dataStatus("
	"id int NOT NULL AUTO_INCREMENT,"	
	"script varchar(50) NOT NULL,"
	"description varchar(100),"
	"lastUpdated TIMESTAMP,"
	"PRIMARY KEY (id));")

# views
# spaties nodig na elke regel in query string!

if dataBaseToReset == "end_develop" or dataBaseToReset == "end_real":

	query += ("CREATE VIEW wallet AS "
		"SELECT STK.ticker, STK.name AS stockName, (SUM(TCN_BUY.numOfStock)-SUM(TCN_SELL.numOfStock)), STK.market, PTF.name AS portfolioName " 
		"FROM portfolio PTF, stock STK, transaction TCN_BUY, transaction TCN_SELL "
		"WHERE TCN_BUY.isBuy = 1 "
		"AND STK.id = TCN_BUY.stock "
		"AND STK.id = TCN_SELL.stock "
		"AND TCN_SELL.isBuy = 0 "
		"AND TCN_BUY.portfolio = PTF.id " 
		"AND TCN_SELL.portfolio = PTF.id;")

# TODO statistics view toevoegen

cur.execute(query)
cur.close()
conn.commit()
conn.close()

print("Done")
