# Indic news data scraper

![Status](https://img.shields.io/badge/status-completed-yellow)<br>
![Issues](https://img.shields.io/badge/issues-0-blue)<br>
[![made-with-Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg)](http://commonmark.org)<br>
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)<br>

A simple scraper to scrape news archives from https://www.oneindia.com in a few low resource languages for use in NLP research/projects.

# Usage

```bash
python3 main.py malayalam ./
```
This command stores the raw news data in a file "monolingial.ml" in the current directory.
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

Add custom date selector argument to get the data of a specific date period. Currently defaults to Jan 1st 2022 - 2000 May 5th.