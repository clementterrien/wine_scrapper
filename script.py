import requests
from bs4 import BeautifulSoup
from service import set_product_links_in_csv, getAllWineData, save_new_wines_to_csv
import pandas as pd
import csv

def main():
    ######### TO CONFIGURE ##########
    ######### Links To Scrap ##########
    scrap_new_data = False
    # paths -> All paths where links can be browsed 
    paths = ["/achat-vins-champagnes-spiritueux-promotion"]
    # page_limit -> limit the page number that be browsed in each paths
    page_limit = 2
    #################################
    
    ########### TEST ENV ############
    product_limit = 5000
    display_product_fields = True #Set if to true for print specified fields of created wines
    fields_to_display = {
        'name': True,
        'ref': False,
        'vintage': False,
        'alcool': False,
        'color': True,
        'country': True,
        'region': True,
        'titles': True,
        'designation_of_origin': True,
        'tastes': False,
        'by_tastes': False,
        'service_temperature': False,
        'service': False,
        'conservation': False,
        'to_drink_until': False,
        'to_drink_as_from': False,
        'smell': False,
        'mouthfeel': False,
        'grape_variety': False,
        'teaser': False,
        'resume': False,
        'prices': False,
        'image': False,
        'food_and_wine_matches': False,
        'rewards': False,
        'error_number': False,
        'errors': True,
        'scrap_alert_number': False,
        'scrap_alerts': False,
        'optional_info_alert_number': False,
        'optional_info_alerts': False
    }

    if scrap_new_data == True: set_product_links_in_csv(paths, page_limit)
    if product_limit > 0: 
        save_new_wines_to_csv(
            limit=product_limit, 
            display_product_fields=display_product_fields, 
            fields_to_display=fields_to_display,
            ) 
    else: save_new_wines_to_csv()

if __name__ == "__main__":
    # execute only if run as a script
    main()

    #TODO
    # Main function -> call save_new_wines without if
    #