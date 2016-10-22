import psycopg2


def db_connect():
    conn = psycopg2.connect(host='localhost',
                            port=5432,
                            database='postgres')

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
