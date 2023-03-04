from bs4 import BeautifulSoup
import requests
import re
import time
import os
from tqdm import tqdm, trange
from datetime import date, timedelta
from argparse import ArgumentParser
import ssl
import pandas as pd
import csv
from datetime import datetime

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


def get_data(url, lang, save_dir, dates):
    header = {"User-Agent": "Mozilla/5.0"}
    url = url.replace("language", args.lang)
    start_date = dates[0]
    end_date = dates[1]
    data = []
    for single_date in daterange(start_date, end_date):
        url_end = single_date.strftime("%Y/%m/%d")
        page_url = url + url_end + "/"
        main_soup = BeautifulSoup(
            requests.get(page_url, headers=header).content, features="html5lib"
        )
        check = main_soup.find_all("section")
        if "Page not found" not in check:
            for elem in main_soup.findAll("ul", attrs={"class": "dayindexTitles"}):
                if elem.a:
                    doc_data = ""
                    news_url = url + elem.a.attrs["href"]
                    try:
                        news_soup = BeautifulSoup(
                            requests.get(news_url, headers=header).content,
                            features="html5lib",
                        )
                    except e:
                        print(
                            f"Network error, process stopped at url, date: {news_url}, {single_date}"
                        )
                    for elem in news_soup.findAll("p"):
                        doc_data += (
                            str(elem)
                            .replace("\n", "")
                            .replace("<p>", "")
                            .replace("<\\p>", "")
                        )
                    data.append(doc_data)
            with open(os.path.join(save_dir, "monolingual.") + CODES[lang], "w") as f:
                f.writelines(data)


def get_structured_data(
    url, lang, save_dir, dates):
    header = {"User-Agent": "Mozilla/5.0"}
    url = url.replace("language", lang)
    start_date = dates[0]
    end_date = dates[1]

        
    for single_date in daterange(start_date, end_date):
        data_dict = {}
        data_df = pd.DataFrame()
        url_end = single_date.strftime("%Y/%m/%d")
        page_url = url + url_end + "/"
        main_soup = BeautifulSoup(
            requests.get(page_url, headers=header).content, features="html5lib"
        )
        topics = []
        if "Page not found" not in main_soup.find_all("section"):
            for elem in main_soup.findAll("h2", attrs={"class": "dayIndexHeading"}):
                topics.append(elem.string)
            index = 0
            for elem in main_soup.findAll("ul", attrs={"class": "dayindexTitles"}):
                if elem.a:
                    doc_data = ""
                    news_url = url + elem.a.attrs["href"]
                    news_soup = BeautifulSoup(
                        requests.get(news_url, headers=header).content,
                        features="html5lib",
                    )
                    for elem in news_soup.findAll("p"):
                        doc_data += (
                            str(elem)
                            .replace("\n", "")
                        )
                    data_dict["date"] = single_date
                    data_dict["news_data"] = doc_data
                    data_dict["category"] = (
                        topics[index].replace("News ›› ", "").strip()
                    )
                    data_dict["url"] = news_url
                    data_df = pd.concat(
                        [data_df, pd.DataFrame([data_dict])], ignore_index=True
                    )
                index += 1
            output_path = os.path.join(save_dir, f"{lang}_data.csv")

            if not os.path.exists(output_path) or os.stat(output_path).st_size == 0:
                data_df.to_csv(output_path, mode="w", index=False)
            else:
                data_df.to_csv(output_path, mode="a", index=False, header=False)


if __name__ == "__main__":
    url = "https://language.oneindia.com/"
    parser = ArgumentParser(
        description="Creating a scraper for getting news data from oneindia.com, in the preferred language. Eg. python3 main.py malayalam ./ ",
        epilog="Use the data well! :)",
    )

    def valid_path(string):
        if os.path.isdir(string):
            return string
        else:
            raise NotADirectoryError(string)

    def valid_lang(string):
        if string in CODES.keys():
            return string
        else:
            raise Exception(
                "LanguageError: Choose one of the supported languages. Check help for details."
            )

    def valid_date(s):
        try:
            return datetime.strptime(s, "%Y/%m/%d")
        except ValueError:
            msg = "Not a valid date: {0!r}".format(s)
            raise argparse.ArgumentTypeError(msg)

    parser.add_argument(
        "-l",
        "--lang",
        metavar="lang",
        type=valid_lang,
        help="The language in which the news article should be scraped. Supported languages - hindi, malayalam, telugu, tamil, kannada, odia, bengali, gujarati",
    )

    parser.add_argument(
        "-sa",
        "--save_dir",
        metavar="save_dir",
        type=valid_path,
        required=False,
        default=".",
        help="The location where the data should be saved",
    )

    parser.add_argument(
        "-s",
        "--start_date",
        metavar="start_date",
        help="The start date - format YYYY/MM/DD",
        default="2000/05/01",
        required=False,
        type=valid_date,
    )

    parser.add_argument(
        "-e",
        "--end_date",
        metavar="end_date",
        help="The end date - format YYYY/MM/DD",
        default = datetime.now().date().strftime("%Y/%m/%d"),
        required=False,
        type=valid_date,
    )

    parser.add_argument(
        "-f",
        "--file_type",
        metavar="file_type",
        type=str,
        required=False,
        default="csv",
        help="The type of file to be returned: csv or text",
    )

    args = parser.parse_args()

    if args.file_type == "csv":
        get_structured_data(
            url, args.lang, args.save_dir, dates=(args.start_date, args.end_date)
        )
    elif args.file_type == "text":
        get_data(url, args.lang, args.save_dir, dates=(args.start_date, args.end_date))
    else:
        print("Invalid file type.")
