import xlrd
import database_operations as dbo
import pprint
import os


def read_data(src):
    data = []
    str_input = open(os.path.join('data', src), 'rb').read()
    wb = xlrd.open_workbook(file_contents=str_input)
    sheet = wb.sheets()[0]
    fields = []
    for col in range(sheet.ncols):
        fields.append(sheet.cell(0, col).value)

    data = []
    for row in range(1, sheet.nrows):
        row_data = [sheet.cell(row, col).value for col in range(sheet.ncols)]
        data.append(dict(zip(tuple(fields), tuple(row_data))))

    fields_to_keep = {'Response ID': 'response_id',
                      '9: 1.:In your own words, list the top 3 reasons why your organization requires Second Harvest food support for your program(s).:What effect does Second Harvest have on your program(s) and program participants?': 'reas_1',
                      '9: 2.:In your own words, list the top 3 reasons why your organization requires Second Harvest food support for your program(s).:What effect does Second Harvest have on your program(s) and program participants?': 'reas_2',
                      '9: 3.:In your own words, list the top 3 reasons why your organization requires Second Harvest food support for your program(s).:What effect does Second Harvest have on your program(s) and program participants?': 'reas_3',
                      '10: In your own words, list how your program(s) would be affected without the food from Second Harvest?:What would your program(s) be like without the food from Second Harvest?': 'effect',
                      '12: How many individual clients are served with Second Harvest food annually?Please count each person only once, regardless of the number of times they access your agency. Ex. Joe Smith visits your food bank twice each month and he attends the drop-in breakfast once a week, count Joe only once as he is one person accessing multiple programs.': 'clients',
                      '19: % that are Children:What are the age groups of the people who receive Second Harvest food through your agency\'s program(s)?         Example: Our programs serve women and their children. Adult Women = 40%; Youth = 10%; Children = 50%  ': 'children_perc',
                      '19: % that are Youth:What are the age groups of the people who receive Second Harvest food through your agency\'s program(s)?         Example: Our programs serve women and their children. Adult Women = 40%; Youth = 10%; Children = 50%  ': 'youth_perc',
                      '19: % that are Adult Men:What are the age groups of the people who receive Second Harvest food through your agency\'s program(s)?         Example: Our programs serve women and their children. Adult Women = 40%; Youth = 10%; Children = 50%  ': 'men_perc',
                      '19: % that are Adult Women:What are the age groups of the people who receive Second Harvest food through your agency\'s program(s)?         Example: Our programs serve women and their children. Adult Women = 40%; Youth = 10%; Children = 50%  ': 'women_perc',
                      '19: % that are Seniors:What are the age groups of the people who receive Second Harvest food through your agency\'s program(s)?         Example: Our programs serve women and their children. Adult Women = 40%; Youth = 10%; Children = 50%  ': 'senior_perc',
                      '22: Overall, what percentage (%) of your agency\'s total food is provided by Second Harvest?': 'perc_provided',
                      '34: Dispatch/Office - Customer Service:Please rate Second Harvest on each of the following criteria, from "Excellent" to "Very Poor".': 'nps_office',
                      '34: Driver - Customer Service:Please rate Second Harvest on each of the following criteria, from "Excellent" to "Very Poor".': 'nps_driver',
                      '34: Agency Relations - Communications and Customer Service:Please rate Second Harvest on each of the following criteria, from "Excellent" to "Very Poor".': 'nps_agency',
                      '34: Agency Workshops:Please rate Second Harvest on each of the following criteria, from "Excellent" to "Very Poor".': 'nps_workshop',
                      '35: Second Harvest is crucial to the success of our program(s).:To what extent would you say you agree or disagree with each of the following statements about Second Harvest?': 'crucial_to_success',
                      '35: Second Harvest provides healthy and nutritious food for our program(s).:To what extent would you say you agree or disagree with each of the following statements about Second Harvest?': 'healthy_and_nutritious',
                      '35: Second Harvest food donations provide opportunities for us to have diverse foods and flavours at our programs.:To what extent would you say you agree or disagree with each of the following statements about Second Harvest?': 'diverse',
                      '35: Second Harvest food donations allow us to offer expanded programs and services to our program participants.:To what extent would you say you agree or disagree with each of the following statements about Second Harvest?': 'expanded_programs',
                      '35: Second Harvest has connected us to resources and/or opportunities that have benefited our agency.:To what extent would you say you agree or disagree with each of the following statements about Second Harvest?': 'more_opportunities'}

    keep_data = [{fields_to_keep[field]: row[field]
                  for field in fields_to_keep.keys()} for row in data]

    nps_map = {'Strongly Agree': 1,
               'Somewhat Agree': 0,
               'Somewhat Disagree': -1,
               'Strongly Disagree': -1,
               'Excellent': 1,
               'Very Good': 1,
               'Good': 0,
               'Average': -1,
               'Poor': -1,
               'Very Poor': -1}
    response_id_map = {151: 1009, 253: 1010, 113: 1013, 235: 1039, 246: 1146, 379: 1155, 156: 1158, 302: 1162, 332: 1165, 75: 1167, 372: 1168, 355: 1171, 241: 1179, 248: 1183, 388: 1186, 250: 1188, 380: 1189, 115: 1190, 180: 1191, 279: 1195, 410: 1196, 426: 1202, 94: 1204, 267: 1205, 219: 1428, 188: 1785, 143: 2530, 304: 2940, 342: 2987, 345: 3014, 173: 3048, 376: 4568, 231: 4866, 344: 5203, 327: 5205, 297: 5207, 69: 5208, 158: 5209, 373: 6566, 186: 7237, 226: 7239, 352: 7242, 403: 7244, 268: 7245, 323: 7246, 64: 7972, 400: 8157, 131: 8161, 150: 8165, 76: 8167, 420: 8169, 141: 11447, 288: 11451, 418: 12098, 70: 12099, 416: 12102, 299: 12174, 371: 12177, 125: 13112, 209: 13467, 411: 13598, 399: 13599, 205: 13600, 197: 13603, 409: 14526, 202: 14878, 71: 14899, 294: 17834, 119: 18728, 181: 19174, 85: 19201, 222: 19280, 245: 19469, 402: 19538, 292: 20878, 387: 20919, 273: 21525, 350: 22449, 147: 22549, 341: 23513, 74: 23563, 377: 23590, 386: 24014, 63: 24112, 363: 24754, 343: 24757, 264: 24854, 306: 25471, 126: 25472, 398: 25473, 368: 25476, 397: 26049, 391: 26165, 138: 26339, 176: 27596, 359: 27744, 169: 28314, 229: 28319, 224: 28859,
                       171: 29160, 275: 29323, 174: 29377, 407: 30259, 329: 30260, 154: 31102, 213: 31245, 351: 31246, 72: 31401, 88: 31595, 242: 31596, 221: 31597, 348: 32272, 360: 32371, 346: 32375, 393: 32392, 381: 32515, 333: 33003, 112: 33012, 191: 33014, 230: 33015, 204: 33473, 357: 33524, 325: 33663, 389: 34101, 349: 34198, 308: 34942, 236: 35100, 277: 35532, 318: 35727, 337: 35770, 408: 36601, 282: 39015, 401: 39039, 87: 47089, 303: 47413, 178: 47425, 262: 48122, 314: 48139, 183: 48141, 247: 48143, 265: 48146, 378: 51025, 149: 56662, 97: 56693, 286: 59339, 301: 60454, 417: 60483, 405: 64336, 251: 67733, 227: 69864, 238: 70411, 201: 73676, 142: 76698, 157: 76700, 182: 76702, 249: 76739, 260: 76741, 383: 76742, 300: 76746, 382: 76748, 73: 76750, 310: 76752, 289: 78057, 240: 84644, 419: 85062, 107: 86045, 109: 90662, 189: 91398, 296: 99464, 413: 99740, 414: 105307, 254: 105540, 406: 108503, 317: 110648, 190: 110659, 331: 110667, 184: 111113, 167: 111114, 293: 111723, 425: 111725, 422: 111727, 404: 111793, 328: 111797, 415: 111799, 255: 112472, 239: 112475, 315: 112477, 281: 113632, 99: 114347, 276: 116586, 244: 116589, 423: 117187, 140: 117195}

    for d in keep_data:
        remap_fields(d, nps_map)
        d['donor_id'] = response_id_map[int(d['response_id'])]
    return keep_data


def remap_fields(d, nps_map):

    for k in d.keys():
        if k.endswith('perc') or k == 'perc_provided':
            try:
                d[k] = float(d[k].replace('%', '').strip()) / 100
            except:
                d[k] = 0
        if k.startswith('nps') or k in ['crucial_to_success', 'diverse', 'healthy_and_nutritious', 'more_opportunities', 'expanded_programs']:
            d[k] = nps_map[d[k]]
    return d


if __name__ == '__main__':
    d = read_data('survey.xlsx')
    conn = dbo.db_connect()
    fields = ['response_id', 'donor_id', 'reas_1', 'reas_2', 'reas_3', 'effect', 'clients', 'children_perc', 'youth_perc', 'men_perc', 'women_perc', 'senior_perc', 'perc_provided',
              'nps_office', 'nps_driver', 'nps_agency', 'nps_workshop', 'crucial_to_success', 'healthy_and_nutritious', 'diverse', 'expanded_programs', 'more_opportunities']
    dbo.insert_dict_query(
        conn, "INSERT INTO survey VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", d, fields, multiple=True)
