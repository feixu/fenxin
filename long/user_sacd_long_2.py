#coding:utf-8
import MySQLdb
import sys
import os
import time
#project 1 = 龙的收藏 2 = **

conn = MySQLdb.connect(host='192.168.0.254',user='root',passwd='123456', db='sacd')
cursor = conn.cursor()

cursor.execute("set names utf8")
conn.commit()

year = time.strftime('%Y')
month = time.strftime('%m')
today = time.strftime('%d')

today = int(today) - int(sys.argv[1])

if today<10:
	today = '0'+str(today)

gamedir = '/home/jason/game/long/'+year+'/'+month+'/'+str(today)
if os.path.isdir(gamedir):

	dirs = os.listdir(gamedir)
	for files in dirs:
		if os.path.isfile(gamedir+'/'+files):
			fp = open(gamedir+'/'+files,'r')
			line = fp.readline()
			while line:
				
				data  = eval(line)

				uid = data['uid']
				name = data['name']
				level = data['level']
				sex =  data['sex']
				cash = data['cash']
				mcash = data['mcash']

				sql = "select user_id from user_1 where `user_id` = %s"
				count = cursor.execute(sql,uid)
				if count:
					sql = "update user_1 set `level` = %s, `cash` = %s, `mcash` = %s where `user_id`= %s"
					cursor.execute(sql,[level, cash, mcash, uid])
				else:
					sql = "insert into user_1 (`user_id`,`name`,`level`,`sex`,`cash`,`mcash`) values (%s,%s,%s,%s,%s,%s)"
					cursor.execute(sql,[uid, name, level, sex, cash, mcash])

				conn.commit()
				line = fp.readline()


cursor.close()
conn.close()

