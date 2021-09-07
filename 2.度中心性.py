import pandas as pd
import numpy as np
import time
import datetime
from tqdm import trange

# 从列城班次数据生成路线相邻两个车站联系情况 -- 度中心性



pd.set_option('display.max_columns',None)
start_time = datetime.datetime.now()

time_now = time.time()
# 前一个文件生成csv
file = pd.read_csv(r'/Users/ternencekk/OneDrive/!ctrip/携程铁路20200614result2.csv')
file = file.drop_duplicates()
file = file.drop_duplicates(subset='od')
# 路径里头所有的站名
lst_all = []

# 路径里头按每个班次分的list
lst_all2= []
# print(file[:7])
for x in file['way']:
    lst_all.extend(x.split(' '))
    # print(lst_all)
    lst_all2.append(x.split(' '))
    # print(lst_all2)

# 做matrix行列的值
lst_unique = pd.unique(lst_all)
# print(lst_unique)

# 所需要的度中心性格式的list 坐标格式
lst_all3 = []

for a in trange(len(lst_all2)):
    for b,c in zip(range(len(lst_all2[a])),range(1,len(lst_all2[a]))):
        zuobiao = [lst_all2[a][b],lst_all2[a][c]]
        lst_all3.append(zuobiao)
result = pd.Series(lst_all3)
# print(lst_all3)

zero_matrix = np.zeros((len(lst_unique),len(lst_unique)))
# print(zero_matrix)
result_matrix = pd.DataFrame(zero_matrix,columns=lst_unique,index=lst_unique)
# print(result_matrix)
for d,e in lst_all3:
    # print(d,e)
    # print(e)
    f = list(lst_unique).index(d)
    g = list(lst_unique).index(e)
    result_matrix.iloc[f,g] += 1

O = []
D = []
nums = []
for a1 in trange(len(lst_unique)):
    for a2 in range(len(lst_unique)):
        if a1 == a2:
            pass
        else:
            h1 = lst_unique[a1]
            h2 = lst_unique[a2]

            h3 = list(lst_unique).index(h1)
            h4 = list(lst_unique).index(h2)
            num = result_matrix.iloc[h3,h4]
            if num == 0:
                pass
            else:
                O.append(h1)
                D.append(h2)
                nums.append(num)
# print(O)
# print(len(O))
# print(D)
# print(len(D))
# print(nums)
# print(len(nums))
# print(zip(O,D,nums))
result_line = pd.DataFrame(list(zip(O,D,nums)),columns=['O','D','nums'])
result_line = result_line.sort_values(by='nums',ascending=False)

end_time = datetime.datetime.now()
writer = pd.ExcelWriter(r'/Users/ternencekk/OneDrive/!ctrip/携程铁路20200614result.xlsx')
result_matrix.to_excel(writer,sheet_name='matrix')
result_line.to_excel(writer,sheet_name='lines')
writer.save()
print('time use:%s' %(end_time-start_time))