import requests
from bs4 import BeautifulSoup


#定义天气城市代码
cityCodeDict={
        "北京":101010100,"上海":101020100,"天津":101030100,"重庆":101040100,"哈尔滨":101050101,
        "长春":101060101,"沈阳":101070101,"呼和浩特":101080101,"石家庄":101090101,"太原":101100101,
        "西安":101110101,"济南":101120101,"乌鲁木齐":101130101,"拉萨":101140101,"西宁":101150101,
        "兰州":101160101,"银川":101170101,"郑州":101180101,"南京":101190101,"武汉":101200101,
        "杭州":101210101,"合肥":101220101,"龙岩":101230701,"南昌":101240101,"长沙":101250101,
        "贵阳":101260101,"成都":101270101,"广州":101280101,"昆明":101290101,"南宁":101300101,
        "海口":101310101,"香港":101320101,"澳门":101330101,"台北":101340102,"厦门":101230201
        }

def getHTMLText(url,timeout = 30):
    try:
        r = requests.get(url, timeout = 30)       #用requests抓取网页信息
        r.raise_for_status()                      #可以让程序产生异常时停止程序
        r.encoding = r.apparent_encoding          #设置编码标准
        return r.text
    except:
        return '产生异常'
    
 
def get_data(html):
    final_list = []
    soup = BeautifulSoup(html,'html.parser')       #html.parser表示用BeautifulSoup库解析网页
    body  = soup.body                              #取body结构
    data = body.find('div',{'id':'7d'})            #字典参数方式查找
    ul = data.find('ul')
    lis = ul.find_all('li')

 
 
    for day in lis:
        temp_list = []
        
        date = day.find('h1').string             #找到日期
        temp_list.append(date)     
    
        info = day.find_all('p')                 #找到所有的p标签
        temp_list.append(info[0].string)
    
        if info[1].find('span') is None:          #找到p标签中的第二个值'span'标签——最高温度
            temperature_highest = ' '             #用一个判断是否有最高温度
        else:
            temperature_highest = info[1].find('span').string
            temperature_highest = temperature_highest.replace('℃',' ')
            
        if info[1].find('i') is None:              #找到p标签中的第二个值'i'标签——最低温度
            temperature_lowest = ' '               #用一个判断是否有最低温度
        else:
            temperature_lowest = info[1].find('i').string
            temperature_lowest = temperature_lowest.replace('℃',' ')
            
        temp_list.append(temperature_highest)       #将最高气温添加到temp_list中
        temp_list.append(temperature_lowest)        #将最低气温添加到temp_list中
    
        wind_scale = info[2].find('i').string      #找到p标签的第三个值'i'标签——风级，添加到temp_list中
        temp_list.append(wind_scale)
    
        final_list.append(temp_list)              #将temp_list列表添加到final_list列表中
    return final_list
    

#用format()将结果打印输出
def print_data(final_list,num,cityName):
    print("\t\t\t {}一周天气预报".format(cityName))
    print("{:^10}\t{:^8}\t{:^8}\t{:^8}\t{:^8}".format('日期','天气','最高温度','最低温度','风级'))
    for i in range(num):    
        items= final_list[i]
        print("{:^10}\t{:^8}\t{:^8}\t{:^8}\t{:^8}".format(items[0],items[1],items[2],items[3],items[4]))
        
#定义主函数main()
def main():
        
    while (True):
        try:
            cityName = input('请输入城市名称(按q/Q键退出):')
            if cityName == 'q' or cityName == 'Q':
                print("程序结束...")
                break
            cityCode = cityCodeDict[cityName]  #得到城市代码
            url = 'http://www.weather.com.cn/weather/%d.shtml' % cityCode  #得到城市天气网址
            #print(url)
            html = getHTMLText(url)
            final_list = get_data(html)
            print_data(final_list,7,cityName)  #输出天气数据
        except:
            print('未查到%s城市，请重新输入：'%cityName)

if __name__ == '__main__':
    main()

import matplotlib.pyplot as plt
import numpy as np
plt.figure()# 创建figure对象
# 绘制普通图像
x = [21,22,23,24,25,26,27]
y1 = [28,19,16,15,23,23,24]
y2 = [18,16,13,11,15,17,17]
plt.xlabel("date")
# 绘制y1，线条说明为'y1'，线条宽度为2，颜色为红色，线型为虚线，数据标记为圆圈
plt.plot(x, y1, label='Highest temperature',linewidth = 2, linestyle='--', marker='o', color='r')
# 绘制y2，线条说明为'y2'，线条宽度为4，颜色为蓝色，线型为点线，数据标记为'*'
plt.plot(x, y2,'b:*',label='Lowest temperature',linewidth = 4)
plt.legend()# 显示图例
plt.show()# 显示图像

# 创建figure对象
plt.figure()
# 绘制子图1
HT = plt.subplot(2,2,1)
plt.plot([21,22,23,24,25,26,27],[28,19,16,15,23,23,24],'r-o')
plt.title('Highest temperature')
# 绘制子图2
LT = plt.subplot(2,2,2)
plt.plot([21,22,23,24,25,26,27],[18,16,13,11,15,17,17],'g-*')
plt.title('Lowest temperature')

import matplotlib.pyplot as plt
plt.figure(figsize=(10,6))
#天气日期
date = ['21', '22', '23', '24', '25','26','27']
# 21-27日最高温度，最低温度
highest_temperature = [28,19,16,15,23,23,24]
lowest_temperature = [18,16,13,11,15,17,17]
x = list(range(len(highest_temperature)))

#设置间距
total_width, n = 0.8, 3
width = total_width / n
#在偏移间距位置绘制柱状图1
for i in range(len(x)):
    x[i] -= width
plt.bar(x, highest_temperature, width=width, label='Highest temperature', fc='teal')
# 设置数字标签
for a, b in zip(x, highest_temperature):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
             
#在偏移间距位置绘制柱状图2
for i in range(len(x)):
    x[i] += width
plt.bar(x, lowest_temperature, width=width, label='Lowest temperature', tick_label=date, fc='darkorange')
# 设置数字标签
for a, b in zip(x, lowest_temperature):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
        
plt.title("一周天气双重柱状图")
plt.xlabel("date")
plt.ylabel("TEMP(℃)")
plt.legend(loc='lower right')
plt.show()

# 绘制堆叠图
plt.stackplot(date, highest_temperature, lowest_temperature, colors=['teal','darkorange'], labels=['Highest temperature', 'Lowest temperature'])
plt.title("一周天气堆叠图")
plt.xlabel("date")
plt.ylabel("TEMP(℃)")
plt.legend()
plt.show()

#绘制横向柱状图
plt.barh([u'21','22','23','24','25','26','27'], [28,19,16,15,23,23,24])
plt.barh([u'21','22','23','24','25','26','27'], [18,16,13,11,15,17,17])
plt.title("一周天气横向柱状图")
plt.xlabel("TEMP(℃)")
plt.ylabel("DATE")
plt.show()

# 绘制散点图
size1= 500
plt.scatter(date, highest_temperature,size1, color='r', alpha=0.5, marker="o")
plt.scatter(date, lowest_temperature,color='k', s=25, marker="o")
plt.title("一周天气散点图")
plt.xlabel("date")
plt.ylabel("TEMP(℃)")
plt.show()

from matplotlib import pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
#绘制折线图
def Zspot():
    df = pd.DataFrame(pd.read_excel('一周天气.xlsx'))
    x = df.日期
    y1 = df.最高温度
    y2 = df.最低温度
    plt.xlabel("date")
    plt.ylabel("Temp(℃)")
    plt.plot(x,y1,color="red",label="折线")
    plt.plot(x,y2,color="green",label="折线")
    plt.title("一周高温曲线图")
    plt.legend()
    plt.show()
Zspot()
