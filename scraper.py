import json
import re
from bs4 import BeautifulSoup
import smtplib
import time
import cloudscraper

scraper = cloudscraper.create_scraper(browser='chrome')
rogueStock = 'stockStatus'
urls = ['https://www.roguefitness.com/stainless-steel-ohio-bar',
        'https://www.repfitness.com/strength-equipment/power-racks/pr-4000-series/pr-4000-power-rack',
        'https://www.roguefitness.com/stainless-steel-ohio-bar',
        'https://www.repfitness.com/rep-competition-bench-with-wide-pad',
        'https://www.repfitness.com/ab-5200-bench',
        'https://www.repfitness.com/pr-4000-power-rack',
        'https://www.repfitness.com/catalog/product/view/id/199/s/rep-color-bumper-plates/category/220/',
        'https://www.roguefitness.com/rogue-color-echo-bumper-plate'
        ]


def check_availability():
    parser = "html.parser"
    while True:
        try:
            req = scraper.get(urls[0])
            print("request.get attempt")
        except cloudscraper.exceptions.CloudflareIUAMError as err:
            print("Http Error: ", err)
            time.sleep(300)
        break

    soup = BeautifulSoup(req.text, parser)
    # try:
    tag = str(soup.find("script", type='application/javascript'))
    print(re.findall('{"stockStatus":\[[^\s]+\]}\);', tag))


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
    check_availability()
    time.sleep(300)
