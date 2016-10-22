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
    response_id_map = {1009: 151, 1010: 253, 1013: 113, 1039: 235, 1146: 246, 1155: 379, 1158: 156, 1162: 302, 1165: 332, 1167: 75, 1168: 372, 1171: 355, 1179: 241, 1183: 248, 1186: 388, 1188: 250, 1189: 380, 1190: 115, 1191: 180, 1195: 279, 1196: 410, 1202: 426, 1204: 94, 1205: 267, 1428: 219, 1785: 188, 2530: 143, 2940: 304, 2987: 342, 3014: 345, 3048: 173, 4568: 376, 4866: 231, 5203: 344, 5205: 327, 5207: 297, 5208: 69, 5209: 158, 6566: 373, 7237: 186, 7239: 226, 7242: 352, 7244: 403, 7245: 268, 7246: 323, 7972: 64, 8157: 400, 8161: 131, 8165: 150, 8167: 76, 8169: 420, 11447: 141, 11451: 288, 12098: 418, 12099: 70, 12102: 416, 12174: 299, 12177: 371, 13112: 125, 13467: 209, 13598: 411, 13599: 399, 13600: 205, 13603: 197, 14526: 409, 14878: 202, 14899: 71, 17834: 294, 18728: 119, 19174: 181, 19201: 85, 19280: 222, 19469: 245, 19538: 402, 20878: 292, 20919: 387, 21525: 273, 22449: 350, 22549: 147, 23513: 341, 23563: 74, 23590: 377, 24014: 386, 24112: 63, 24754: 363, 24757: 343, 24854: 264, 25471: 306, 25472: 126, 25473: 398, 25476: 368, 26049: 397, 26165: 391, 26339: 138, 27596: 176, 27744: 359, 28314: 169, 28319: 229, 28859: 224,
                       29160: 171, 29323: 275, 29377: 174, 30259: 407, 30260: 329, 31102: 154, 31245: 213, 31246: 351, 31401: 72, 31595: 88, 31596: 242, 31597: 221, 32272: 348, 32371: 360, 32375: 346, 32392: 393, 32515: 381, 33003: 333, 33012: 112, 33014: 191, 33015: 230, 33473: 204, 33524: 357, 33663: 325, 34101: 389, 34198: 349, 34942: 308, 35100: 236, 35532: 277, 35727: 318, 35770: 337, 36601: 408, 39015: 282, 39039: 401, 47089: 87, 47413: 303, 47425: 178, 48122: 262, 48139: 314, 48141: 183, 48143: 247, 48146: 265, 51025: 378, 56662: 149, 56693: 97, 59339: 286, 60454: 301, 60483: 417, 64336: 405, 67733: 251, 69864: 227, 70411: 238, 73676: 201, 76698: 142, 76700: 157, 76702: 182, 76739: 249, 76741: 260, 76742: 383, 76746: 300, 76748: 382, 76750: 73, 76752: 310, 78057: 289, 84644: 240, 85062: 419, 86045: 107, 90662: 109, 91398: 189, 99464: 296, 99740: 413, 105307: 414, 105540: 254, 108503: 406, 110648: 317, 110659: 190, 110667: 331, 111113: 184, 111114: 167, 111723: 293, 111725: 425, 111727: 422, 111793: 404, 111797: 328, 111799: 415, 112472: 255, 112475: 239, 112477: 315, 113632: 281, 114347: 99, 116586: 276, 116589: 244, 117187: 423, 117195: 140}


    for d in keep_data:
        remap_fields(d, nps_map)
        d['donor_id'] = response_id_map[d['response_id']]
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
        conn, "INSERT INTO survey VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", d, fields, multiple=True)
