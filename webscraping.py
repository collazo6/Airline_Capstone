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


if __name__ == "__main__":

    southwest_reviews = webscrape('southwest-airlines')
    american_reviews = webscrape('american-airlines')
    delta_reviews = webscrape('delta-air-lines')
    united_reviews = webscrape('united-airlines')

    ana_reviews = webscrape('ana-all-nippon-airways')
    japan_reviews = webscrape('japan-airlines')

    qatar_reviews = webscrape('qatar-airways')
    i = 0
    airline = ['southwest-airlines','american-airlines','delta-air-lines','united-airlines','ana-all-nippon-airways','japan-airlines','qatar-airways']
    airline_dict = defaultdict(list)
    for reviews in [southwest_reviews,american_reviews,delta_reviews,united_reviews,ana_reviews,japan_reviews,qatar_reviews]:
        for review in reviews:
            for r in review:
                airline_dict[airline[i]].append(parse_review(r))
        i += 1

    southwest_df = pd.DataFrame(airline_dict['southwest-airlines'])
    american_df = pd.DataFrame(airline_dict['american-airlines'])
    delta_df = pd.DataFrame(airline_dict['delta-air-lines'])
    united_df = pd.DataFrame(airline_dict['united-airlines'])

    ana_df = pd.DataFrame(airline_dict['ana-all-nippon-airways'])
    japan_df = pd.DataFrame(airline_dict['japan-airlines'])

    qatar_df = pd.DataFrame(airline_dict['qatar-airways'])

    engine = create_engine('postgresql://manuelcollazo:manuelcollazo@localhost:5432/airlines')

    southwest_df.to_sql('southwest',con = engine)
    american_df.to_sql('american',con = engine)
    delta_df.to_sql('delta',con = engine)
    united_df.to_sql('united',con = engine)

    ana_df.to_sql('ana',con = engine)
    japan_df.to_sql('japan',con = engine)

    qatar_df.to_sql('qatar',con = engine)

        

