# Indic news data scraper

![Status](https://img.shields.io/badge/status-completed-yellow)<br>
![Issues](https://img.shields.io/badge/issues-0-blue)<br>
[![made-with-Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg)](http://commonmark.org)<br>
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)<br>

A simple scraper to scrape news archives from https://www.oneindia.com in a few low resource languages for use in NLP research/projects.

# Features

- Custom date selector
- Option to get data in a csv file, with category of news, url, news data, and date as row items, or a text file with just data.
- In case of failure, the dates will be displayed, which can then be used as inputs to a custom command. This will append the remaining data to the data file.

# Usage

```bash
python3 main.py -l malayalam
```

This command stores the structured news data in a csv file "malayalam_data.csv" in the current directory. The articles selected from would be from 2000/05/01 to the current date.

```bash
python3 main.py -l malayalam -s 2023/02/01 -e 2023/02/20 -f text -sa ./output/
```

This command stores the raw news data in a file "monolingual.ml" in a directory named "output". The articles selected from would be from 2023/02/01 to 2023/02/20.

# How it works
Takes in the language and save directory (defaults to current directory) as arguments. Language arguments are listed below.
<ul>
  <li>malayalam</li>
  <li>telugu</li>
  <li>kannada</li>
  <li>tamil</li>
  <li>odia</li>
  <li>bengali</li>
  <li>gujarati</li>
  <li>hindi</li>
</ul> 

## Technology Stack 💻
- Python
- BeautifulSoup


## Future Scope

Open to suggestions ^.^