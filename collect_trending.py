from pathlib import Path
import requests
import argparse
import bs4
import json

def get_trending_articles(name):

    fpath = Path(f"{name}.html")
    headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'} 

    if not fpath.exists():
        data = requests.get("https://montrealgazette.com/category/news/", headers=headers)

        with open(fpath, "w") as f:
            f.write(data.text)

    with open(fpath) as f:
        return f.read()
    
def get_trending_info(name, url):
    fpath = Path(f"{name}.html")
    headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}

    if not fpath.exists():
        data = requests.get(url, headers=headers)

        with open(fpath, "w") as f:
            f.write(data.text)

    with open(fpath) as f:
        return f.read()


REL_TABLE_FIELDS = [
    "TITLE",
    "PUBLICATION_DATE",
    "AUTHOR",
    "BLURB"
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output_json_file", help="output_json_file")
    args = parser.parse_args()

    output_filepath = args.output_json_file

    html_data = get_trending_articles("main_page")

    # contains an Object oriented representation of the entire website 
    soup = bs4.BeautifulSoup(html_data, "html.parser")

    trending_div = soup.find("div", class_="list-widget-trending")
    ol_list_content = trending_div.find("ol", class_="list-widget__content")
    articles = ol_list_content.find_all("li")
    a_link = ol_list_content.find("a", class_="article-card__image-link")

    json_list = {"data":[]} 
    nb = 1
    for i, article in enumerate(articles):

        link = article.find("a")
        link_url = "https://montrealgazette.com" + link["href"]

        html_article_data = get_trending_info(f"article{nb}", link_url)
        soup2 = bs4.BeautifulSoup(html_article_data, "html.parser")

        #print(link_url)

        article_info_div = soup2.find("div", class_="article-header__detail__texts")
        try:
            rel_title = article_info_div.find("h1").text.strip()
            rel_blurb = article_info_div.find("p", class_="article-subtitle").text.strip()
            rel_author = article_info_div.find("span", class_="published-by__author").find("a").text.strip()
            rel_publication_date = article_info_div.find("span", class_="published-date__since").text.strip()

        except AttributeError:
            pass

        nb += 1
        relationship = {}
        data = [rel_title, rel_publication_date, rel_author, rel_blurb]

        for field, info in zip(REL_TABLE_FIELDS, data):
            relationship[field] = info
        
        json_list["data"].append(relationship)

    
    with open(output_filepath, 'w') as f:
        json.dump(json_list, f, indent = 4)

if __name__ == "__main__":
    main()
