import threading
import time
import requests
from lxml import etree
import pandas as pd
import datetime
from tqdm import trange
import queue


# 基于携程订票网页数据爬取所有铁路线路班次和途径站点数据

typpe= ['G','C','D','Z','T','K','']


def GOGOGO(input):
    time_now = time.time()
    name = []
    OD = []
    result = []
    for j in trange(0,10000):
        checi = input+str(j)
        if checi == '5611' or checi == '5612':
            pass
        else:
            # print(checi)
            url = 'https://trains.ctrip.com/trainbooking/TrainSchedule/'+ checi +'/'
            # print(url)
            r = requests.get(url,timeout = 5)
            et =etree.HTML(r.content.decode('gbk'))
            line = et.xpath('//div[@class="s_bd"]//a[@id]/text()')
            # print(line)
            # if line == []:
            #     pass
            # else:
            lline = []
            for a in line:
                b = a.replace(' ','')
                lline.append(b)
            line1 = lline[:2]
            line2 = lline[2:]
            name.append(checi)
            OD.append(' '.join(line1))
            result.append(' '.join(line2))
    df = pd.DataFrame({'banci': name, 'od': OD, 'way': result})
    df.to_csv(r'/Users/ternencekk/OneDrive/!ctrip/携程铁路{}result.csv'.format(time.strftime('%Y%m%d', time.localtime(time_now))),mode='a')
    # df.to_csv(r'C:\Users\steve\Desktop\123.csv',mode='a')

if __name__ == '__main__':
    now = datetime.datetime.now()
    now_time = time.time()
    t1 = threading.Thread(target=GOGOGO,args=('G',))
    t2 = threading.Thread(target=GOGOGO,args=('C',))
    t3 = threading.Thread(target=GOGOGO, args=('D',))
    t4 = threading.Thread(target=GOGOGO, args=('Z',))
    t5 = threading.Thread(target=GOGOGO, args=('T',))
    t6 = threading.Thread(target=GOGOGO, args=('K',))
    t7 = threading.Thread(target=GOGOGO, args=('',))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()

    a = pd.read_csv(r'/Users/ternencekk/OneDrive/!ctrip/携程铁路{}result_Origin.csv'.format(time.strftime('%Y%m%d', time.localtime(now_time))))
    # 把index替换成banci
    b = a.set_index(keys='banci')
    # 除去Unnamed:0这一列（原index）
    d = b.reindex(columns=['od', 'way'])
    # 根据od列降序排列
    e = d.sort_values(by='od', ascending=False)
    # print(e)
    # 除去没有车次的空置
    f = e.dropna()
    # print(f)
    # 把剩余表头删除
    h = f.drop(['banci'])
    print(h)
    h.to_csv(r'/Users/ternencekk/OneDrive/!ctrip/携程铁路{}result_withoutNaN.csv'.format(time.strftime('%Y%m%d', time.localtime(now_time))), encoding='utf-8')

    end = datetime.datetime.now()
    print('time use:%s' % (end - now))


