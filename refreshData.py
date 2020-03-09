from datetime import date

import tushare as ts
import sqlite3
import sys


def getdata():
    try:
        today = sys.argv[1]
    except IndexError:
        today = date.today().strftime('%Y%m%d')
    conn = sqlite3.connect('db')
    pro = ts.pro_api('***ENTER YOUR TUSHARE TOKEN HERE***')
    # Get china data
    if conn.execute(f'select count(1) from nCoV where level=3 and ann_date={today};').fetchone()[0] == 0:
        df = pro.ncov_num(level=3, ann_date=today)
        df.to_sql('nCoV', conn, index=False, if_exists='append')
        print(f'Get new china data {df.shape[0]} rows.')
    else:
        print("Already updated today's china data.")
    # Get provinces detail data
    if conn.execute(f'select count(1) from nCoV where level=4 and ann_date={today};').fetchone()[0] == 0:
        df = pro.ncov_num(level=4, ann_date=today)
        df.to_sql('nCoV', conn, index=False, if_exists='append')
        print(f'Get new provinces detail data {df.shape[0]} rows.')
    else:
        print("Already updated today's provinces detail data.")
    conn.close()


if __name__ == '__main__':
    getdata()
