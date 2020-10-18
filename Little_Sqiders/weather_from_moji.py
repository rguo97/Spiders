import requests
from bs4 import BeautifulSoup
import time


def get_url():
	print("请输入你要查询的省份: (请输入正确的拼音)")
	province=input()
	print("请输入你要查询的城市: (请输入正确的拼音)")
	city=input()
	ur2='https://tianqi.moji.com/weather/china/{}/{}'.format(province,city)
	return ur2

def show(page):
	soup=BeautifulSoup(page.text,'html.parser')
	positon=soup.find('div','search_default')
	print("\n您查询的地点是: "+positon.em.text+"     时间: "+time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())))
	temperature=soup.find("div",'wea_weather clearfix')
	print("温度是: "+temperature.em.text+"摄氏度");
	print("天气情况是: "+temperature.b.text)
	humidity=soup.find("div","wea_about clearfix")
	print(humidity.span.text+","+humidity.em.text)
	air_quality=soup.find("div","wea_alert clearfix")
	print("空气质量指数: "+air_quality.em.text)
	tip=soup.find("div","wea_tips clearfix")
	print("贴心小提示: "+tip.em.text)
	print("!!-----以上数据来源于墨迹天气-----!!\n")

def menu():
	print("********************************")
	print("********1.查询城市天气**********")
	print("********2.显示所有省会天气******")
	print("********3.返回菜单**************")
	print("********4.退出程序**************")
	print("********************************")

headers= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
m=0
while(m!=4):
	menu()
	print("请输入选项:")
	m=input()
	while(int(m)>4 or int(m)<=0):
		print("请重新输入选项:")
		m=input()

	if(int(m)==1):
		url=get_url()
		page=requests.get(url,headers=headers)
		show(page)

	if(int(m)==2):
		print("\n此功能还待开发，请耐心等待！\n")
	if(int(m)==3):
		menu()
