import re
import csv
import time

import requests
import codecs
from selenium import webdriver


from bs4 import BeautifulSoup

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


# url = "http://100500otvetov.ru/page/vopros-1"
# response = requests.get(url, headers=HEADERS)
# print(response.status_code)
#
# with open("result.txt", "w", encoding="utf-8") as data_file:
#     data_file.write(response.text)

def parse_html(url):
    message = "К сожалению мне не удалось найти ничего интересного"
    # response = requests.get(url)
    # pattern = r"""<table[^>]*?>(.*?)<\/td>"""
    # content = codecs.decode(response.content, 'UTF-8')
    # searched_result = re.search(pattern, content)
    # message_list = searched_result.group(0).split(">")
    # if len(message_list) > 4:
    #     message = message_list[3].split(">wa")[0]

    driver = webdriver.Opera()
    driver.minimize_window()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    # soup = BeautifulSoup(webpage, 'lxml')
    res_question = soup.find("div", class_="panel-body", text=True)
    res_answer = soup.find("div", class_="alert alert-success", text=True)

    res_question_answer = res_answer.text
    res_question_message = res_question.text
    # for val in res:
    #     message = val.get_text()

    return res_question_message, res_question_answer


for idx in range(1, 30001):
    url = f"http://100500otvetov.ru/page/vopros-{idx}"
    print(f"Getting data from: {url}")
    try:
        question, answer = parse_html(url)
        with open("questions_new.csv", "a", encoding="utf-8") as data_file:
            writer = csv.writer(data_file, delimiter=';')
            writer.writerow((question, answer))
    except Exception as ex:
        print(ex)
    time.sleep(0.3)
