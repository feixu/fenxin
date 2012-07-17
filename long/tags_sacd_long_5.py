#coding:utf-8
import MySQLdb
import sys
import os
import time
#project 1 = long 2 = **

conn = MySQLdb.connect(host='192.168.0.254',user='root',passwd='123456', db='sacd')

cursor = conn.cursor()
year = time.strftime('%Y')
month = time.strftime('%m')
today = time.strftime('%d')
#hour = time.strftime('%H')
#获取时间戳 今天凌晨和第二天凌晨 2012-6-7 2012-6-8
starttime = time.mktime([int(year),int(month),int(today)-int(sys.argv[1]),0,0,0,0,0,0])
endtime = time.mktime([int(year),int(month),int(today)-int(sys.argv[2]),0,0,0,0,0,0])
cursor.execute("SELECT SUM(num) AS num, action FROM `tag_1` where `action` not in ('login','new_user') and time between %s and %s group by action ",[starttime, endtime])
dataall = cursor.fetchall()

sec = starttime
today = time.strftime("%Y%m%d",time.localtime())
today = int(today)-int(sys.argv[1])
if today<10:
	today
sql=''
if dataall:
	
	params=[]
	for val in dataall:
		params.append(int(val[0]))
		params.append(val[1])
		params.append(int(sec))
		params.append(today)
		sql += "(%s,%s,%s,%s),"

if sql:
	
	sql = sql[0:-1]
	cursor.execute("insert into tags_1 (`num`,`tag`,`time`,`today`) values "+sql, params)
	cursor.close()
	conn.commit()
	conn.close()