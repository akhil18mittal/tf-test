from dateutil import parser
import re


def parse_amount_and_currency(amount_string):
    amount_pattern = r"[\d.,]+"
    currency_pattern = r"[^\d.,\s]+"

    amount = re.search(amount_pattern, amount_string).group(0)
    currency = re.search(currency_pattern, amount_string).group(0)

    # Remove any thousands separators (e.g., '.') and replace the decimal separator (e.g., ',') with a period
    amount = float(amount.replace(',', ''))

    return amount, currency


def parse_year(date_string):
    return parser.parse(date_string).year
