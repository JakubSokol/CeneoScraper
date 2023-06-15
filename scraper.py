from requests import get, codes
from bs4 import BeautifulSoup
import json
import os
import re
from translate import Translator


def get_element(ancestor, selector=None, attribute=None, return_list=False):
    try:
        if return_list:
            return ",".join([tag.text.strip() for tag in opinion.select(selector)])
        if not selector and attribute:
            return ancestor[attribute].strip()
        if attribute:
            return ancestor.select_one(selector)[attribute].strip()
        return ancestor.select_one(selector).text.strip()
    except (AttributeError, TypeError):  # taple
        return None


selectors = {
    "id": [None, "data-entry-id"],
    "author": ["span.user-post__author-name"],
    "recomendation": ["span.user-post__author-recomendation>em"],
    "stars": ["span.user-post__score-count"],
    "content": ["div.user-post__text"],
    "pros": [
        "div.review-feature__title--positives~div.review-feature__item",
        None,
        True,
    ],
    "cons": [
        "div.review-feature__title--negatives~div.review-feature__item",
        None,
        True,
    ],
    "upvote": ["button.vote-yes", "data-total-vote"],
    "downvote": ["button.vote-no", "data-total-vote"],
    "posted": ["span.user-post__published>time:nth-child(1)", "datetime"],
    "purchased": ["span.user-post__published>time:nth-child(2)", "datetime"],
}
lang_from = "pl"
lang_to = "en"
translator = Translator(lang_to, lang_from)
# product_code = input("Please enter product code: ")
# product_code = "36991221"
# product_code="150607722"
product_code = "150607717"
url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
all_opinions = []

while url:
    print(url)
    response = get(url)
    if response.status_code == codes["ok"]:
        soup = BeautifulSoup(response.text, "html.parser")
        opinions = soup.select("div.js_product-review")
    for opinion in opinions:
        single_opinion = {}
        for key, value in selectors.items():
            single_opinion[key] = get_element(opinion, *value)
        single_opinion["id"] = int(single_opinion["id"])
        single_opinion["recomendation"] = (
            True
            if single_opinion["recomendation"] == "Polecam"
            else False
            if single_opinion["recomendation"] == "Nie polecam"
            else None
        )
        single_opinion["stars"] = float(
            single_opinion["stars"].split("/")[0].replace(",", ".")
        )
        single_opinion["upvote"] = int(single_opinion["upvote"])
        single_opinion["downvote"] = int(single_opinion["downvote"])
        single_opinion["content"] = " ".join(
            re.sub(r"\s+", " ", single_opinion["content"], flags=re.UNICODE).split(" ")
        )
        single_opinion["content_en"] = translator.translate(
            single_opinion["content"][:500]
        )
        single_opinion["pros_en"] = (
            None
            if not translator.translate(single_opinion["pros"])
            else translator.translate(single_opinion["pros"])
        )
        single_opinion["cons_en"] = (
            None
            if not translator.translate(single_opinion["cons"])
            else translator.translate(single_opinion["cons"])
        )

        all_opinions.append(single_opinion)
    try:
        url = "https://www.ceneo.pl" + get_element(soup, "a.pagination__next", "href")
    except TypeError:
        url = None
if not os.path.exists("./opinions"):
    os.mkdir("./opinions")

with open(f"./opinions/{product_code}.json", "w", encoding="UTF-8") as file:
    json.dump(all_opinions, file, indent=4, ensure_ascii=False)
