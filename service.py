from product import vin, selectors
from bs4 import BeautifulSoup
import requests
import pandas as pd
from typing import Union
from urllib.parse import urlparse, urlunparse
import csv
import re
from product import data

def getProductsUrls():
    selector = selectors()
    page = 1
    product_number = 1
    product_links = []
    
    #while product_number > 0:
    url = "https://www.vinatis.com/achat-vin-rouge#page_number=7&product_per_page=15&orderby=7&instantSearch=1&select_wishlist=0&display_style=list"
    #response = requests.get("https://www.vinatis.com/achat-vin-rouge#p"+str(2)+"&n15&t7&f[]3[]33:f[]27[]11425")
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, features="lxml")
        product_list = soup.select(selector.product_list)[0].find_all('h2', "product-title")
        product_number = len(product_list)
        result_page = getUrlsFromAList(product_list)
        product_links.append(result_page)
        page += 1
    return product_links

def getUrlsFromAList(product_list):
    links = []
    for product_div in product_list:
        product_link = product_div.find('a')['href']
        links.append(product_link)
    return links

def get_urls_from_link_div_list(link_div_list):
    links = []
    for link_div in link_div_list:
        try:
            link = link_div['href']
            links.append(link)
        except:
            try:
                link = link_div['src']
            except:
                continue
    return links

def getAllWineData(wine_url):
    response = requests.get(wine_url)
    if not response.ok:
        print(f'Code: {response.status_code}, url: {wine_url}')
    else:
        new_collected = vin(response)
        return new_collected

def save_links_in_excel_file(links):
    with open('vinatis_wines_links.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for link in links:
            writer.writerow([link])
    csvfile.close()

def get_html(url):
    response = requests.get(url)
    if not response.ok:
        print(f'Code: {response.status_code}, url: {url}')
    return response

def build_product_page_url_by_page(path, page_product: int)->str:
    params = f"page_number={page_product}&product_per_page=15&orderby=7&instantSearch=1&select_wishlist=0&display_style=grid"
    url = f"https://www.vinatis.com{path}?{params}"
    return url

def insert_new_wine_links_in_csv(links):
    links_df = pd.read_csv('vinatis_wines_links.csv', header=0)

def set_product_links_in_csv(paths: list, page_limit: int):
    """
    Set product wine links browsing product pages
    """
    #f = open("vinatis_wines_links.csv", "a")
    all_web_links = []
    csv_links_df = pd.read_csv('vinatis_wines_links.csv', header=0)

    for path in paths:
        product_number = 1

        print(f"Passing to page listing from {path}.")
        page = 1

        while product_number > 0:
            print(f'From {path} -> Scrapping and registering product links from page {page}')
            url = build_product_page_url_by_page(path, page)
            print(url)
            response = get_html(url)
            if response.ok:    
                soup = BeautifulSoup(response.text, features="lxml")
                result = soup.find_all('a', href=re.compile(r"https://www.vinatis.com/\d\d\d\d\d"))
                page_links = get_urls_from_link_div_list(result)
                product_number = len(page_links)
                if len(page_links) > 0:
                    all_web_links += page_links
            else:
                continue
            page += 1
    
    all_web_links_df = pd.DataFrame(all_web_links, columns=['links'])
    all_links_df = pd.concat([csv_links_df, all_web_links_df])

    all_links_df.drop_duplicates(keep='first', inplace=True)
    product_added = int(all_links_df.shape[0]) - int(csv_links_df.shape[0])
    #print(all_links_df.head(), all_links_df.shape, type(all_links_df))
    all_links_df.to_csv('vinatis_wines_links.csv', index=False)
    
    print(f'End of writing in the csv. {product_added} product(s) added !')
    return

def save_new_wines_to_csv(
    limit: int=0, 
    display_product_fields: bool=False, 
    fields_to_display: Union[bool, list]=False,
    display_errors: bool=False,
    )-> bool:
    """ Browses all links in the links.csv file and stores each one in products.csv
    1. Verify is the wine is already in the csv
    2. Creates a new wine
    3. Store it to the product.csv file

    Parameters
    ----------
    limit: int, optional
        If the limit is setted the function stops to the specified number of products
    display_product_fields: bool, optional
        Default is False. If True will display specified fields of the wine when created
    fields_to_display: dict, optional
        The list of fields that needed to be displayed
    
    Returns
    ----------
    Returns True when completed
    """
    #columns_names is here to check manually the column names that have to have the products.csv
    columns_names = [
        'ref', 'name', 'titles', 'alcool',
        'color', 'vintage', 'country',
        'region', 'state', 'capacity', 
        'designation_of_origin', 'grape_variety', 'tastes',
        'by_tastes', 'smell', 'mouthfeel', 'service_temperature',
        'service', 'conservation', 'to_drink_until',
        'to_drink_as_from', 'food_and_wine_matches', 'prices',
        'teaser', 'resume', 'image', 'rewards'
        ]
    #errors -> erros happening during scrapping will be stored in this variable
    errors = []

    with open("vinatis_wines_links.csv", newline='') as link_files:
        loop = 0
        links_reader = csv.reader(link_files)

        #1. Create a Panda DataFrame with all wines stored in the CSV then compare if columns_names is similar to the df column names
        csv_product_df = pd.read_csv('./products/products.csv', header=0)
        final_product_df = csv_product_df
        if list(csv_product_df.columns) != columns_names:
            raise ValueError("Columns in the csv doesn't match the columns_names in this function.")
    
        #2. Browses all links in the product_links csv
        for row in links_reader:
            link = row[0]

            #Optional -> if limit is setted, will stop browsing links at the limit
            if limit > 0:
                if loop == limit: break
                loop +=1

            #Check if this wine is already in the csv -> if it is pass to the next link in the loop
            if getRefInURL(link) in csv_product_df.ref.unique(): continue

            #3. Create a wine object
            try:
                new_wine = getAllWineData(link)
            except Exception as err:
                try:
                    errors.append(f'Error {err} occured after {new_wine.name}')
                    #Optional: If display error is True
                    if display_errors: print(f'Error after {new_wine.name}')
                except UnboundLocalError:
                    continue
            
            #.Verify if new_wine has been correctly created
            if isinstance(new_wine, vin): 
                #Optional -> Display fields of the new_wine if setted
                if  display_product_fields != False and fields_to_display != False: print_selected_fields(new_wine, fields_to_display)

                #Create row in pandas format
                product_to_store_df = format_wine_to_df(new_wine, columns_names)
                #Insert this row in the df
                final_product_df = final_product_df.append(product_to_store_df)

        
    # Save the final dataframe in the csv
    final_product_df.to_csv('./products/products.csv', index=False) # save to new csv file
    
    product_added_number = int(final_product_df.shape[0]) - int(csv_product_df.shape[0])
    print(f'End of writing in the csv. {product_added_number} product(s) added in the products csv!')
    print(errors)
    
    return True        
                
def push_wine_to_csv(wine: object) ->None:
    
    to_store_wine = [
        wine.ref, 
        wine.name, 
        wine.titles, 
        wine.alcool, 
        wine.color, 
        wine.vintage,
        wine.country, 
        wine.region,
        wine.state, 
        wine.capacity,
        wine.designation_of_origin,
        wine.grape_variety, 
        wine.tastes, 
        wine.by_tastes, 
        wine.smell, 
        wine.mouthfeel, 
        wine.service_temperature, 
        wine.service, 
        wine.conservation, 
        wine.to_drink_until, 
        wine.to_drink_as_from, 
        wine.food_and_wine_matches,
        wine.prices, 
        wine.teaser, 
        wine.resume, 
        wine.image, 
        wine.rewards,
        ]
    df = pd.read_csv('./products/products.csv', header=0)
    
    product = pd.DataFrame([to_store_wine], columns=columns_names)
    #df1 = df.append(to_store_wine, verify_integrity=True)
    df.to_csv('./products/products.csv', index=False) # save to new csv file

def format_wine_to_df(wine: object, columns: list)-> object:
    """
    Creates a df containing all attributes of a wine object
    
    Parameters
    ----------
    wine (object class: wine):
        Wine object that needs to be stored in a pandas df
    columns (list):
        List containing all columns of the csv
    
    Return
    ------
    formated_wine: object->DataFrame
        
    """
    to_store_wine = [
        wine.ref, 
        wine.name, 
        wine.titles, 
        wine.alcool, 
        wine.color, 
        wine.vintage,
        wine.country, 
        wine.region,
        wine.state, 
        wine.capacity,
        wine.designation_of_origin,
        wine.grape_variety, 
        wine.tastes, 
        wine.by_tastes, 
        wine.smell, 
        wine.mouthfeel, 
        wine.service_temperature, 
        wine.service, 
        wine.conservation, 
        wine.to_drink_until, 
        wine.to_drink_as_from, 
        wine.food_and_wine_matches,
        wine.prices, 
        wine.teaser, 
        wine.resume, 
        wine.image, 
        wine.rewards,
    ]
    formated_wine = pd.DataFrame([to_store_wine], columns=columns)
    return formated_wine

def print_selected_fields(new_wine, fields_to_display: dict) ->None:
    """Prints selected fields of a wine object"""
    if len(new_wine.titles) == 0:
        return
    
    if len(fields_to_display) == 0:
        print('No field to display. Select fields in the configuration.')
    elif isinstance(fields_to_display, (list)) == False:
        print('')

    for field in fields_to_display:
        if fields_to_display[field]:
            print(f'{field}: {new_wine.__getattribute__(field)}')
    print('\n')
    return

def getRefInURL(url: str) ->Union[bool, str]:
    """
    Returns the product ref contained in the url
    1. Parse the url
    2. Get the ref 
    3. Verify if the ref contains just digits
    Parameters
    ----------
    url:
        the url in str format
    
    Returns
    ----------
    Product_reference:
        str containing the ref of the product
    
    False: 
        If not found.

    """
    parsed = urlparse(url, scheme='', allow_fragments=True)
    ref = parsed.path[1:6]
    if ref.isdigit() == True:
        return ref
    else:
        try:
            ref = re.compile(r"\d\d\d\d\d").search(url).group(0)
            return ref
        except:
            return False
    return False
    