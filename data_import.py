import xlrd
import xlsxwriter
import os

src_files = [f for f in os.listdir('data') if f[-1] in 'Xx']


for src in src_files:
    data = []
    str_input = open(os.path.join('source', src), 'rb').read()
    wb = xlrd.open_workbook(file_contents=str_input)
    sheet = wb.sheets()[0]
    for row in range(sheet.nrows):
        values = []
        for col in range(sheet.ncols):
            values.append(sheet.cell(row, col).value)
        data.append(values)




###DATA PARSING
## split
