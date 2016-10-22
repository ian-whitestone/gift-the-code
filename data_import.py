import xlrd
import xlsxwriter
import os
import datetime


def read_data(src):
    data =[]
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

def parse_data(data):
    ints=[0,1,2,3,4,5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
    data2=[tuple([d[i] for i in ints]) for d in data]

    data3=[]
    for data in data2[1:]:
        tup=()
        for i,d in enumerate(data):
            if i==0:
                tup+=(parse_date(d),)
            elif i==3:
                ss=d.split('|')
                if len(ss)>1:
                    tup+=(ss[0].strip(),ss[1].strip())
                else:
                    tup+=(ss[0].strip(),None)
            elif i in [6,7]:
                tup+=(parse_timestamp(d),)
            else:
                if isinstance(d,str):
                    tup+=(d.strip(),)
                else:
                    tup+=(d,)
        data3.append(tup)
    return data3


def main():
    src_files = [f for f in os.listdir('data') if f[-1] in 'Xx']

    for src in src_files:
        data=read_data(src)
        parsed_data=parse_data(data)
        print (len(parsed_data))
        print (parsed_data[1])
        break
    return

main()

###TO DO
##raise exception if columns are not matching expected type
##add instructions (i.e. info must be in sheet 0)
