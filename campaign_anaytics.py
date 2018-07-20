#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 16:48:22 2018

@author: razzak_lebbai
"""
##new column only control and test group 
def control_challange(x):
    if x==1:
        val ='CONTROL'
    else:
        val='CHALLENGER'
    return val
import pandas as pd
import numpy as np

df = pd.read_csv('/Users/razzak_lebbai/Desktop/msc/campaign/jgray_yr1_ar_list_pull_hist_status_as_01_18_2018.csv')
##add control or challenger filed as "GROUP
df['GROUP']=df.apply(lambda x: control_challange(x['RAND_GROUP']), axis=1)  

##remove rows with 'STILL HAVE TIME'
df_filter = df[df.RENEWAL_STATUS!='STILL HAVE TIME']





 
 #####group by random group 
count_by_status_rand_group = df_filter.groupby(['RAND_GROUP','RENEWAL_STATUS']).size().rename('total_count').reset_index()
count_by_status_rand_group = count_by_status_rand_group.assign(Percentage=(100*count_by_status_rand_group.total_count/count_by_status_rand_group.groupby('RAND_GROUP')\
                                                                 ['total_count'].transform('sum')).round(2).astype(str)+'%')



##Group by group 
count_by_status_group = df_filter.groupby(['GROUP','RENEWAL_STATUS']).size().rename('total_count').reset_index()

count_by_status_group = count_by_status_group.assign(Percentage=(100*count_by_status_group.total_count/count_by_status_group.groupby('GROUP')\
                                                                 ['total_count'].transform('sum')).round(2).astype(str)+'%')


count_by_status_group = count_by_status_group.assign(Ratio= (count_by_status_group.total_count/count_by_status_group.groupby('GROUP')\
                                                                 ['total_count'].transform('sum')).round(4))


count_by_status_group_1  = count_by_status_group.loc[:, ['GROUP', 'RENEWAL_STATUS', 'Percentage']].set_index('GROUP') 

count_by_status_group_pivot  = count_by_status_group_1.pivot(columns='RENEWAL_STATUS').reset_index()



##for total data
total_data = count_by_status_group.groupby('RENEWAL_STATUS')['total_count'].sum().reset_index()

total_data['Percentage'] = (100*total_data.total_count/total_data.total_count.sum()).round(2).astype(str)+'%'

del total_data['total_count']

##control ratio/true ratio
P = count_by_status_group[(count_by_status_group.GROUP=='CONTROL') & (count_by_status_group.RENEWAL_STATUS=='AR')]['Ratio']
##P=0.8142
##sample ratio
p = count_by_status_group[(count_by_status_group.GROUP=='CHALLENGER') & (count_by_status_group.RENEWAL_STATUS=='AR')]['Ratio']
##p=0.8158

n= df_filter.shape[0]
sigma = np.sqrt( P * ( 1 - P ) / n )

##test statistics
z = (p - P) / sigma

import scipy.stats as st

##let's assume significant is Assume a significance level of 0.025 (alpha=0.025)

P_value = 1- st.norm.cdf(z)
##since Pvalue is less than alpha 
## we reject the null hypothesis

def p_vale_cal(P, p, n):
    sigma = np.sqrt( P * ( 1 - P ) / n )

    ##test statistics
    z = (p - P) / sigma
    P_value = 1- st.norm.cdf(z)
    return P_value

n_ret=[87428,84892,84696]
P_ret=[0.2631, 0.2616,0.2642]
P_refund=[0.0166,0.0163,0.0175]
P_bill_update=[0.1692,0.1704,0.1720]

P=15/14184
