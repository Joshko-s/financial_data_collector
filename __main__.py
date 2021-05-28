from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import time
from tabulate import tabulate


def get_input():
    user_input = input()
    stocks = user_input.split(' ')
    return stocks


def get_data(stocks):
    relevant_pages = []
    for stock in stocks:
        url = 'https://de.finance.yahoo.com/quote/' + str(stock)
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, 'html.parser')
        relevant_pages.append(soup)
        time.sleep(1)
    return relevant_pages


def find_relevant_stats(stocks, relevant_pages):
    stats = []
    index = 0

    for page in relevant_pages:
        items = []
        names_values = []
        names_values.append(stocks[index])
        names_values.append(' ')
        items.append(names_values)
        data = page.find_all('td')
        for code in data:
            if 'data-test' in str(code):
                    names_values = []
                    code = re.split('"|<|>', str(code))
                    names_values.append(code[6])
                    names_values.append(code[-5])
                    items.append(names_values)
        stats.append(items)
        index = index + 1
    return stats


def create_tables(filtered_data):
    for stock_data in filtered_data:
        print(tabulate(stock_data))



stocks = get_input()
relevant_pages = get_data(stocks)
filtered_data = find_relevant_stats(stocks, relevant_pages)
create_tables(filtered_data)
