## ARDA Application released on: April 21, 2017
## Last review: February 19, 2018
## Author: Roderick Fanou


def count_number_days(date1, date2):
    date_beg = datetime.strptime(date1, "%d/%m/%Y")
    date_end = datetime.strptime(date2, "%d/%m/%Y")

    print('Date =', date_beg, date_end)

    if date_beg <= date_end:

        delta = date_end - date_beg

        periodd = delta.days  # that's it

        return periodd

    else:

        return 'impossible'


from datetime import datetime
import sys, MySQLdb

## This script is run daily. => put it in the cron for everyday at 1 am, 9 am and 5pm (17h)

## import all files in the library you need
sys.path.append('../2_libraries/')
from functions import *


def Check_tables_for_insertions(database):
    import datetime
    Current_db = database

    ## connect to the DB
    db = MySQLdb.connect(host="localhost", user="", passwd="", db=Current_db)
    cur = db.cursor()
    print('Connected')

    # Create a datetime object with today's value
    today = datetime.datetime.today()

    # print today's date in YYYY-MM-DD format
    value1 = datetime.datetime.strftime(today, '%d-%m-%Y')
    tab = value1.split('-')
    table1 = 'Data__' + str(int(tab[2])) + '_' + str(int(tab[1]))

    # add one day to today's date
    tomorrow = today + datetime.timedelta(1)

    # print tomorrow's date in YYYY-MM-DD format
    value2 = datetime.datetime.strftime(tomorrow, '%d-%m-%Y')
    tab = value2.split('-')
    table2 = 'Data__' + str(int(tab[2])) + '_' + str(int(tab[1]))

    Original_table = 'Data__2003_1'

    print(table1, table2)

    ## Check if today table exists

    stmt = "SHOW TABLES LIKE '" + table1 + "'"
    print(stmt)
    cur.execute(stmt)
    result = cur.fetchone()
    print(result)
    if result:
        # there is a table for today
        print('the table ', table1, ' exists')

    else:
        # there is no table for today; create it
        print('the table ', table1, ' does not exist')

        stmt = """CREATE TABLE """ + table1 + """ LIKE """ + Original_table;
        cur.execute(stmt)

    stmt = "SHOW TABLES LIKE '" + table2 + "'"
    print(stmt)
    cur.execute(stmt)
    result = cur.fetchone()
    print(result)
    if result:
        # there is a table for today
        print('the table ', table2, ' exists')

    else:
        # there is no table for today; create it
        print('the table ', table2, ' does not exist')

        stmt = """CREATE TABLE """ + table2 + """ LIKE """ + Original_table;
        cur.execute(stmt)


Check_tables_for_insertions('MergedData_backup')
