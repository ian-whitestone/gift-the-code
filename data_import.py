import xlrd
import os
import datetime
import database_operations as dbo
import locations
import json

def read_data(src):
    data = []
    str_input = open(os.path.join('data', src), 'rb').read()
    wb = xlrd.open_workbook(file_contents=str_input)
    sheet = wb.sheets()[0]
    for row in range(sheet.nrows):
        values = []
        for col in range(sheet.ncols):
            values.append(sheet.cell(row, col).value)
        data.append(values)
    return data


def parse_timestamp(s):
    try:
        h, m = s.split(":")
        h = int(h)
        m = int(m)
        if h < 8:
            h += 12
        return datetime.time(hour=h, minute=m)
    except:
        return None


def parse_date(s):
    return datetime.datetime.strptime('1900-01-01', '%Y-%m-%d') + datetime.timedelta(days=int(s))


def parse_data_dict(data, header=True, fields=None):
    row_skip = 0
    if header:
        row_skip += 1
        fields = tuple(data[0])
    else:
        fields = tuple(fields)
    all_data = []
    for d in data[row_skip:]:
        dd = dict(zip(fields, tuple(d)))
        source = dd['stop_type'].split("|")
        dd['stop_type'] = source[0].strip()
        dd['source_type'] = None
        dd['stop_id'] = int(dd['stop_id'].strip())
        if len(source) > 1:
            dd['source_type'] = source[1].strip()
        all_data.append(dd)
    return all_data


def parse_data(data):
    ints = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12,
            13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
    data2 = [tuple([d[i] for i in ints]) for d in data]

    data3 = []
    for data in data2[1:]:
        tup = ()
        for i, d in enumerate(data):
            if i == 0:
                tup += (parse_date(d),)
            elif i == 3:
                ss = d.split('|')
                if len(ss) > 1:
                    tup += (ss[0].strip(), ss[1].strip())
                else:
                    tup += (ss[0].strip(), None)
            elif i in [6, 7]:
                tup += (parse_timestamp(d),)
            else:
                if isinstance(d, str):
                    tup += (d.strip(),)
                else:
                    tup += (d,)
        data3.append(tup)
    return data3


def main():
    conn = dbo.db_connect()
    src_files = [f for f in os.listdir('data') if f[-1] in 'Xx']
    for src in src_files:
        ###read in and parse excel data
        data = read_data(src)
        parsed_data = parse_data(data)  # list of tuples

        # ##insert delivery.pickup data into 'data' table
        # query = 'INSERT INTO data VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        # dbo.insert_query(conn, query, parsed_data, True)

        ###get location data from google geocode api
        ##read existing postal_codes
        query="SELECT postcode FROM postal"
        historized_pcs=[result[0] for result in dbo.select_query(conn,query)]

        ##get postal_codes thats havent been historized already
        postal_codes=list(set([data[-1] for data in parsed_data if data[-1] not in historized_pcs]))
        location_data={postal_code:locations.get_location_data(postal_code) for postal_code in postal_codes}
        location_dict=locations.parse_location_data(location_data)

        ##insert new location data into 'postal' table
        if location_dict:
            loc_data=[(k,v['longitude'],v['latitude'],v['neighborhood'],v['locality']) for k,v in location_dict.items()]
            query = 'INSERT INTO postal VALUES (%s,%s,%s,%s,%s)'
            dbo.insert_query(conn, query, loc_data, True)
            print('%s records historized' % len(loc_data.keys()))
        else:
            print ('nuttin historized')
    conn.close()
    return parsed_data


def loc_hist_test():
    conn = dbo.db_connect()
    with open('loc_data.json', 'r') as fp:
        location_dict = json.load(fp)

    loc_data=[(k,v['longitude'],v['latitude'],v['neighborhood'],v['locality']) for k,v in location_dict.items()]
    query = 'INSERT INTO postal VALUES (%s,%s,%s,%s,%s)'
    dbo.insert_query(conn, query, loc_data, True)
    conn.close()
    return

if __name__ == '__main__':
    main()




# TO DO
# raise exception if columns are not matching expected type
# add instructions (i.e. info must be in sheet 0)
