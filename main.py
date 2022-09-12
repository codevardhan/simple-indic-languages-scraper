from bs4 import BeautifulSoup
import requests
import re
import time
import os
from tqdm import tqdm, trange
from datetime import date, timedelta
from argparse import ArgumentParser

CODES = {
    "telugu": "te",
    "malayalam": "ml",
    "bengali": "bn",
    "gujarati": "gj",
    "hindi": "hn",
    "tamil": "tn",
    "odia": "od",
    "kannada": "kn",
}


def daterange(start_date, end_date):
    for n in trange(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def get_data(url, lang, save_dir):
    url = url.replace("language", args.lang)
    end_date = date(2022, 4, 1)
    start_date = date(2000, 5, 1)
    data = []
    for single_date in daterange(start_date, end_date):
        url_end = single_date.strftime("%Y-%m-%d").replace("-", "/") + "/"
        page_url = url + url_end
        print(page_url)
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
            with open(os.path.join(save_dir, "monolingual.") + CODES[lang], "w") as f:
                f.writelines(data)


if __name__ == "__main__":
    url = "https://language.oneindia.com/"
    parser = ArgumentParser(
        description="Creating a scraper for getting news data from oneindia.com, in the preferred language.",
        epilog="Use the data well! :)",
    )

    def dir_path(string):
        if os.path.isdir(string):
            return string
        else:
            raise NotADirectoryError(string)

    def def_lang(string):
        if string in CODES.keys():
            return string
        else:
            raise Exception(
                "LanguageError: Choose one of the supported languages. Check help for details."
            )

    parser.add_argument(
        "lang",
        metavar="lang",
        type=def_lang,
        help="The language in which the news article should be scraped. Supported languages - hindi, malayalam, telugu, tamil, kannada, odia, bengali, gujarati",
    )

    parser.add_argument(
        "--save_dir",
        metavar="save_dir",
        type=dir_path,
        required=False,
        default=".",
        help="The location where the data should be saved",
    )

    args = parser.parse_args()

    get_data(url, args.lang, args.save_dir)
