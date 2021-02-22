from product import selectors
from bs4 import BeautifulSoup 
import requests

class scrapper:

    def __init__(self, url):
        self.selectors = selectors()
        self.set_response(self.make_a_request(url))
        self.soup = self.create_soup(self.response)
        self.scrap_alerts = {}
        self.scrap_errors = {}
        
    def get_response(self):
        return self.response

    def set_response(self, response):
        self.response = response
        return

    def make_a_request(self, url):
        response = requests.get(url)
        if not response.ok:
            print(f'Code: {response.status_code}, url: {url}')
        else:
            return response
    
    def create_soup(self, response):
        soup = BeautifulSoup(response.text, features="lxml")
        return soup

    def scrapName(self):
        selector = self.selectors
        soup = self.soup
        try:
            name = self.soup.select(selector.name)[0].text
        except IndexError:
            try:
                self.set_scrap_alert('name:', 'name_2.')
                name = soup.select(selector.name_2)[0].text
            except IndexError:
                self.set_error('name not found.')
                self.name = False    
        return name.strip() 

    def set_scrap_alert(self, alert, alert2):
        return True

    def set_error(self, error):
        return True 