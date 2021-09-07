import pandas as pd
import numpy as np
import time
import datetime
import csv
import json
import requests
import threading


# 查看特定时间内两个站点之间所有铁路线路
# 项目当时是选取在春运时，铁路线路调整情况。从侧面体现春运迁徙流动情况


def assa(time):
    hs = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Cookie': '_RF1=111.199.168.89; _RSG=Wj4KMqOqSGBD8bD.sTdqhB; _RDG=28db5c6458e29521452a887d6aa7d19c2a; _RGUID=b41cd18d-1650-4b60-baf4-9dddbe36520d; MKT_CKID=1627821750904.isdo2.l273; _ga=GA1.2.1712558599.1628668287; MKT_CKID_LMT=1631028345476; _gid=GA1.2.992698158.1631028346; MKT_Pagesource=PC; appFloatCnt=1; ibulanguage=CN; ibulocale=zh_cn; cookiePricesDisplayed=CNY; _gat=1; Session=smartlinkcode=U130026&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; Union=AllianceID=4897&SID=130026&OUID=&createtime=1631029004&Expires=1631633803936; _jzqco=%7C%7C%7C%7C%7C1.1280201987.1631029003951.1631029003951.1631029003951.1631029003951.1631029003951.0.0.0.1.1; __zpspc=9.4.1631029003.1631029003.1%232%7Cwww.baidu.com%7C%7C%7C%7C%23; Customer=HAL=ctrip_cn; _ctm_t=ctrip; ibu_wws_c=1633621004696%7Czh-cn; _bfi=p1%3D10320670296%26p2%3D100101991%26v1%3D5%26v2%3D4; login_uid=C6F2C1BB6F780155ABC827F200F4B439; login_type=0; cticket=A3887152A855972F0F62853AD7F7A85D4E3116BB584E7B49BA123E11A662830A; AHeadUserInfo=VipGrade=10&VipGradeName=%BB%C6%BD%F0%B9%F3%B1%F6&UserName=&NoReadMessageCount=0; ticket_ctrip=bJ9RlCHVwlu1ZjyusRi+ypZ7X2r4+yojl9IHo9acfbmDoqhYdezS3hJ/1L3KKN5YK9Ruw1FJjftqK2jQifyDuYw5dxvl+UPCI6gZZtGZtMWGerRxT96GJCTlIXZ/jIx9Py9LxnsZqqwPVsymKi/CRY5pPlj1dOEUXRRMmbfwfZRWdYbRTIa8OaRCpIKSyEATbcg1NpOutQHVslBgXLZaG3BAaqC1hEUcDwSsA+FOvBSbtqn9ynm8GT6ZsH0YDBNMQhDqrZyEvY1dNuKitPFoOEVcngrXNyi6PS7r83hTRQU=; DUID=u=C6F2C1BB6F780155ABC827F200F4B439&v=0; IsNonUser=F; UUID=43F3E6B9AEAE403CB5B531616046BA3C; IsPersonalizedLogin=T; _bfa=1.1627821747759.3x75rw.1.1628668283626.1631028342426.3.6; _bfs=1.4',
        'Host': 'trains.ctrip.com',
        'Origin': 'http://trains.ctrip.com',
        # 'Referer':'http://trains.ctrip.com/TrainBooking/Search.aspx?from=beijing&to=shanghai&day=2019/03/06&number=&fromCn=%25E5%258C%2597%25E4%25BA%25AC&toCn=%25E4%25B8%258A%25E6%25B5%25B7',
        # 'Referer':'http://trains.ctrip.com/TrainBooking/Search.aspx?from=wuxi&to=shanghai&day=7&fromCn=%CE%DE%CE%FD&toCn=%C9%CF%BA%A3',
        'If-Modified-Since': 'Thu, 01 Jan 1970 00:00:00 GMT',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '317',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    a = pd.read_csv(r'C:\Users\steve\Desktop\携程春运\携程铁路20200109result.csv')
    # print(a)
    od = a['od']
    # print(od)
    unique_od = pd.unique(od)
    unique_od = pd.Series(unique_od)
    unique_od = unique_od.dropna()
    print(len(unique_od))
    O = []
    D = []
    for i in unique_od:
        print(i)
        o = i.split(' ')[0]
        d = i.split(' ')[1]
        O.append(o)
        D.append(d)
    TrainNames = []
    for x,y in zip(O,D):
        url1 = 'http://trains.ctrip.com/TrainBooking/Ajax/SearchListHandler.ashx?Action=getSearchList'
        p2 = {
            'value': '{"IsBus":false,"Filter":"0","Catalog":"","IsGaoTie":false,"IsDongChe":false,"CatalogName":"","HubCity":"","DepartureCityName":"' + str(x) + '","ArrivalCityName":"' + str(y) + '","DepartureDate":"' + time + '","ArrivalDate":"","TrainNumber":""}'
        }

        print(x,y)
        # print(p2)
        result = requests.post(url=url1, data=p2, headers=hs)
        if result.text == '':
            pass
        else:
            # print(result.url)
            result.encoding = result.apparent_encoding
            # a1 = etree.HTML(a)
            # b=a.json()
            js = json.loads(result.text)
            # print(js)
            TrainItemsList_ = js['TrainItemsList']
            for index in range(len(TrainItemsList_)):
                TrainName_ = TrainItemsList_[index]['TrainName']
                TrainNames.append(TrainName_)
                # print(TrainName_)
    df = pd.Series(TrainNames)
    # end = datetime.datetime.time()
    # print(df)
    # df.to_csv(r'C:\Users\steve\Desktop\春运.csv',mode = 'a')

if __name__ == '__main__':
    # times = ['2020-01-10', '2020-01-11', '2020-01-12']
    # for time in times:
    #     assa(time)
    # now = datetime.datetime.time()
    # threads = []
    t1 = threading.Thread(target=assa, args=('2020-01-10',))
    # t2 = threading.Thread(target=assa, args=('2020-01-11',))
    # t3 = threading.Thread(target=assa, args=('2020-01-12',))
    # t4 = threading.Thread(target=assa, args=('2020-01-13',))
    # t5 = threading.Thread(target=assa, args=('2020-01-14',))
    # t6 = threading.Thread(target=assa, args=('2020-01-15',))
    # t7 = threading.Thread(target=assa, args=('2020-01-16',))
    t1.start()
    # t2.start()
    # t3.start()
    # t4.start()
    # t5.start()
    # t6.start()
    # t7.start()
    t1.join()
    # t2.join()
    # t3.join()
    # t4.join()
    # t5.join()
    # t6.join()
    # t7.join()
    # end = datetime.datetime.time()
    # print('time use:%s' % (end - now))