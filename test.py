from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver
from os import system
from os import name as osName
import io
import sys
import time

def clear():
    if osName == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()

class LoggingPrinter:
    def __init__(self, filename):
        self.out_file = open(filename, "w")
        self.old_stdout = sys.stdout
        sys.stdout = self
    def write(self, text):
        self.old_stdout.write(text)
        self.out_file.write(text)
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        sys.stdout = self.old_stdout

def main():
    url = "https://coinmarketcap.com/"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)

    driver.get(url)
    scroll_height = driver.execute_script("return document.body.scrollHeight")

    percent = 0.1
    clear()
    print("Loading...")
    while percent <= 1:
        driver.execute_script("window.scrollTo(0, " + str(scroll_height * percent) + ");")
        progress((round(percent * 100)), 100, "%")
        time.sleep(0.1)
        percent += 0.1


    bsoup = BeautifulSoup(driver.page_source, 'html.parser')
    table = bsoup.find('table', class_='cmc-table')
    crypttable = table.find('tbody').find_all('tr', class_='')

    with LoggingPrinter("test.txt"):
        print('{:<3}'.format("#"),
              '{:>20}'.format("Name"),
              '{:<20}'.format(" "),
              '{:<15}'.format("Price"),
              '{:<20}'.format("Market Cap"))

        for crypt in crypttable:
            properties = crypt.find_all('td')
            block = properties[2].find_all('p')
            numberPlate = properties[1].find('p')
            name = block[0]
            reduct = block[1]
            price = properties[3].find('a')
            marketCap = properties[6].find('p')

            print('{:<3}'.format(numberPlate.text), "|",
                  '{:25}'.format(name.text),
                  '{:>6}'.format(reduct.text), "|",
                  '{:>15}'.format(price.text), "|",
                  '{:>20}'.format(marketCap.text))

    word = input()
    with io.open('test.txt', encoding='utf-8') as file:
        for line in file:
            if word in line:
                print(line, end='')

if __name__ == '__main__':
    main()