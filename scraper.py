import json
import re
from bs4 import BeautifulSoup
import smtplib
import time
import cloudscraper
import requests
import colorama
from colorama import Fore, Style
colorama.init(convert=True)

scraper = cloudscraper.create_scraper(browser='chrome')
parser = "html.parser"
urls = ['https://www.roguefitness.com/stainless-steel-ohio-bar',
        'https://www.repfitness.com/rep-competition-bench-with-wide-pad',
        'https://www.repfitness.com/ab-5200-bench',
        'https://www.repfitness.com/pr-4000-power-rack']
options = ['https://www.roguefitness.com/rogue-color-echo-bumper-plate',
           'https://www.repfitness.com/catalog/product/view/id/199/s/rep-color-bumper-plates/category/220/',
           'https://www.repfitness.com/catalog/product/view/id/454/s/rep-iron-plates/category/169/']
reset = Style.RESET_ALL


def check_availability():
    for x in urls:
        try:
            #print("get attempt " + x)

            req = scraper.get(x)
            soup = BeautifulSoup(req.text, parser)
            name = soup.find('title')
            # Check if link is Rogue Fitness
            if "roguefitness" in x:
                script = str(
                    soup.find("script", type='application/javascript'))

                if not re.findall('{"stockStatus":\["In Stock"\]}\)', script):
                    status = "Not In Stock"
                    color = Fore.RED
                else:
                    status = "In Stock"
                    color = Fore.GREEN

                print('[' + str(name.text) + '] ' + color + status + reset)
            # Rep Fitness
            else:

                if not soup.findAll('p', {'class': 'stock available'}):
                    status = "Not In Stock"
                    color = Fore.RED

                else:
                    status = "In Stock"
                    color = Fore.GREEN
                # soup.findAll('p', {'class': 'stock unavailable'})

                print('[' + str(name.text) + '] '+color + status + reset)

            time.sleep(3)
        except cloudscraper.exceptions.CloudflareIUAMError as err:
            print("error: ", err)


def check_options():
    for x in options:
        try:
            #print('get attempt '+x)
            req = scraper.get(x)
            soup = BeautifulSoup(req.text, parser)
            print()
            print(soup.find('title').contents)
        # Check if link is Rogue Fitness
            if "roguefitness" in x:
                divs = soup.findAll(
                    'div', re.compile(r'grouped-item\s+product-purchase-wrapper'))
                for items in divs:
                    name = items.find('div', {'class': 'item-name'})
                    status = items.find(
                        'div', {'class': ['bin-out-of-stock-message bin-out-of-stock-default', 'bin-out-of-stock bin-out-of-stock-cart', 'item-qty input-text']})
                    if re.findall(r'out-of-stock', str(status)):
                        stock = 'Out of Stock'
                        color = Fore.RED
                    else:
                        stock = 'In Stock'
                        color = Fore.GREEN

                    print(str(name.contents)+" "+color+stock+reset)
            else:
                divs = soup.findAll('tr', {'class': ['out-of-stock', '']})

                for items in divs:
                    name = items.find('strong', {'class': 'product-item-name'})
                    status = items.find(
                        'div', {'class': ['stock unavailable', 'control qty']})
                    if re.findall(r'control qty', str(status)):
                        stock = 'In Stock'
                        color = Fore.GREEN

                    else:
                        stock = 'Out of Stock'
                        color = Fore.RED

                    print(str(name.contents)+" "+color+stock+reset)

            time.sleep(3)

        except cloudscraper.exceptions.CloudflareIUAMError as err:
            print("error: ", err)


while(True):
    check_availability()
    check_options()
    time.sleep(600)
