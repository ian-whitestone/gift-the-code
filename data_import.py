import xlrd
import xlsxwriter
import os
import datetime
import pandas as pd
import database_operations as dbo


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


def parse_data_mod(data):
    ints = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12,
            13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
    data2 = [tuple([d[i] for i in ints]) for d in data]
    data3 = []
    for j, data in enumerate(data2[1:]):
        entry = []
        for i, d in enumerate(data):
            if i == 0:
                entry.append(parse_date(d))
            elif i == 3:
                ss = d.split('|')
                if len(ss) > 1:
                    entry.append(ss[0].strip())
                    entry.append(ss[1].strip())
                else:
                    entry.append(ss[0].strip())
                    entry.append(None)
            elif i in [6, 7]:
                entry.append(parse_timestamp(d))
            else:
                if isinstance(d, str):
                    entry.append(d.strip())
                else:
                    entry.append(d)
        data3.append(entry)
    return data3


def main():
    src_files = [f for f in os.listdir('data') if f[-1] in 'Xx']
    for src in src_files:
        data = read_data(src)
        parsed_data = parse_data(data)  # list of tuples
        conn = dbo.db_connect()
        query = 'INSERT INTO data VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        dbo.insert_query(conn, query, parsed_data, True)
    return parsed_data

# data=main()
#
# headers=['date', 'trans_type', 'route_desc', 'stop_type','source_type','driver', 'donor_id', 'arrive', 'depart', 'bread', 'baked', 'dairy', 'produce', 'protein', 'prepared', 'bev_juice', 'bev_other', 'snack', 'non_perish', 'non_food', 'quality', 'zero_lbs', 'postcode']
# # headers=data.pop(0)
# df=pd.DataFrame(data, columns=headers)
# print(df.head())
# TO DO
# raise exception if columns are not matching expected type
# add instructions (i.e. info must be in sheet 0)
