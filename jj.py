# -*- coding: utf-8 -*-

# 功能：查询城市天气
import requests, json, re
from matplotlib import pyplot as plt
import os


# 获取城市代码
def getCityCode(city):
    url = 'http://toy1.weather.com.cn/search?cityname=' + city
    r = requests.get(url)
    if len(r.text) > 4:
        json_arr = json.loads(r.text[1:len(r.text) - 1])
        code = json_arr[0]['ref'][0:9]
        return code
    else:
        return "000000000"


# 获取城市天气信息
def getWeatherInfo(city):
    code = getCityCode(city)
    url = 'http://t.weather.sojson.com/api/weather/city/' + code
    r = requests.get(url)
    info = r.json()
    weather = {}
    if info['status'] == 200:
        weather['城市：'] = info['cityInfo']['parent'] + info['cityInfo']['city']
        weather['时间：'] = info['time'] + ' ' + info['data']['forecast'][0]['week']
        weather['温度：'] = info['data']['forecast'][0]['high'] + ' ' + info['data']['forecast'][0]['low']
        weather['天气：'] = info['data']['forecast'][0]['type']
    else:
        weather['错误：'] = '[' + city + ']不存在！'
    return weather


# 打印天气信息
def printWeatherInfo(weather):
    zifu1=''
    for key in weather:
        # print(key + weather[key])
        zifu1+=key + weather[key]+'<br/>'
    return zifu1


# 获取未来气温
def getTemperatures(city):
    code = getCityCode(city)
    url = 'http://t.weather.sojson.com/api/weather/city/' + code
    r = requests.get(url)
    info = r.json()
    temperatures = {}
    if info['status'] == 200:
        forecast = info['data']['forecast']
        for i in range(len(forecast)):
            dayinfo = forecast[i]
            high = int(re.findall(r'\d+', dayinfo['high'])[0])
            low = int(re.findall(r'\d+', dayinfo['low'])[0])
            temperatures[dayinfo['ymd']] = [high, low]
    else:
        temperatures['错误：'] = '[' + city + ']不存在！'
    return temperatures


# 打印未来气温
def printTemperatures(temperatures):
    zifu2=''
    if '错误：' not in temperatures.keys():
        for key in temperatures:
            # print(key + ' 高温：' + str(temperatures[key][0]) + ' 低温：' + str(temperatures[key][1]))
            dgh=key + ' 高温：' + str(temperatures[key][0]) + ' 低温：' + str(temperatures[key][1])+'<br/>'
            zifu2 += dgh
        return zifu2
        # 绘制未来气温折线图


def drawTemperatureLineChart(city):
    city=city
    plt.rcParams['font.sans-serif'] = ['SimHei']

    plt.rcParams['axes.unicode_minus'] = False
    temperatures = getTemperatures(city)
    if '错误：' not in temperatures.keys():
        dates = []
        highs = []
        lows = []
        for key in temperatures:
            dates.append(key)
            highs.append(temperatures[key][0])
            lows.append(temperatures[key][1])
        # 设置图标的图形格式


        fig = plt.figure(dpi=128, figsize=(10, 6))
        plt.xlabel('Date (YYYY-MM-DD)', fontsize=10)
        plt.ylabel("Temperature (℃)", fontsize=10)
        fig.autofmt_xdate()
        plt.plot(dates, highs, c='red', alpha=0.5)
        plt.plot(dates, lows, c='blue', alpha=0.5)
        plt.title('Recent weather conditions', fontsize=24)
        # plt.show()
        plt.savefig('近期天气情况.png')



        fig = plt.figure(dpi=128, figsize=(10, 6))

        # 绘制堆叠图
        plt.stackplot(dates, highs, lows, colors=['teal', 'darkorange'],
                      labels=['Highest temperature', 'Lowest temperature'])
        plt.xticks(rotation=70) # 倾斜70度
        plt.title("Weather stack")
        plt.xlabel("date", fontsize=10)
        plt.ylabel("TEMP(℃)", fontsize=10)
        plt.legend()
        # plt.show()
        plt.savefig('天气堆叠图.png')


        fig = plt.figure(dpi=128, figsize=(10, 6))

        # 绘制散点图
        size1 = 500
        plt.scatter(dates, highs, size1, color='r', alpha=0.5, marker="o")
        plt.scatter(dates, lows, color='k', s=25, marker="o")
        plt.xticks(rotation=70) # 倾斜70度
        plt.title("Weather scatter")
        plt.xlabel("date")
        plt.ylabel("TEMP(℃)")
        # plt.show()

        plt.savefig('天气散点图.png')


        vfig = plt.figure(dpi=128, figsize=(10, 6))
        x = list(range(len(highs)))

        # 设置间距
        total_width, n = 0.8, 3
        width = total_width / n
        # 在偏移间距位置绘制柱状图1
        for i in range(len(x)):
            x[i] -= width
        plt.bar(x, highs, width=width, label='Highest temperature', fc='teal')
        # 设置数字标签
        for a, b in zip(x, highs):
            plt.text(a, b, b, ha='center', va='bottom', fontsize=10)

        # 在偏移间距位置绘制柱状图2
        for i in range(len(x)):
            x[i] += width
        plt.bar(x, lows, width=width, label='Lowest temperature', tick_label=dates, fc='darkorange')
        plt.xticks(rotation=70) # 倾斜70度

        # 设置数字标签
        for a, b in zip(x, lows):
            plt.text(a, b, b, ha='center', va='bottom', fontsize=10)

        plt.title("Double histogram")
        plt.xlabel("date")
        plt.ylabel("TEMP(℃)")
        plt.legend(loc='lower right')
        # plt.show()

        plt.savefig('天气双重柱状图.png')


        fig = plt.figure(dpi=128, figsize=(10, 10))

        # 绘制横向柱状图
        plt.barh(dates, highs)
        plt.barh(dates, lows)
        plt.title("Horizontal bar chart")
        plt.xlabel("TEMP(℃)")
        plt.ylabel("DATE")
        # plt.show()
        plt.savefig('天气横向柱状图.png')



        fig = plt.figure(dpi=128, figsize=(10, 6))  # 创建figure对象
        # 绘制普通图像
        x = dates
        y1 = highs
        y2 = lows
        plt.xlabel("date")
        # 绘制y1，线条说明为'y1'，线条宽度为2，颜色为红色，线型为虚线，数据标记为圆圈
        plt.plot(x, y1, label='Highest temperature', linewidth=2, linestyle='--', marker='o', color='r')
        # 绘制y2，线条说明为'y2'，线条宽度为4，颜色为蓝色，线型为点线，数据标记为'*'
        plt.plot(x, y2, 'b:*', label='Lowest temperature', linewidth=4)
        plt.xticks(rotation=70)  # 倾斜70度
        plt.legend()  # 显示图例
        # plt.show()  # 显示图像
        plt.savefig('绘制普通图像.png')


        fig = plt.figure(dpi=128, figsize=(10, 6))



        HT = plt.subplot(2, 2, 1)
        plt.plot(dates, highs, 'r-o')
        plt.xticks(rotation=70)  # 倾斜70度
        plt.title('Highest temperature')
        # 绘制子图2
        LT = plt.subplot(2, 2, 2)
        plt.plot(dates, lows, 'g-*')
        plt.xticks(rotation=70)  # 倾斜70度
        plt.title('Lowest temperature')
        plt.legend()
        # plt.show()
        plt.savefig('双折线图.png')




def main(city):



    # city = input('输入城市名：')
    city = city
    getWeatherInfo(city)
    e = printWeatherInfo(getWeatherInfo(city))
    # print(e)
    k = printTemperatures(getTemperatures(city))
    drawTemperatureLineChart(city)
    # print(k)
    zifu3 = e + '<br/>' + k
    # print(zifu3)

    return zifu3

if __name__ == '__main__':
    main('shanghai')
