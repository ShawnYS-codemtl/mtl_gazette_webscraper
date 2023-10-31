October 30th, 2023

The program is a web scraper for this news website: https://montrealgazette.com/category/news/.

It collects the trending articles from the url provided above, and scrapes information from 
those articles and writes it into a json file. The data collected includes the title, publication date, author, and subtitle of the article. 

USAGE:

In the terminal, change to the directory where the file is located and type:
python3 collect_trending.py -o <output_file.json>

LIBRARIES USED:
pathlib
requests
argparse
bs4 (Beautiful Soup)
json



