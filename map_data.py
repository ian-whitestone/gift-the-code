import database_operations as dbo
import pandas as pd
import numpy as np


def perishable_ratio(df):
    if df['total']==0:
        return 0
    else:
        return (df['non_food']+df['non_perish'])/df['total']

def nutrient_ratio(df):
    if df['total']==0:
        return 0
    else:
        return (df['protein']+df['produce']+df['dairy'])/df['total']

def get_map_data():
    ##query db

    ##filter out rows missing postal codes
    df=df[df['postcode'].notnull()]

    #create addl fields
    df['year']=df['date'].map(lambda x: int(str(x)[0:4]))
    sum_col_list=['bread', 'baked', 'dairy','produce', 'protein', 'prepared', 'bev_juice', 'bev_other', 'snack','non_perish', 'non_food']
    df['total']=df[sum_col_list].sum(axis=1)
    df['perishable_ratio']=df.apply(perishable_ratio,axis=1)
    df['nutrient_ratio']=df.apply(nutrient_ratio,axis=1)

    #get summary df
    grouped_df=df.groupby(['stop_type','year','postcode','long','lat','neighbourhood','locality']).agg({'total':np.sum,'nutrient_ratio':np.mean,'perishable_ratio':np.mean}).reset_index()

    return
