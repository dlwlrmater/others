import pandas as pd
import time

# 查看所有车站经过的车次，从侧面体现车站在地区中重要程度

time_now = time.time()
# file = pd.read_csv(r'C:\Users\steve\Desktop\携程铁路{}.csv'.format(time.strftime('%Y%m%d', time.localtime(time_now))))
file = pd.read_csv(r'C:\Users\steve\Desktop\携程铁路20200109result.csv')

a = file['banci']
b = file['way']
file1 = pd.DataFrame(zip(a,b),columns=list('ab'))
# print(file1)

# 路径里头所有的值
lst_all = []
lst_all2 = []
lst_lens = []

# 路径里头按每个班次分的list
for x in range(len(file1['a'])):

    for y in range(len(file1['b'][x].split(' '))):
        c = file1['b'][x].split(' ')[y]
        d = file1['a'][x]
        lst_all.append(d)
        lst_all2.append(c)
        lst_lens.append(len(c))
        # print(file1['b'][x][y],file1['a'][x])
df = pd.DataFrame(zip(lst_all,lst_all2,lst_lens),columns=['banci','station','lens'])
df = df.sort_values(by='lens')
print(df)
df.to_csv(r'C:\Users\steve\Desktop\携程铁路{}-车站所在班次.csv'.format(time.strftime('%Y%m%d', time.localtime(time_now))))