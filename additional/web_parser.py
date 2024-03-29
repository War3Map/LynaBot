import requests

from bs4 import BeautifulSoup
from additional.config_loader import get_setting

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/88.0.4324.192 Safari/537.36 OPR/74.0.3911.218 (Edition Yx)',
    'accept': 'text/html,application/xhtml+xml,'
              'application/xml;q=0.9,image/avif,'
              'image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',

}



FACT_URL = "https://randstuff.ru/fact/"
QUOTE_URL = "https://citaty.info/random"


def parse_from_html_test(parse_func, url, params=None):
    """
    Parse html and return result as text
    :param parse_func: function for parsing
    :param url: resourse link for parse
    :param params: parse function params
    :return:
    """
    message = "К сожалению мне не удалось найти ничего интересного"

    response = requests.get(url, headers=HEADERS, params=params)

    # search_result = get_fact_result(response)
    search_result = parse_func(response)

    # print(search_result)
    if search_result is None:
        return message

    message = search_result

    return message


def get_fact_result(response):
    """
    Returns parse result of fact for response
    :param response: request result
    :return:
    """
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        res = soup.find("table", class_="text").findChild("td", recursive=True)
        return res.text
    except Exception as ex:
        print(ex)
        return None


def get_quote_result(response):
    """
    Returns parse result of quote for response
    :param response: request result
    :return:
    """
    soup = BeautifulSoup(response.text, 'lxml')
    text = soup.find("div", class_="field-item even last")
    author = soup.find("div", class_="field-item even")
    source = author.find_next("div", class_="field-item even")

    # print(f"{text}\n{author}:{source}")
    return f"{text.text}\n{author.text} - {source.text}"


def get_fact2_result(response):
    """
    Returns parse result of fact for response: second version
    :param response: request result
    :return:
    """
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        res = soup.find("div", id="quote")
        print(res)
        return res.text
    except Exception as ex:
        print(ex)
        return None


def get_gif_test(response):
    """
    Returns parse result of gif for response
    :param response: request result
    :return:
    """
    # print(response.text)
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        res = soup.find("div", class_="entry").findChild("img")
        return res['src']
    except Exception as ex:
        print(ex)
        return None


PARSERS = {
    "fact": get_fact_result,
    "quote": get_quote_result

}


async def get_info_from_url(url, info_type: str):
    """
    Parse html for info
    :param url:
    :param info_type: "fact" or"quote"
    :return:
    """

    parse_func = PARSERS[info_type] if info_type in PARSERS else PARSERS["fact"]
    return parse_from_html_test(parse_func, url)



def test():
    print(parse_from_html_test(get_quote_result, QUOTE_URL))
    print(parse_from_html_test(get_fact_result, FACT_URL))
    # print(parse_from_html_test(get_fact2_result, "http://webdiscover.ru/facts/"))
    # print(parse_from_html_test(get_gif_test, "https://xdgif.ru/random/"))


if __name__=="__main__":
    test()
