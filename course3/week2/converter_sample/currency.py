from bs4 import BeautifulSoup
from decimal import Decimal


def convert(amount, cur_from, cur_to, date, requests):
    # response = requests.get()  # Использовать переданный requests
    response = requests.get("http://www.cbr.ru/scripts/XML_daily.asp",
                        params={'date_req': date})
    soup = BeautifulSoup(response.content, "xml")

    def get_nominal(soup, cur):
        return int(soup.find("CharCode", text=cur).find_next_sibling("Nominal").string)

    def get_rate(soup, cur):
        """rate cur_from to rub, rub per cur"""
        raw_rate = Decimal(soup.find("CharCode", text=cur).find_next_sibling("Value").string.replace(",", ".")) \
            if cur != "RUR" else Decimal("1")
        nominal = get_nominal(soup, cur) if cur != "RUR" else 1
        return raw_rate / nominal

    rate_from = get_rate(soup, cur_from)
    rate_to = get_rate(soup, cur_to)
    result = amount * rate_from / rate_to

    # result = Decimal('3754.8057')
    return result.quantize(Decimal('1.0000'))  # не забыть про округление до 4х знаков после запятой

from bs4 import BeautifulSoup
from decimal import Decimal

# variant from teachers
def convert_(amount, cur_from, cur_to, date, requests):
    result = requests.get("http://www.cbr.ru/scripts/XML_daily.asp", {"date_req": date})
    soup = BeautifulSoup(result.content, 'xml')
    rates = {i.CharCode.string: (
            Decimal(i.Value.string.replace(',', '.')),
            int(i.Nominal.string)
        ) for i in soup('Valute')
    }
    rates['RUR'] = (Decimal(1), 1)

    result = amount * rates[cur_from][0] * rates[cur_to][1] / rates[cur_from][1] / rates[cur_to][0]
    return result.quantize(Decimal('.0001'))
