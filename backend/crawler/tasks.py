import logging

from celery import shared_task
from .selenium_utils import setup_webdriver, navigate_to_website, change_pagination, wait_for_articles_to_load, \
    get_articles, process_articles


logger = logging.getLogger(__name__)


@shared_task
def scrape_article_from_url():
    logger.info("Starting scrape_article_from_url function")

    driver = setup_webdriver()

    navigate_to_website(driver)

    change_pagination(driver)

    wait_for_articles_to_load(driver)

    articles = get_articles(driver)

    logger.info("Found {} articles".format(len(articles)))

    process_articles(articles)

    logger.info("Finished processing articles")

    driver.quit()
    logger.info("Completed scrape_article_from_url function")

