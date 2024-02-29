import numpy as np
import pandas as pd
import re


def check_empty_bins(dtm,bins):
    # check empty bins
    bin_list = np.unique(dtm[bins].astype(str)).tolist()
    if 'nan' in bin_list:
        bin_list.remove('nan')
    binleft = set([re.match(r'\((.+),(.+)\]', i).group(1) for i in bin_list]).difference(set(['-inf', 'inf']))
    binright = set([re.match(r'\((.+),(.+)\]', i).group(2) for i in bin_list]).difference(set(['-inf', 'inf']))
    if binleft != binright:
        bstbrks = sorted(list(map(float, ['-inf'] + list(binright) + ['inf'])))
        bstbrks.pop(-2)
        labels = ['[{},{})'.format(bstbrks[i], bstbrks[i + 1]) for i in range(len(bstbrks) - 1)]
        # print("The break points are modified into '[{}]'. There are empty bins based on the provided break points.".format(','.join(binright)))
        # binning
        # dtm['bin'] = dtm['bin'].astype(str)
    # return
    return bstbrks
#字符型或者唯一值较少的变量
def psi1(data,psi_data,var):
    a = data[var].value_counts().reset_index(drop=False)#.astype(str)
    a.rename(columns={var:'name','count':'开发'+var},inplace=True)
    b=psi_data[var].value_counts().reset_index(drop=False)#.astype(str)
    b.rename(columns={var:'name','count':'验证'+var},inplace=True)
    m=pd.merge(a,b,on='name',how='inner')
    m[var+'开发频率']=m['开发'+var]/sum(m['开发'+var])
    m[var+'验证频率']=m['验证'+var]/sum(m['验证'+var])
    m['psi']=(m[var+'开发频率']-m[var+'验证频率'])*np.log(m[var+'开发频率']/m[var+'验证频率'])
    psi_sum=sum(m['psi'])
    return psi_sum
def psi2(data,psi_data,var,brk):
    a = pd.cut(data[var], brk, right=False).value_counts().reset_index(drop=False)#.astype(str)
    a.rename(columns={var:'name','count':'开发'+var},inplace=True)
    b=pd.cut(psi_data[var], brk,right=False).value_counts().reset_index(drop=False)#.astype(str)
    b.rename(columns={var:'name','count':'验证'+var},inplace=True)
    m=pd.merge(a,b,on='name',how='inner')
    m[var+'开发频率']=m['开发'+var]/sum(m['开发'+var])
    m[var+'验证频率']=m['验证'+var]/sum(m['验证'+var])
    m['psi']=(m[var+'开发频率']-m[var+'验证频率'])*np.log(m[var+'开发频率']/m[var+'验证频率'])
    psi_sum=sum(m['psi'])
    return psi_sum
def psi_hui(df,psi_data,target,n=5):
    chat=list(df.columns[df.dtypes == 'object'])
    name=df.columns.drop(target)
    psis=[]
    for i in name:
        X=df[i]
        Y=df[target]
        nuniq=X.nunique()
        if nuniq<=n:
            chat.append(i)
        if i in chat:
            psi=psi1(df,psi_data,i)
            psis.append(psi)
        else:
            d1=pd.DataFrame({"X":X,"Y":Y,"bin":pd.qcut(X,n,duplicates='drop')})
#            d1['bin']=d1['bin'].astype(str)
            brk=check_empty_bins(d1, 'bin')
            psi=psi2(df,psi_data,i,brk)
            psis.append(psi)
        print (i)
    d=pd.DataFrame({"name":name,"psi":psis})
    return d

data = pd.read_csv('test_data.csv')
print('Shape:',data.shape)
d=psi_hui(data.iloc[0:250],data.iloc[250:500],'target')
print(d)