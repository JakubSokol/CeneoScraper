from requests import get, codes
from bs4 import BeautifulSoup 
import json

def get_element(ancestor, selector = None, attribute = None, return_list = False):
    try:
        if return_list:
            return [tag.text.strip() for tag in opinion.select(selector)]
        if not selector and attribute:
            return ancestor[attribute].strip()
        if attribute:
            return ancestor.select_one(selector)[attribute].strip()
        return ancestor.select_one(selector).text.strip()
    except (AttributeError, TypeError): #taple
        return None

selectors = {
    "id" : [None,"data-entry-id"],
    "author" : ["span.user-post__author-name"],
    "recommendation" : ["span.user-post__author-recommendation>em"],
    "stars" : ["span.user-post__score-count"],
    "content" : ["div.user-post__text"],
    "pros" : ["div.review-feature__title--positives~div.review-feature__item",None,True],
    "cons" : ["div.review-feature__title--negatives~div.review-feature__item",None,True],
    "upvote" : ["button.vote-yes","data-total-vote"],
    "downvote" : ["button.vote-no","data-total-vote"],
    "posted" : ["span.user-post__published>time:nth-child(1)","datetime"],
    "purchased" : ["span.user-post__published>time:nth-child(2)","datetime"],
}
#product_code = input("Please enter product code: ")
product_code="36991221"
#product_code="150607722"
#print(product_code)
url=f"https://www.ceneo.pl/{product_code}#tab=reviews"
all_opinions=[]

while url:
    print(url)
    response = get(url)
    if response.status_code == codes["ok"]:
        soup = BeautifulSoup(response.text, "html.parser")
    try:
        opinions_count = int(soup.select_one("a.product-review__link > span").text.strip()) #soup=pagedom
    except AttributeError:
        opinions_count = 0
    if opinions_count > 0:
        opinions = soup.select("div.js_product-review")
        for opinion in opinions:
            id=get_element(opinion, None, "data-entry-id")
            author=get_element(opinion,"span.user-post__author-name")
            recommendation=opinion.select_one("span.user-post__author-recommendation>em")
            stars=get_element(opinion,"span.user-post__score-count")
            content=get_element(opinion,"div.user-post__text")
            pros=get_element(opinion,"div.review-feature__title--positives~div.review-feature__item",None,True)
            cons= get_element(opinion,"div.review-feature__title--negatives~div.review-feature__item",None,True)
            upvote=get_element(opinion,"button.vote-yes","data-total-vote")       #"button.vote-yes>span"
            downvote=get_element(opinion,"button.vote-no","data-total-vote")       #"button.vote-no>span"
            posted=get_element(opinion,"span.user-post__published>time:nth-child(1)","datetime")
            purchased=get_element(opinion,"span.user-post__published>time:nth-child(2)","datetime")


            single_opinion= {}
            for key,value in selectors.items():
                single_opinion[key] = get_element(opinion, *value)
            all_opinions.append(single_opinion)
    try:
        url=("https://www.ceneo.pl"+ get_element(soup,"a.pagination__next","href"))
    except TypeError:
        url=None
        

with open(f"./opinions/{product_code}.json","w",encoding="UTF-8") as file:
    json.dump(all_opinions,file,indent=4, ensure_ascii=False)