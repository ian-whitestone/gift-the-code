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
    for d in keep_data:
        remap_fields(d, nps_map)

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
    fields = ['response_id', 'reas_1', 'reas_2', 'reas_3', 'effect', 'clients', 'children_perc', 'youth_perc', 'men_perc', 'women_perc', 'senior_perc', 'perc_provided',
              'nps_office', 'nps_driver', 'nps_agency', 'nps_workshop', 'crucial_to_success', 'healthy_and_nutritious', 'diverse', 'expanded_programs', 'more_opportunities']
    dbo.insert_dict_query(
        conn, "INSERT INTO survey (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", d, fields, multiple=True)
