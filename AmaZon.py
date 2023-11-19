from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service 
from lxml.html import fromstring
import csv

class Amazon():
    def __init__(self) -> None:
        pass

    def Header(self):
        Header = ['Product Name', 'Product Url', 'Product Image', 'Availability', 'Total Review', 'Price']
        with open(file='Amazon.csv', mode='a', newline='') as file:
            CsvWriter = csv.writer(file)
            CsvWriter.writerow(Header)
    
    def Mysearch(self):
        MySearch = input('Enter your Search: ')
        SearchUrl = f'https://www.amazon.com/s?k={MySearch}'
        WebUrl = '+'.join(SearchUrl.split())
        return WebUrl

    def ParseData(self,HTML):
        AllData = fromstring(HTML)
        Boxes = AllData.xpath('//span[@data-component-type="s-search-results"]//div[@data-component-type="s-search-result"]')
        for box in Boxes:
            ProductUrl = 'https://www.amazon.com' + box.find('.//h2/a').get('href')
            ProductName = box.find('.//h2/a/span').text
            print(f"[INFO] Geting Product Name:- {ProductName}")
            ImageLink = box.find('.//img[@data-image-latency="s-product-image"]').get('src')
            PriceTag = box.find('.//span[@class="a-offscreen"]')
            if PriceTag != None:
                Price = PriceTag.text
            else:
                Price = None
            ReviewTag = box.find('.//span[@class="a-size-base s-underline-text"]')
            if ReviewTag != None:
                TotalReview = ReviewTag.text
            else:
                TotalReview = ''
            Ships = box.find('.//span[@class="a-size-small a-color-base"]')
            if Ships != None:
                Avaiablity = Ships.text
            else:
                Avaiablity = ''
            Row = [ProductName,ProductUrl,ImageLink,Avaiablity,Ships,TotalReview,Price]
            self.savedata(Row)
    
    def savedata(self,row):
        with open(file='AmaZon.csv', mode='a', newline='', encoding='UTF-8') as file:
            csv.writer(file).writerow(row)
    
Myclass = Amazon()
# driverPath = ChromeDriverManager().install()
# Servc = Service(driverPath)
Myclass.Header()
browser = webdriver.Chrome()
WebUrl = Myclass.Mysearch()
StartPage = int(input('Enter the page where you want to start: '))
EndPage = int(input('Enter the page where you want to end: ')) + 1
# print(f"[Info] Do you want to delete all data and add new data! ")
# answer = input('enter your decision (y/n):- ')
for page in range(StartPage, EndPage):
    Url = f"{WebUrl}&page={page}"
    browser.get(Url)
    Html = browser.page_source
    Myclass.ParseData(Html)
