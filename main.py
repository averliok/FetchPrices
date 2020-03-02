#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def create_headless_firefox_browser():
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    return webdriver.Firefox(options=options)
    # Create a headless browser to reduce memory usage


def main():
    brand = input('Название бренда: ')
    address = input('Название парфюма: ').replace(' ', '+')
    browser = create_headless_firefox_browser()
    ilede(brand, address)
    rg(browser, address)
    molecule(browser, brand)
    tsum(browser, address)
    letu(browser, address)
    browser.quit()


def ilede(brand, address):
    url = requests.get('https://iledebeaute.ru/shop/search?q=' + address)
    soup = BeautifulSoup(url.text, 'html.parser')
    names = [i.a.img['alt'] for i in
             soup.findAll('div', {'class': lambda value: value and value.endswith(brand.lower())})]
    # Fetch names within <div> and classes that end with Brand input.
    # Iterate through all instances and return all names of the given class
    prices = [i.span.text for i in
              soup.findAll('div', {'class': lambda value: value and value.endswith(brand.lower())})]
    # Zip lists into DataFrame to export into xlsx/cvs later
    dictionary = dict(zip(names, prices))
    return dictionary


def rg(browser, address):
    browser.get('https://shop.rivegauche.ru/search?text=' + address)
    price_class = browser.find_elements_by_class_name('price')
    prices = []
    for price in price_class:
        prices.append(price.text)
        # Iterate through  corresponding elements and append them to the list
    name_class = browser.find_elements_by_class_name('product__title')
    names = []
    for name in name_class:
        names.append(name.text)
    dictionary = dict(zip(names, prices))
    return dictionary


def molecule(browser, brand):
    browser.get('https://molecule.ru/brand/' + brand + '.html')
    browser.implicitly_wait(4)
    name_class = browser.find_elements_by_class_name('product-title')
    price_class = browser.find_elements_by_class_name('ty-grid-list__price')
    prices = []
    names = []
    while True:
        for name in name_class:
            names.append(name.text)
        for price in price_class:
            prices.append(price.text)
        try:
            browser.find_element_by_class_name('ty-pagination__text-arrow').click()
        except NoSuchElementException:
            break
        # Get on the next page to parse the contents if necessary
    dictionary = dict(zip(names, prices))
    return dictionary


def tsum(browser, address):
    browser.get('https://www.tsum.ru/catalog/search/?q=' + address)
    url = requests.get('https://www.tsum.ru/catalog/search/?q=' + address)
    name_class = browser.find_elements_by_class_name('product__description')
    soup = BeautifulSoup(url.text, 'html.parser')
    names = []
    for name in name_class:
        names.append(name.text)
    prices = []
    for price in soup.findAll('span', attrs={'class': 'price'}):
        prices.append(price.text.replace(b'\xa0'.decode('ISO 8859-1'), ' '))
    dictionary = dict(zip(names, prices))
    return dictionary


def letu(browser, address):
    browser.get('https://www.letu.ru/search?Dy=1&Ntt=' + address)
    price_class = browser.find_elements_by_class_name('products-list-price__number')
    name_class = browser.find_elements_by_class_name('products-list__item-title')
    prices = []
    names = []
    for price in price_class:
        prices.append(price.text)
    for name in name_class:
        names.append(name.text)
    dictionary = dict(zip(names, prices))
    return dictionary


if __name__ == '__main__':
    main()
