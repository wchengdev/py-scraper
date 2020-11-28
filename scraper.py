import json
import re
from bs4 import BeautifulSoup
import smtplib
import time
import cloudscraper
import requests

scraper = cloudscraper.create_scraper(browser='chrome')
parser = "html.parser"
urls = ['https://www.roguefitness.com/stainless-steel-ohio-bar',
        'https://www.repfitness.com/rep-competition-bench-with-wide-pad',
        'https://www.repfitness.com/ab-5200-bench',
        'https://www.repfitness.com/pr-4000-power-rack']
options = ['https://www.roguefitness.com/rogue-color-echo-bumper-plate',
           'https://www.repfitness.com/catalog/product/view/id/199/s/rep-color-bumper-plates/category/220/',
           'https://www.repfitness.com/catalog/product/view/id/454/s/rep-iron-plates/category/169/']


def check_availability():
    for x in urls:
        try:
            #print("get attempt " + x)

            req = scraper.get(x)
            soup = BeautifulSoup(req.text, parser)

            # Check if link is Rogue Fitness
            if "roguefitness" in x:
                script = str(
                    soup.find("script", type='application/javascript'))
                if not re.findall('{"stockStatus":\["In Stock"\]}\)', script):
                    status = "Not In Stock"
                else:
                    status = "In Stock"
                name = soup.find('title')
                print('[' + str(name.text) + '] '+status)
            # Rep Fitness
            else:
                if not soup.findAll('p', {'class': 'stock available'}):
                    status = "Not In Stock"
                else:
                    status = "In Stock"
                # soup.findAll('p', {'class': 'stock unavailable'})
                name = soup.find('title')
                print('[' + str(name.text) + '] '+status)

            time.sleep(3)
        except cloudscraper.exceptions.CloudflareIUAMError as err:
            print("error: ", err)


def check_options():
    for x in options:
        try:
            #print('get attempt '+x)
            req = scraper.get(x)
            soup = BeautifulSoup(req.text, parser)

        # Check if link is Rogue Fitness
            if "roguefitness" in x:
                divs = soup.findAll(
                    'div', re.compile(r'grouped-item\s+product-purchase-wrapper'))
                print(soup.find('title').contents)
                for items in divs:
                    name = items.find('div', {'class': 'item-name'})
                    status = items.find(
                        'div', {'class': ['bin-out-of-stock-message bin-out-of-stock-default', 'bin-out-of-stock bin-out-of-stock-cart', 'item-qty input-text']})
                    if re.findall(r'out-of-stock', str(status)):
                        stock = 'Out of Stock'
                    else:
                        stock = 'In Stock'

                    print(str(name.contents)+" "+stock)
            else:
                divs = soup.findAll('tr', {'class': ['out-of-stock', '']})
                print(soup.find('title').contents)
                for items in divs:
                    name = items.find('strong', {'class': 'product-item-name'})
                    status = items.find(
                        'div', {'class': ['stock unavailable', 'control qty']})
                    if re.findall(r'control qty', str(status)):
                        stock = 'In Stock'
                    else:
                        stock = 'Out of Stock'
                    print(str(name.contents)+" "+stock)

            time.sleep(3)

        except cloudscraper.exceptions.CloudflareIUAMError as err:
            print("error: ", err)

# def send_mail(title, price, link):
#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.ehlo()
#     server.starttls()
#     server.ehlo()

#     server.login('', '')
#     subject = title + " is back in stock!"
#     body = title + " is now in stock for $" + str(price)

#     print(title, price)

#     msg = f"Subject: {subject}\n\n{body}"
#     server.sendmail('', '', msg)
#     server.quit()


while(True):
    # check_availability()
    check_options()
    time.sleep(300)
