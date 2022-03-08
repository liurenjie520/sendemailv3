    #-*- codeing = utf-8 -*-
    #@Time : 2020/6/2 20:26
    #@Author : dele
    #@File : weather.py
    #@Software: PyCharm
    
    
    import requests
    from bs4 import  BeautifulSoup
    import io
    import sys
    import pandas
    from matplotlib import pyplot as plt
    
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
    def get_data(weather_url):
        rseponse = requests.get(weather_url)
    
        html = rseponse.content.decode('gbk')
        soup = BeautifulSoup(html,'html.parser')
    
        tr_lsit = soup.find_all('tr')
    
        print(tr_lsit)
        dates,conditions,temp = [],[],[]
        for data in tr_lsit[1:]:
            sub_data = data.text.split()
            dates.append(sub_data[0])
            conditions.append(''.join(sub_data[1:3]))
            temp.append(''.join(sub_data[3:6]))
    
        # 数据保存
        _data = pandas.DataFrame()
        _data['日期'] = dates
        _data['天气情况'] = conditions
        _data['气温'] = temp
    
        return _data
        # print(_data)
        # _data.to_csv('anqing.csv',index=False,encoding='gbk')
    
    # data_month_3 =get_data('http://www.tianqihoubao.com/lishi/anqing/month/202003.html')
    # data_month_4 =get_data('http://www.tianqihoubao.com/lishi/anqing/month/202004.html')
    # data_month_5 =get_data('http://www.tianqihoubao.com/lishi/anqing/month/202005.html')
    #
    # data = pandas.concat([data_month_3,data_month_4,data_month_5]).reset_index(drop=True)
    # data.to_csv('anqing.csv',index=False,encoding='gbk')
    
    
    
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    datalsit = pandas.read_csv('G:/Python_Web/weather/anqing.csv',encoding='gbk')
    
    # 数据处理
    datalsit['最高气温'] = datalsit['气温'].str.split('/',expand=True)[0]
    datalsit['最低气温'] = datalsit['气温'].str.split('/',expand=True)[1]
    
    datalsit['最高气温'] = datalsit['最高气温'].map(lambda x:int(x.replace('℃','')))
    datalsit['最低气温'] = datalsit['最低气温'].map(lambda x:int(x.replace('℃','')))
    
    dates = datalsit['日期']
    highs = datalsit['最高气温']
    lows =  datalsit['最低气温']
    
    # 画图
    
    fig = plt.figure(dpi=128,figsize=(10,6))
    
    plt.plot(dates,highs,c='red',alpha=0.5)
    plt.plot(dates,lows,c='blue',alpha=0.5)
    
    plt.fill_between(dates,highs,lows,facecolor='blue',alpha=0.2)
    # 图表格式
    # 设置图标的图形格式
    plt.title('2020安庆市3-5月天气情况',fontsize=24)
    plt.xlabel('',fontsize=6)
    fig.autofmt_xdate()
    plt.ylabel('气温',fontsize=12)
    plt.tick_params(axis='both',which='major',labelsize=10)
    # 修改刻度
    plt.xticks(dates[::20])
    # 显示
    plt.show()
