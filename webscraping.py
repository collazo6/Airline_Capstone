from collections import defaultdict
import time
import bs4
import selenium
from bs4 import BeautifulSoup
import selenium.webdriver as webd
import pandas as pd
from sqlalchemy import create_engine

def webscrape(airline):
    '''
    INPUT:
    airline: text used to go to reviews website for particular airline

    OUTPUT:
    reviews: list of HTML segments that contains all relevant review information 
    '''
    reviews = []
    browser = webd.Chrome()
    for page_num in range(1,50): 
        url = "http://www.airlinequality.com/airline-reviews/{}/page/{}/?sortby=post_date%3ADesc&pagesize=100".format(airline,page_num)
        browser.get(url)
        time.sleep(5)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        if soup.select('div.col-content article article.list-item'):
            reviews.append(soup.select('div.col-content article article.list-item'))
        else:
            break
    return reviews


def parse_review(review: bs4.element.Tag) -> dict:
    '''
    INPUT:
    review: HTML segment that contains all relevant review information

    OUTPUT:
    d: dictionary of relevant review information
    '''
    d = {}
    if review.select_one("div.rating-10 span"):
        d['rating'] = int(review.select_one("div.rating-10 span").text)
    d['headline'] = review.select_one("h2.text_header").text
    try:
        d['country'] = review.select_one('h3.text_sub_header').text.replace(')','(').split('(')[1]
    except IndexError:
        d['country'] = 'None'
    d['body'] = review.select_one("div.text_content").text.strip()
    rows = review.select('tr')
    for row in rows:
        if row.select('td')[1].attrs['class'][0] == 'review-rating-stars':
            for x in row.select('span'):
                try:
                    if x.attrs['class'] == ['star', 'fill']:
                        num = int(x.text)
                        d[row.td.attrs['class'][1]] = num
                except KeyError:
                    continue
        else:       
            d[row.td.attrs['class'][1]] = row.select('td')[1].text
    return d

def webscrape_manager(airline_list):
    '''
    INPUT:
    airline_list: list of airline names as strings
    
    OUTPUT:
    webscrape_info_dict: dictionary with keys as airline names and values as webscraped html code
    '''
    webscrape_info_dict = {}
    for airline in airline_list:
        webscrape_info_dict[airline] = webscrape(airline)
    return webscrape_info_dict
    
def review_parser(airline_list, webscrape_info_dict):
    '''
    INPUT:
    airline_list: list of airline names as strings
    webscrape_info_dict: dictionary with keys as airline names and values as webscraped html code

    OUTPUT:
    airline_dict: dictionary with keys as airline names and values as their respective reviews
    '''
    airline_dict = defaultdict(list)
    i = 0
    for reviews in webscrape_info_dict.values():
        for review in reviews:
            for r in review:
                airline_dict[airline_list[i]].append(parse_review(r))
        i += 1
    return airline_dict

def copy_to_sql(airline_list,airline_dict,engine)
    '''
    INPUT:
    airline_list: list of airline names as strings
    airline_dict: dictionary with keys as airline names and values as their respective reviews
    engine: directory to SQL database to store webscraped review data

    OUTPUT:
    None
    '''
    for airline in airline_list:
        pd.DataFrame(airline_dict[airline]).to_sql(airline.split('-')[0],con = engine)


if __name__ == "__main__":

    airline_list = ['southwest-airlines','american-airlines','delta-air-lines',
            'united-airlines','ana-all-nippon-airways','japan-airlines','qatar-airways']

    webscrape_info_dict = webscrape_manager(airline_list)
    airline_dict = review_parser(webscrape_info_dict,airline_list)

    engine = create_engine('postgresql://manuelcollazo:manuelcollazo@localhost:5432/airlines')
    copy_to_sql(airline_list,airline_dict,engine = )

        

