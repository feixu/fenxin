import MySQLdb
import sys
import os
import time
import datetime

conn = MySQLdb.connect(host='192.168.0.254',user='root',passwd='123456', db='sacd')
cursor = conn.cursor()
year = time.strftime('%Y')
month = time.strftime('%m')
day = time.strftime('%d')

today = time.strftime('%Y-%m-%d')
yesterday = time.strftime('%Y-%m-%d',[int(year),int(month),int(day)-int(sys.argv[1]),0,0,0,0,0,0])

#yesterday 00:00:00 to today 00:00:00
starttime = time.mktime([int(year),int(month),int(day)-int(sys.argv[1]),0,0,0,0,0,0])
endtime = time.mktime([int(year),int(month),int(day)-int(sys.argv[2]),0,0,0,0,0,0])

#get records already exist in database
cursor.execute("select * from customer_loyalty_1",[])
oldrecords=cursor.fetchall ()
databaserecords={i[1]:[i[2],i[3],i[4]] for i in oldrecords}

#get register data of yesterday
cursor.execute("select * from tag_1 where `action` = 'new_user' and `time` between  %s and %s",[starttime, endtime])
newrecords=cursor.fetchall ()

sqldata=[[rec[1],yesterday,yesterday,0] for rec in newrecords]

for i in sqldata:
    #no covered and no repreat
    #if i[0] in databaserecords:
    #i[0]=user_id

    #    continue;
    cursor.execute("insert into customer_loyalty_1 (`user_id`,`register_date`,`latest_login_date`,`loyal_dates`) values (%s,%s,%s,%s)",i)
    
cursor.close ()
conn.commit()

'''
update 'latest_login_date' and 'loyal_dates'
'''
#get login data of yesterday
cursor = conn.cursor()
cursor.execute("select * from tag_1 where `action` = 'login' and `time` between  %s and %s",[starttime, endtime])
loginrecords=cursor.fetchall ()
newloginrecords={i[1]:i[5] for i in loginrecords}

updaterecords={}
for i in newloginrecords:
    if i in databaserecords:
        t = time.localtime(newloginrecords[i])#time.strptime(newloginrecords[i], "%Y-%m-%d")
        y,m,d = t[0:3]
        updaterecords[i]=[datetime.date(y,m,d),(datetime.date(y,m,d)-databaserecords[i][0]).days]
        #to insert latest_login_date and loyal_dates of YesterdayLOGIN
        #and neglect users registered before 2012-07-23
        

        #cursor.execute("update customer_loyalty_1 set `latest_login_date` = %s , `loyal_dates` = %s where `user_id` = %s",[updaterecords[i][0], updaterecords[i][1],i])
        #print [i,"%s-%s-%s"%(databaserecords[i][0].year,databaserecords[i][0].month,databaserecords[i][0].day),updaterecords[i][0], updaterecords[i][1]]
        cursor.execute("insert into customer_loyalty_1 (`user_id`,`register_date`,`latest_login_date`,`loyal_dates`) values (%s,%s,%s,%s)",[i,"%s-%s-%s"%(databaserecords[i][0].year,databaserecords[i][0].month,databaserecords[i][0].day),updaterecords[i][0], updaterecords[i][1]])


cursor.close ()
conn.commit()
conn.close()