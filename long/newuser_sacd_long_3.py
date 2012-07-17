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
data = cursor.execute("SELECT * FROM tag_1 where `action`='new_user' and time between %s and %s group by user_id ",[starttime, endtime])

dau = data
sec = starttime
today = time.strftime("%Y%m%d",time.localtime())
today = int(today)-int(sys.argv[1])


#吧今天的导入到dau_1的表
ishave = cursor.execute("select id from base_1 where `type` = 'new_user' and `time` = %s",[sec])
if not ishave:
	cursor.execute("insert into base_1 (`num`,`time`,`today`,`type`) values (%s, %s,%s,%s)",[dau,sec,today,'new_user'])
else:
	cursor.execute("update base_1 set `num`=%s where `type` = 'new_user' and `time` = %s",[dau,sec])
cursor.close()
conn.commit()
conn.close()