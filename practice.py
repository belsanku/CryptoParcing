from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import time
from os import system
from os import name as os_name
import sys
import io

class Currency:
    def __init__(self, name, abb, price, market_cap):
        self.name = name
        self.abb = abb
        self.price = price
        self.market_cap = market_cap

def find(word):
	with io.open('dogecointhebest.txt') as file:
		for line in file:
			if word in line:
				print(line, end='\n')

def main():
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--log-level=1")
	driver = webdriver.Chrome('./chromedriver', options=chrome_options)
	info = dict()
	i = 1
	while i < 10:
		url = 'https://coinmarketcap.com/?page=' + str(i)
		driver.get(url)
		scroll_height = driver.execute_script("return document.body.scrollHeight")
		percent = 0.1
		print("Page " + str(i) + " Loading...")
		while percent <= 1:
			driver.execute_script("window.scrollTo(0, " + str(scroll_height * percent) + ");")
			time.sleep(0.3)
			percent += 0.1
		html = driver.page_source
		soup = BeautifulSoup(html, 'lxml')
		cmc_table = soup.find('table', class_='cmc-table')
		if cmc_table is None:
			print("Nothing is loaded, goodbye very well")
			break
		money_tr_arr = cmc_table.find('tbody').find_all('tr', class_=None)
		for money in money_tr_arr:
			properties = money.find_all('td')
			currency_block = properties[2].find_all('p')
			name = currency_block[0].text
			abb = "--" if currency_block[1] is None else currency_block[1].text
			price = properties[3].find('a')
			price = "--" if price is None else price.text
			market_cap = properties[6].find('p')
			market_cap = "--" if market_cap is None else market_cap.text
			info[name] = (Currency(name, abb, price, market_cap))
		i += 1
	driver.close();
	max_name_len = 0
	cnt = 0
	for currency in info.keys():
		if len(info[currency].name) > max_name_len:
			max_name_len = len(info[currency].name)
	format_str = "%" + str(max_name_len  + 3) + "s\t%-10s\t%24s\t%24s\t"
	print(format_str % ("Name", "", "Price", "Market cap"))
	f = open('dogecointhebest.txt', 'w', encoding = 'utf-8')

	try:
		for currency in info.keys():
			f.write(info[currency].name +" "+ info[currency].abb +" "+ info[currency].price +" "+ info[currency].market_cap +" "+ '\n')
			cnt+=1
			print(format_str % (
				info[currency].name, info[currency].abb, info[currency].price,
				info[currency].market_cap))
	finally:
		f.close()
	print(cnt)
	while 1:
		print("What do you want to find? Print 'Goodbye' if you want to quit")
		NeedToFind = input()
		if NeedToFind == "Goodbye":
			return 228
		find(NeedToFind);
	
if __name__ == '__main__':
    main()