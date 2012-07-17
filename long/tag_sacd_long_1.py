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

today = int(today) - int(sys.argv[1])

if today<10:
	today = '0'+str(today)
	
#hour = time.strftime('%H')
for i in range(1,25):
	if i<10:
		hour = '0'+str(i)
	else:
		hour = str(i)

	gamedir = '/home/jason/game/long/'+year+'/'+month+'/'+str(today)+'/'+hour
	if os.path.isfile(gamedir+'/game.log'):

		fp = open(gamedir+'/game.log','r')

		line = fp.readline()
		while line:
			
			data  = eval(line)

			uid = data['uid']
			action =  data['action']
			num = data['num']
			if 'prop' in data:
				props = data['prop']
			else:
				props = 0

			createtime = data['time']

			sql = "insert into tag_1 (`user_id`,`action`,`num`,`prop`,`time`) values (%s,%s,%s,%s,%s)"
			cursor.execute(sql,[uid,action,num,props,createtime])
			conn.commit()
			line = fp.readline()

cursor.close()
conn.close()

