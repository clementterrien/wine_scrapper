import re
from product import data, vin
from service import getRefInURL
from scrapper import scrapper
import requests

def main():
    url = "https://www.vinatis.com/42591-la-cote-2019-chateau-de-la-negly"
    scrap = scrapper(url)
    wine = vin(scrap.response)
    wine.set_name(scrap.scrapName())
    print(wine.name)
    #eturn re.compile(fr".*?{feature}.*?", bonjour)


    return True
    # #x = list(filter(lambda v: re.match(r'.+% vol', v), test))
    # #x = list(filter(lambda v: test in test_list, test))
    # #x = any(item in test_list for item in test)
    # #region = [e for e in test if e in test_list]
    #print(test)

print(main())