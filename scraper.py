import requests
import csv
import re
from bs4 import BeautifulSoup


def get_html(url):
    request = requests.get(url)
    if request.status_code == 200:
        return request.text
    return False


def get_sources(source):
    sources = []
    with open(source, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            sources.append(row[0])
    return sources


def store_scraped_data(sources):
    for source in sources:
        html = get_html(source)
        soup = BeautifulSoup(html, 'html.parser')

        name = soup.find(
            "h1", {"class": "ty-product-block-title"}).text

        price = soup.find("span", {"class": "price_inner--amount"}).span.text

        discount = 0
        if(soup.find("span", {"class": "labels-zbritje"})):
            discount = soup.find(
                "span", {"class": "labels-zbritje"}).text.split("%")[0]
            discount = int(re.findall('[0-9]+', discount)[0])

        stock = soup.find(
            "div", {"class": "product-price_info--status"}).strong.text
        stock = int(re.findall('[0-9]+', stock)[0])

        data = [name, price, discount, stock]

        with open('product-details.txt ', 'a', newline='') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_NONE,
                                delimiter=',', quotechar='', escapechar='\\')
            writer.writerow(data)
            print('"' + name + '"' + ' is being stored...')


sources_csv = 'sources.csv'
sources = get_sources(sources_csv)
store_scraped_data(sources)
