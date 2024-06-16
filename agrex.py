from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
from threading import Thread, current_thread
import logging
 
# Create and configure logger
logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger("mylogger")

ua = UserAgent()

#Initialize Engine
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float
engine = create_engine('sqlite:///product.db', echo = True)
meta = MetaData()

product_table = Table(
   'product_table', meta, 
    Column('id', Integer, primary_key = True), 
    Column('name', String), 
    Column('url', String), 
    Column('price', Integer), 
    Column('rating', Float), 
    Column('review_count', Integer)
)

product_table.create(engine)


# Code to scrape the data from Amazon
def extract (soup: BeautifulSoup):
    products = []
    items = soup.find_all("div", {"data-index": True}, class_="s-result-item")
    for item in items:
        name = item.find(
            "h2")
        if name is not None:
            name = name.text
        else:
            continue

        url = item.find("a", href=True)
        if url is not None:
            url = "https://www.amazon.in" + url["href"]
        else:
            url = ""

        price = item.find("span", class_="a-offscreen")
        if price is not None:
            price = int(''.join([p for p in price.text if p.isdigit()]))
        else:
            price = 0

        rating = item.find("span", class_="a-icon-alt")
        if rating is not None:
            rating = float(rating.text[:3])
        else:
            rating = 0.0

        review_count = item.find("span", class_="a-size-base s-underline-text")
        if review_count is not None:
            review_count = int(review_count.text.replace(",", ""))
        else:
            review_count = 0

        products.append({
            "name": name,
            "url" : url,
            "price" :  price,
            "rating": rating,
            "review_count": review_count
        })
    return products

def url_scraper(url):
    retry_count=0
    while(retry_count<10):
        headers={"User-Agent": ua.random,
            "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            "Accept-Language": 'en'
        }
        prod = requests.get(url, headers=headers, timeout=5)
        logging.info(f"On thread {current_thread()}")
        if prod.status_code==200:
            soup=BeautifulSoup(prod.content, 'html.parser')
            products = extract(soup)
            conn = engine.connect()
            result = conn.execute(product_table.insert(), products)
            print(result)

            break
        retry_count+=1


if __name__=='__main__':
    pages_urls = [
        "https://www.amazon.in/s?k=tv&page=1",
        "https://www.amazon.in/s?k=tv&page=2",
        "https://www.amazon.in/s?k=tv&page=3",

    ]
    threads = []
    for page in pages_urls:
        threads.append(Thread(target=url_scraper, args=(page,)))
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
    print("executed successfully")
