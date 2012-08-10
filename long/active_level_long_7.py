import MySQLdb
import sys
import os
import time
import datetime

conn = MySQLdb.connect(host='192.168.0.254',user='root',passwd='123456', db='sacd')
#conn = MySQLdb.connect(host='localhost',user='root',passwd='chenbo', db='sacd')

cursor = conn.cursor()
year = time.strftime('%Y')
month = time.strftime('%m')
day = time.strftime('%d')

today = time.strftime('%Y-%m-%d')
# yesterday = time.strftime('%Y-%m-%d',[int(year),int(month),int(day)-int(sys.argv[1]),0,0,0,0,0,0])

#yesterday 00:00:00 to today 00:00:00
starttime = time.mktime([int(year),int(month),int(day)-int(sys.argv[1]),0,0,0,0,0,0])
endtime = time.mktime([int(year),int(month),int(day)-int(sys.argv[2]),0,0,0,0,0,0])

yesterday = time.strftime("%Y-%m-%d",time.localtime(endtime))

cursor.execute("SELECT `user_id` FROM  `tag_1` WHERE `time`>%s and `time`<=%s and \
                    `action`='login' ",[starttime,endtime])
TemUserlogin=cursor.fetchall ()
# print TemUserlogin
insertData=str(sorted(list(set(j[0] for j in TemUserlogin))))
# print starttime
# print endtime
strinsertData=insertData.replace(' ','')
strinsertData=insertData.replace('L','')
#print(strinsertData)
cursor.execute("insert into active_level_1 (`date`,`active`) values (%s,%s)",[yesterday,strinsertData])
cursor.close ()
conn.commit()
conn.close()