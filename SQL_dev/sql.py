#!/usr/bin/python
import MySQLdb

conn = MySQLdb.connect(host="localhost", user="root", passwd="lnrddvnc", db="oakTest")

# cursor object
cur = conn.cursor() 

#query = ("INSERT INTO users(name, password_hashed) "
#	"VALUES ('nero','h4shc0de');")

#query = "SELECT * FROM users"

#query = "DROP TABLE stocks"

cur.execute(query)

# print all the first cell of all the rows
for row in cur.fetchall():
	print "nieuwe rij"	
	print row[0]
	print row[1]
	print row[2]

cur.close()
conn.commit()
conn.close()
