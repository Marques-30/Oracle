import time 
import os
import sys
import getpass
import platform
import cx_Oracle

if __name__ == "__main__":

    name = raw_input("Enter Lan ID ")
    HC_ID = raw_input("Enter HC_ID ")
    BATCH = raw_input("Enter BATCH_ID ")

#os.startfile('"C:\TEMP\putty\putty.exe"')
#putty = putty.exe
#if putty:
#	print "etlt1.bankofthewest.com"

SQL = "SELECT HC_ID, BATCH_ID, HC_REPORT FROM AUDITDATA.HC_RUN WHERE HC_ID = 5510501 AND BATCH_ID = 551 ;"

print ("Python version: " + platform.python_version())
print ("cx_Oracle version: " + cx_Oracle.version)
print ("Oracle client: " + str(cx_Oracle.clientversion()).replace(', ','.'))

pwd = getpass.getpass()
connection = cx_Oracle.connect(''+name+'@TEDW/etlt1.bankofthewest.com')

print ("Oracle DB version: " + connection.version)
print ("Oracle client encoding: " + connection.encoding)

print 'sqlplus'
print SQL

import conval
time.sleep(60)
connection.close()