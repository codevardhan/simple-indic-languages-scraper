from bs4 import BeautifulSoup
import requests
import re
import time
from tqdm import tqdm, trange
from datetime import date, timedelta


def daterange(start_date, end_date):
    for n in trange(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def get_data(url, lang):
    end_date = date(2022, 4, 1)
    start_date = date(2000, 5, 1)
    data = []
    for single_date in daterange(start_date, end_date):
        url_end = single_date.strftime("%Y-%m-%d").replace("-", "/") + "/"
        page_url = url + url_end
        main_soup = BeautifulSoup(requests.get(page_url).content, features="html5lib")
        check = main_soup.find_all("section")
        if "Page not found" not in check:
            for elem in main_soup.findAll("ul", attrs={"class": "dayindexTitles"}):
                if elem.a:
                    doc_data = ""
                    news_url = url + elem.a.attrs["href"]
                    news_soup = BeautifulSoup(
                        requests.get(news_url).content, features="html5lib"
                    )
                    for elem in news_soup.findAll("p"):
                        doc_data += str(elem).replace("\n", "")
                    data.append(doc_data)
            with open("monolingual." + lang, "w") as f:
                f.writelines(data)

if __name__ == "__main__":
    get_data("https://telugu.oneindia.com/", "te")