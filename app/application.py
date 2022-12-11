import cx_Oracle
import time
import kopf
import kubernetes
import yaml
import os
from environs import Env
from kubernetes.client.rest import ApiException
from pprint import pprint
import datetime
import random
import asyncio

# setting missing variables
try:
  USER = os.environ['USER']
except:
  USER="demopython"
  logger.info(f"USER  is not set, using {USER}s as demopython")

try:
  PASSWORD = os.environ['PASSWORD']
except:
  PASSWORD="XXXXX"
  logger.info(f"PASSWORD is not set, using {PASSWORD} as XXXXX")


try:
  DSN = os.environ['DSN']
except:
  DSN="localhost/xepdb1"
  logger.info(f"DSN  is not set, using {DSN} as XXXXX")


try:
  SQL = os.environ['SQL']
except:
  SQL="select * from dual;"
  logger.info(f"SQL  is not set, using {SQL} as SQL")


try:
  LOOP_COUNT = int(os.environ['LOOP_COUNT'])
except:
  LOOP_COUNT=10
  logger.info(f"Variable LOOP_COUNT is not set, using {LOOP_COUNT} as default")    


connection = cx_Oracle.connect(
    user=USER,
    password=PASSWORD,
    dsn=DSN)

print("Successfully connected to Oracle Database")


# Obtain a cursor
cursor = connection.cursor()


for a in range(LOOP_COUNT):

    # Execute the query
    sql = SQL
    cursor.execute(sql)

    # Loop over the result set
    for row in cursor:
        print(row)

exit (0) 


# Create a table

cursor.execute("""
    begin
        execute immediate 'drop table todoitem';
        exception when others then if sqlcode <> -942 then raise; end if;
    end;""")

cursor.execute("""
    create table todoitem (
        id number generated always as identity,
        description varchar2(4000),
        creation_ts timestamp with time zone default current_timestamp,
        done number(1,0),
        primary key (id))""")

# Insert some data

rows = [ ("Task 1", 0 ),
         ("Task 2", 0 ),
         ("Task 3", 1 ),
         ("Task 4", 0 ),
         ("Task 5", 1 ) ]

cursor.executemany("insert into todoitem (description, done) values(:1, :2)", rows)
print(cursor.rowcount, "Rows Inserted")

connection.commit()

# Now query the rows back
for row in cursor.execute('select description, done from todoitem'):
    if (row[1]):
        print(row[0], "is done")
    else:
        print(row[0], "is NOT done")
