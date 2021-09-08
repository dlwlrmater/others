import pandas as pd
import re

def MtoList(address,name1,name2):
    try:
        # 数据显示全
        pd.set_option('display.width',None)
        # 读取数据
        a = pd.read_csv(address,index_col=0,header=0)
        # 获得OD index
        b = a.stack().index.values
        # 获得OD之前的值
        c = a.stack().values
        # 建立新的MultiIndex for new DataFrame
        z = []
        for i in b:
            z1 = i[0]
            z2 = re.sub('\d+','',list(i)[1].replace('.',''))
            z.append((z1,z2))
        m_index = pd.Index(z,names=[name1,name2])
        # print(m_index)
        # 建立新Series
        d = pd.Series(c,index=m_index)
        e = d.groupby(by=m_index).sum().sort_values(ascending=False)
        return e
    except:
        print('error')


