#!usr/bin/python
from bs4 import BeautifulSoup
import requests


def scrape12():
    l = []
    for page in range(0, 3):
        page = page + 1
        base_url = 'https://economictimes.indiatimes.com/news/economy/agriculture/articlelist/msid-1202099874,contenttype-a.cms'
        # print(base_url)
        

        # Request URL and Beautiful Parser
        r = requests.get(base_url)
        soup = BeautifulSoup(r.text, "html.parser")

        all_product = soup.find_all('div', class_="eachStory")
        # print(len(all_product))
        
        
        for item in all_product:
            d = { }
            
            # image
            product_image = item.find("img", {"class":"lazy"})
            # image = image.text.replace('\n', "").strip()
            product_image1 = product_image['src']
            product_image = product_image['data-original']
            punctuations = '''#'"\,'''
            my_str = input("Enter a string: ")
            no_punct = ""
            for char in my_str:
               if char not in punctuations:
                   no_punct = no_punct + char
            d['product_image'] = no_punct
            
            
            

            product_name = item.find("a")
            
            # image = image.text.replace('\n', "").strip()

            product_name12=item.find("h3").text
            product_desc=item.find("p").text
            product_time=item.find("time").text
            product_link = 'https://economictimes.indiatimes.com' + product_name['href']
            
            d['product_link'] = product_link
            d["product_name12"]=product_name12
            d["product_desc"]=product_desc
            d["product_time"]=product_time

          

            # name & link
            # product_name = item.find("a", {"itemprop":"name"})
            # product_name1=item.find("href")
            # product_link = '' + str(product_name.get('href'))
            # product_name = product_name.text.replace('\n', "").strip()
            # d['product_link'] = product_link
            # d['product_name'] = product_name

            # # price
            # product_price = item.find("span", {"class":"amount"})
            # print("1",product_price)
            # product_price = product_price.text.replace('\n', "").strip()
            # print("2",product_price)
            # d['product_price'] = 'Rp' + product_price

            # #UPDATE PRICE
            # # price
            # product_price = item.find("span", {"class":"product-price__reduced"})
            # print("1",product_price)
            # product_price = product_price.text.replace('\n', "").strip()
            # print("12",product_price)
            # d['product_price1'] = 'Rp' + product_price

            # # review
            # product_review = item.find("a", {"class":"review__aggregate"})
            # try:
            #     product_review = product_review.text
            #     d['product_review'] = int(product_review)
            # except:
            #     d['product_review'] = 0

            # link
            # product_link = item.find("a", {"class":"product-media__link"}, href=True)
            # product_link = 'https://www.bukalapak.com' + str(product_link.get('href'))
            # d['product_link'] = product_link

            l.append(d)
    print(l)
    return l


if __name__ == "__main__":
    print(scrape12())