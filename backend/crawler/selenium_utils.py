from selenium.common import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

from selenium import webdriver

from .models import Loan, Country, Sector
from .utils import parse_amount_and_currency, parse_year


def setup_webdriver():
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920x1080')
    driver = webdriver.Remote("http://selenium:4444/wd/hub", options.to_capabilities())

    return driver


def navigate_to_website(driver):
    url = 'https://www.eib.org/en/projects/loans/index.htm?q=&sortColumn=loanParts.loanPartStatus.statusDate&sortDir=desc&pageNumber=0&itemPerPage=25&pageable=true&language=EN&defaultLanguage=EN&loanPartYearFrom=1959&loanPartYearTo=2023&orCountries.region=true&orCountries=true&orSectors=true'
    driver.get(url)


def change_pagination(driver):
    select_element_id = 'show-entries'
    wait = WebDriverWait(driver, 60)
    wait.until(EC.presence_of_element_located((By.ID, select_element_id)))

    pagination_select = Select(driver.find_element(by=By.ID, value=select_element_id))
    pagination_select.select_by_value('100')


def wait_for_articles_to_load(driver):
    wait = WebDriverWait(driver, 60)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'article')))
    wait.until(lambda driver: len(driver.find_elements(by=By.TAG_NAME, value='article')) >= 100)


def get_articles(driver):
    return driver.find_elements(by=By.TAG_NAME, value='article')


def process_articles(articles):
    for article in articles:
        try:
            date_string = article.find_element(by=By.CLASS_NAME, value="row-date").text
            title = article.find_element(by=By.CLASS_NAME, value="row-title").text
            country_element = article.find_elements(by=By.CSS_SELECTOR, value=".row-tags > span > a")
            country = country_element[0].text if country_element else ""
            sector = article.find_elements(by=By.CSS_SELECTOR, value=".row-tags > span")[-1].text
            amount_string = article.find_element(by=By.CSS_SELECTOR, value=".col-md-2.col-xs-12 > div").text

            year = parse_year(date_string)
            amount, currency = parse_amount_and_currency(amount_string)

            save_data_to_db(title, country, sector, amount, currency, year)
        except NoSuchElementException:
            pass


def save_data_to_db(title, country, sector, amount, currency, year):
    country, _ = Country.objects.get_or_create(name=country)
    sector, _ = Sector.objects.get_or_create(name=sector)

    Loan.objects.get_or_create(
        borrower=title,
        amount=amount,
        country=country,
        currency=currency,
        sector=sector,
        year=year
    )
