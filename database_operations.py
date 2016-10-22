import general_utils as Ugen
import psycopg2


def db_connect():
    login = Ugen.ConfigSectionMap('db')
    conn = psycopg2.connect(host='ec2-54-164-197-93.compute-1.amazonaws.com',
                            port=5432,
                            database='dfs',
                            user=login['user'],
                            password=login['password'])

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
