import psycopg2
import datetime


def db_connect():
    conn = psycopg2.connect(database='postgres',
                            user='centos')
    return conn


def insert_query(conn, query, data, multiple):
    cur = conn.cursor()
    if multiple:  # data is a list of tuples
        cur.executemany(query, data)
    else:  # data is a single tuple
        cur.execute(query, data)
    conn.commit()
    cur.close()
    return


def insert_dict_query(conn, query, data, fields, multiple):
    cur = conn.cursor()
    tuples = [tuple([d[field] for field in fields]) for d in data]
    if multiple:  # data is a list of tuples
        cur.executemany(query, tuples)
    else:  # data is a single tuple
        cur.execute(query, tuples)
    conn.commit()
    cur.close()
    return


def execute_query(conn, query, data=False):
    cur = conn.cursor()
    cur.execute(query, data)
    conn.commit()
    cur.close()
    return


def select_query(conn, query, data=False):
    cur = conn.cursor()
    if data:  # data is a single tuple
        if not isinstance(data, tuple):
            data = (data,)
        cur.execute(query, data)
        resultset = cur.fetchall()
    else:
        cur.execute(query)
        resultset = cur.fetchall()
    cur.close()
    return resultset


def parse_date(s):
    return datetime.datetime.strptime('1900-01-01', '%Y-%m-%d') + datetime.timedelta(days=int(s))


def parse_time(s):
    h, m = s.split(":")
    h = int(h)
    m = int(m)
    if h < 8:
        h += 12
    return datetime.time(hour=h, min=m)
