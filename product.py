from bs4 import BeautifulSoup 
import requests
import re
from typing import Union
import shutil
import os.path
from os import path

#The wine class has to be instanced from an Response object (the page of the product)
class vin:
    """Wine object to be scraped

    The wine class has to be instanced from an Response object (the page of the product).
    The _init_ has been configured to scrap all information automaticaly.
    
    1.1 - Attributes (Product)
    --------------------------
    All Attributes are setted to a default value within the set_attributes_to_default
    function. If the attribute has not been found, it will be setted to False.

    name: str 
        The name of the wine/product
    ref: str
        The reference of the product (contained in the url)
    titles: list
        List containing infos as type / color / designation / alcool
        not scrapable in other place

    1.2 - Attributes (Alerts & Infos)
    --------------------------
    """

   
   
    #MANDATORY INFOS 
    # -> If missing will generate errors that will be stored
    # -> If need to use second selector // it will generate scrap report
    
    def __init__(self, response):
        self.soup = BeautifulSoup(response.text, features="lxml")
        self.set_attributes_to_default()
        self.set_product_ref(response)      
        
        #Mandatory parameters Set
        self.set_name() 
        self.set_titles() 
        self.set_alcool() 
        self.set_color() 
        self.set_vintage() 

        #Is it a french wine or not 
        if self.is_it_a_french_wine():
           self.set_country(french=True)
           self.set_region(french=True)
           self.set_state(french=True)
        else:
           self.set_country()
           self.set_region()
           self.set_state()
        
        self.set_capacity() 
        self.set_designation_of_origin() 
        self.set_grape_variety() 
        
        self.set_tastes()
        self.set_by_tastes()
        self.set_smell()
        self.set_mouthfeel()
        self.set_service_temperature()
        self.set_service()
        self.set_conservation()
        self.set_to_drink_until()
        self.set_to_drink_as_from()
        self.set_food_and_wine_matches()
        
        self.set_prices()
        self.set_teaser()
        self.set_resume()

        self.set_image()
        self.set_rewards()
                                                                                                                         
    ##### SETTERS #####
    def set_attributes_to_default(self) -> None:
        """
        Set all object attributes to its default value
        """
        self.data = data()
        self.selectors = selectors()

        self.name = "" 
        self.color = ""
        self.region = ""
        self.titles = []
        self.ref = 0
        self.grape_variety = ""
        self.error_number = 0
        self.state = ''
        self.errors = []
        self.scrap_alert_number = 0
        self.scrap_alerts = {}
        self.optional_info_alert_number = 0
        self.optional_info_alerts = []
        self.rewards = {}
        return

    def get_name(self):
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
    def set_name(self):
        name = self.get_name()
        if name == False or name == "":
            self.name = False
        else:
            self.name = name
        return
    
    def get_product_ref(self, response):
        link = response.url
        try:
            ref = re.compile(r"/\d\d\d\d\d-").search(link).group(0).replace('/', '').replace('-', '')
            return ref
        except IndexError:
            self.set_error('No ref found in the link.')
        except AttributeError:
            self.set_error('No ref found in the link.')

        return False
    def set_product_ref(self, response):
        ref = self.get_product_ref(response)
        self.ref = ref
        return
    
    def get_titles(self):
        selector = self.selectors
        soup = self.soup
        titles = self.titles
        try:
            titles = soup.select(selector.titles)[0].text
        except IndexError:
            try:
                self.set_scrap_alert('titles', 'titles_2')
                titles = soup.select(selector.titles_2)[0].text
            except IndexError:
                try:
                    self.set_scrap_alert('titles', 'titles_3')
                    titles = soup.select(selector.titles_3)[0].text
                except IndexError:
                        self.set_scrap_alert('titles', 'title_section')
                        titles = self.find_titles_by_section()
                        if titles == False:
                            return False
        finally:   
            if titles != False and isinstance(titles, str):
                return titles.split(' / ')
            else:
                return False
    def set_titles(self):
        titles = self.get_titles()
        if titles == False or titles == []:
            self.titles = False     
        else:
            self.titles = titles
        return
    
    def get_capacity(self):
        selector = self.selectors
        soup = self.soup
        capacity = ""
        try:
            capacity = soup.select(selectors.capacity)[0].text
        except IndexError:
            try:
                self.set_scrap_alert('capacity', 'capacity_2')
                capacity = soup.select(selector.capacity_2)[0].text
            except IndexError:
                try:
                    self.set_scrap_alert('capacity', 'capacity_3')
                    capacity = soup.select(selector.capacity_3)[0].text
                except IndexError:
                            self.set_scrap_alert('capacity', 'capacity_section')
                            capacity = self.find_capacity_by_section()

        if capacity == False or capacity == "": return False        
        else: return capacity
    def set_capacity(self):
        capacity = self.get_capacity()
        if capacity == False or capacity == "":
            self.capacity = False
        else:
            self.capacity = capacity.strip()
        return
    
    def get_country(self):
        if self.titles == False or self.titles == []:
            self.set_error('country: titles not found.')
            return False
        else:
            country = self.is_there_an_element_in_another_list(self.titles, self.data.country, _bool=False)
            if country != False:
                return country.strip()
            else:
                return False
    def set_country(self, french:bool=False):
        if french:
            self.country = 'France'
        else:
            self.country = self.get_country().strip()
            self.titles.remove(self.country)
        return
    
    def get_state(self):
        if self.titles == False or self.titles == []:
            self.set_error('state: titles not found.')
            return False
        else:
            state = self.is_there_an_element_in_another_list(self.titles, self.data.states, _bool=False)
            if state != False:
                return state.strip()
            else:
                return False
    def set_state(self, french: bool =False):
        if french:
            self.state = False
            return
        else:
            state = self.get_state()
            self.state = state
            if state != False:
                self.titles.remove(state)
            return
    
    def get_region(self, french=False):
        region = self.region
        if self.titles == False:
            self.set_error('region: titles not found.')
            return False
        else:
            regions_list = self.data.fr_regions if french else self.data.foreign_regions 
            region = [e for e in self.titles if e in regions_list]
            if len(region) == 1:
                return region[0]
            else:
                self.set_error('region: match error in titles')
                return False
    def set_region(self, french=False):
        region = self.get_region(french)
        if region == [] or region == False:
            self.region = False
        else:
            self.region = region.strip()
            try:
                self.titles.remove(region)
            except ValueError:
                return
            except AttributeError:
                return
        return
    
    def get_designation_of_origin(self):
        designation_list = data().designation_of_origin
        __designation = ""
        if self.titles == False:
            self.set_error('designation: titles not found.')
            return False
        else:
            for item in self.titles:
                if item in designation_list:
                    __designation = item
                else:
                    if self.is_it_a_designation(item):
                        __designation = item
            
            if __designation == "" or __designation == False:
                self.set_optional_info_alert('No designation found.')
                return False
            else:
                return __designation
    def set_designation_of_origin(self):
        designation = self.get_designation_of_origin()
        if designation == "" or designation == False:
            self.designation_of_origin = False
        else:
            self.designation_of_origin = designation.strip()
            self.titles.remove(designation)
        return
    
    def get_color(self):
        #Color is contained in titles // if titles have not been defined previously -> return False
        color = self.color
        if self.titles == [] or self.titles == False:
            self.set_error('color: titles not found.')
            return False
        else:
            try:
                color = self.titles[0]
            except IndexError:
                self.set_scrap_alert('color', 'body')
                color = self.find_color_by_section()
                
        if color not in self.data.color:
            self.set_error(f'Unvalid Color -> {color}')
            return False
        else:
            return color
    def set_color(self):
        color = self.get_color()
        if color == False:
            self.color = False
        else:
            self.color = color.strip()
            self.titles.remove(color)
        return
    
    def get_alcool(self):
        if self.titles == [] or self.titles == False:
            self.set_error('alcool: titles not found.')
            return False
        else:
            alcool = list(filter(lambda v: re.match(r'.+% vol', v), self.titles))
            if len(alcool) == 1:
                return alcool[0]
            else:
                self.set_error('No alcool match in titles.')
                return False
    def set_alcool(self):
        alcool = self.get_alcool()
        if alcool == False:
            self.alcool = False
        else:
            self.alcool = alcool.strip()
            self.titles.remove(alcool)
        return
    
    def get_grape_variety(self):
        grape_variety = self.grape_variety
        if self.titles == False:
            self.set_error('grape_variety: titles not found.')
            return False
        else:
            #test if there in a match with the regex in the titles
            grape_match = list(filter(lambda v: re.match(r'100%.+', v), self.titles)) 
            if len(grape_match) == 1:
                self.titles.remove(grape_match[0])
                return grape_match[0]
            else:
                grape_variety = self.find_grape_variety_by_section()
                if grape_variety == "":     
                    self.set_error('grape_variety not found.')
                    return False
                else: 
                    return grape_variety           
    def set_grape_variety(self):
        grape_variety = self.get_grape_variety()
        if grape_variety == False or grape_variety == "":
            self.grape_variety = False
        else:
            self.grape_variety = grape_variety.strip()
        return
    
    def get_vintage(self):
        vintage = self.find_vintage_by_section()
        if vintage == False or vintage == "":
            vintage = self.find_vintage_in_name()
        if vintage == False:
            return False
        else:
            return vintage
    def set_vintage(self):
        vintage = self.get_vintage()
        if vintage == False or vintage == "":
            self.vintage = False
        else:
            self.vintage = vintage.strip()
        return    
    
    def get_tastes(self):
        tastes = self.find_feature_by_brother('taste',feature='Goûts')
        return tastes
    def set_tastes(self):
        tastes = self.get_tastes()
        self.tastes = False if tastes == False else tastes.strip()
        return
    
    def get_by_tastes(self):
        by_tastes = self.find_feature_by_brother('by_tastes', feature='Par Goûts')
        return by_tastes
    def set_by_tastes(self):
        by_tastes = self.get_by_tastes()
        self.by_tastes = False if by_tastes == False else by_tastes.strip()
        return

    def get_smell(self):
        smell = self.find_feature_by_brother('smell', feature='Au nez')
        return smell
    def set_smell(self):
        smell = self.get_smell()
        self.smell = False if smell == False else smell.strip()
        return
    
    def get_mouthfeel(self):
        mouthfeel = self.find_feature_by_brother('mouthfeel', feature='En bouche')
        return mouthfeel
    def set_mouthfeel(self):
        mouthfeel = self.get_mouthfeel()
        self.mouthfeel = False if mouthfeel == False else mouthfeel.strip()
        return
    
    def get_service_temperature(self):
        service_temperature = self.find_feature_by_brother('service_temperature', feature='Température de service')
        return service_temperature
    def set_service_temperature(self):
        service_temperature = self.get_service_temperature()
        self.service_temperature = False if service_temperature == False else service_temperature.strip()
        return
    
    def get_service(self):
        service = self.find_feature_by_brother('service', feature='Service')
        return service
    def set_service(self):
        service = self.get_service()
        self.service = False if service == False else service.strip()
        return

    def get_conservation(self):
        conservation = self.find_feature_by_brother('conservation', feature='Conservation')
        return conservation
    def set_conservation(self):
        conservation = self.get_conservation()
        self.conservation = False if conservation == False else conservation.strip()
        return    

    def get_to_drink_until(self):
        to_drink_until = self.find_feature_by_brother('to_drink_until', feature="Jusqu'à")
        return to_drink_until
    def set_to_drink_until(self):
        to_drink_until = self.get_to_drink_until()
        self.to_drink_until = False if to_drink_until == False else to_drink_until.strip()
        return

    def get_to_drink_as_from(self):
        to_drink_as_from = self.find_feature_by_brother('to_drink_from', feature="A boire à partir de")
        return to_drink_as_from
    def set_to_drink_as_from(self):
        to_drink_as_from = self.get_to_drink_as_from()
        self.to_drink_as_from = False if to_drink_as_from == False else to_drink_as_from.strip()
        return  

    def get_teaser(self):
        try:
            teaser = self.soup.select(self.selectors.teaser)[0].text
            return teaser
        except IndexError:
            try:
                self.set_scrap_alert('teaser', 'body')
                teaser = self.soup.select(self.selectors.body)[0].find('strong', class_="accroche").text
                return teaser
            except IndexError:
                return False
        return False
    def set_teaser(self):
        teaser = self.get_teaser()
        self.teaser = False if teaser == False else teaser.strip()
        return

    def get_resume(self):
        try:
            resume = self.soup.select(self.selectors.resume)[0].text
            return resume
        except IndexError:
            self.set_scrap_alert('resume', 'teaser_brother')
            resume = self.get_teaser().next_sibling.text
        
        if len(resume) > 0 and isinstance(resume, str):
            return resume
        else:
            return False
        return False
    def set_resume(self):
        resume = self.get_resume()
        self.resume = False if resume == False else resume.strip()
        return

    def get_prices(self):
        try:
            prices_section = self.soup.select(self.selectors.prices)[0]
            prices = self.find_prices_in_section(prices_section)
            return prices
        except IndexError:
            return False
    def set_prices(self):
        prices = self.get_prices()
        self.prices = prices

    def get_image(self):
        image_soup = self.find_wine_image()
        image_name = self.download_and_save_image(image_soup)
        return image_name
    def set_image(self):
        image = self.get_image()
        self.image = image
    
    def get_rewards(self):
        rewards = self.download_and_save_rewards_images()
        return rewards
    def set_rewards(self):
        rewards = self.get_rewards()
        self.rewards = rewards
        return 
    
    def get_food_and_wine_matches(self):
        try:
            food_and_wine_matches = self.soup.select(self.selectors.food_and_wine_matches)[0]
            return food_and_wine_matches.text
        except IndexError:
            self.set_scrap_alert('food_and_wine_matches', 'section_2')
            food_and_wine_matches = self.find_feature_by_brother('food_and_wine_matches', feature='Accords mets-vin') 
        return food_and_wine_matches
    def set_food_and_wine_matches(self):
        food_and_wine_matches = self.get_food_and_wine_matches()
        self.food_and_wine_matches = food_and_wine_matches.strip() if food_and_wine_matches != False else False
        return
    
    #### VALIDATION / VERIFICATION ####
    ###################################
    def is_it_a_french_wine(self) ->bool:
        #By default the function returns True if there no titles to search in.
        if self.titles == False:
            self.set_error('country: titles not found, considering this as a french')
            return True
        
        if self.is_there_an_element_in_another_list(self.titles, self.data.country) == True:
            return False
        else:
            return True
    def is_it_a_designation(self, item: str) ->bool:
        designation_abbr = data().designation_abbr
        splitted_string = item.split(' ')

        for word in splitted_string:
            if word in designation_abbr:
                return True
        return False
    def is_there_an_element_in_another_list(self,find_match_list: list, known_fields: list, _bool=True) -> Union[str,bool]:
        #This function compares a list and known records to find a match 
        #e.g in titles = ['United-States', 'California', 'North-California'] known_fields = data.country
        # _bool: If setted to False the function will return the matching item (return 'United-States')
        #        Default: Will return True or False
        # If not match is found this function returns False
        for item in find_match_list:
            if item in known_fields:
                if _bool == True:
                    return True
                else:
                    return item
            else: 
                return False
    ######### END VALIDATION ##########

    ######### SECTION FINDERS #########
    ###################################
    # Each function returns False if the data is not found
    # ATTRIBUTE FINDER
    def find_capacity_by_section(self):
        selector = self.selectors
        soup = self.soup
        section = ""
        capacity = ""
        try:
            section = soup.select(selector.capacity_section)[0]
            if section != "":
                #Capacity 
                try:
                    capacity = section.find_all(string=re.compile(r"\d?,?\d+\s?L"))[0]
                    if capacity != "": return capacity
                except IndexError:
                    self.set_scrap_alert('capacity', 'no match in section: passing section_2.')
        
        except IndexError:
            self.set_scrap_alert('capacity', 'section not found: passing section_2.')
            try: 
                section = soup.select(selector.capacity_section_2)[0]
                if section != "":
                    #Capacity 
                    try:
                        capacity = section.find_all(string=re.compile(r"\d?,?\d+\s?L"))[0]
                        if capacity != "": return capacity
                    except IndexError:
                        self.set_scrap_alert('capacity', 'no match in section_2: passing body.')
        
            except IndexError:
                self.set_scrap_alert('capacity','body')
                try:
                    section = soup.select(selector.body)[0]
                    if section != "":
                        try:
                            capacity = section.find_all(string=re.compile(r"\d?,?\d+\s?L"))[0]
                            if capacity != "": return capacity
                        except IndexError:
                            return False
                except IndexError:
                    return False

        if capacity != "": return capacity
        else: return False
    def find_titles_by_section(self):
        selector = self.selectors
        soup = self.soup
        titles = self.titles
        
        # Try to find a section
        try:
            section = soup.select(selector.titles_section)[0]
        except IndexError:
            try:
                self.set_scrap_alert('titles', 'body')
                section = soup.select(selector.body)[0]
            except IndexError:
                self.set_scrap_alert('titles', 'body not found.')
                self.set_error('Body not found.')
                return False

        #If a Section has been found, search for titles in it
        if len(section) >= 1:
            titles = section.find(string=re.compile(r"/ .+% vol")).parent.text
            #If titles have been found 
            if isinstance(titles, str) and len(titles) > 0:
                return titles
            else:
                #Last search method -> find with capacity wich use to be next to titles 
                self.set_scrap_alert('titles', 'capacity_brother')
                titles = self.find_next_brother(self.get_capacity())
                if isinstance(titles, str) and len(titles) > 0:
                    return titles
    def find_grape_variety_by_section(self):
        selector = self.selectors
        soup = self.soup
        section = ""
        grape_variety = self.grape_variety
        try:
            section = soup.select(selector.first_features_section)[0]
        except IndexError:
            self.set_scrap_alert('grape_variety', 'section_2.')
            try:
                section = soup.select(selector.first_features_section_2)[0]
            except IndexError:
                self.set_scrap_alert('grape_variety', 'body')
                try:
                    section = soup.select(selector.body)[0]
                except IndexError:
                    self.set_error('grape_variety: section(body) not found')
                    return False

        if len(section) == 1:
            try:
                grape_variety = section.find_all(string=re.compile(r".+Cépage"))[0].parent.find_next_siblings("div")[0].text
            except IndexError:
                self.set_error('grape_variety: not found with the regex')
                return False
        return grape_variety
    def find_vintage_by_section(self):
        selector = self.selectors
        soup = self.soup
        section = ""
        vintage = ""
        try:
            section = soup.select(selector.first_features_section)[0]
        except IndexError:
            self.set_error('vintage section not found.')
            return False   
        try:
            vintage = section.find_all(string=re.compile(r".+Millésime"))[0].parent.find_next_siblings("div")[0].text
        except IndexError:
            self.set_error('vintage not found with the regex')
            return False
        if bool(re.match(r"\d{4}", vintage)) == True:
            self.set_error('Vintage found but not match pattern (ex: 1990)')
            return False
        return vintage
    def find_vintage_in_name(self):
        if self.name == False:
            return False
        else:
            try:
                vintage = re.findall(r"\d{4}", self.name)[0]
                self.set_scrap_alert('vintage', 'name')
            except IndexError:
                return False
        return vintage
    def find_by_tastes_by_section(self):
        selector = self.selectors
        soup = self.soup
        section = ""
        by_tastes = ""
        try:
            section = soup.select(selector.second_features_section)[0]
        except IndexError:
            self.set_error('by_tastes section not found')
            return False   
        try:
            by_tastes = section.find_all(string=re.compile(r".+Par Goûts"))[0].parent.find_next_siblings("div")[0].text
        except IndexError:
            self.set_error('by_tastes not found with the regex')
            return False
        return by_tastes
    def find_color_by_section(self):
        return False
    def find_wine_image(self):
        try:
            image = self.soup.select(self.selectors.image)[0]
            return image
        except IndexError:
            return image
    def find_rewards_section(self):
        try:
            section = self.soup.select(self.selectors.erreur)[0]
            return section
        except IndexError:
            self.set_scrap_alert('rewards', 'method 2')
            try:
                section = self.soup.find_all(attrs={"class": "recompenses-conteneur-product"})[0]
                return section
            except IndexError:
                return False
        return False

    #SECTION AND SOUP FINDER
    def find_next_brother(self, element: str) -> str:
        #@Find_next_brother Return title section with the capacity
        # On the website -> Capacity is juste before titles
        #@element -> the origin element (Capacity section)
        #Returns -> titles

        section = element.parent.parent.next_sibling.text
        if isinstance(section, str) and re.match(r'.+/.+', section):
            return section
        else:
            return False
    def find_feature_by_brother(self, attr, feature=None, )-> Union[str,bool]:
        # find_feature_by_brother return the feature value.
        # Feature is the "french" name of the searched feature as named in the page
        # attr is the name of the object attribute (for messages)        
        
        if feature == None:
            return False
        else:
            try:
                section = self.soup.select(self.selectors.features_section)[0]
            except IndexError:
                try:
                    self.set_scrap_alert(feature, 'body')
                    section = self.soup.select(self.selectors.body)[0]
                except IndexError:
                    self.set_error(f'{feature}: body not found.')
                    return False
        try:
            feature_value = section.find_all(string=re.compile('.*(%s).*'%feature))[0].parent.find_next_siblings()[0].text
            return feature_value
        except IndexError:
            return False
    def download_and_save_image(self, image) -> str:
        # Download and save the wine image 
        # Returns the image name
        
        #1. Get the image link in the image soup
        try:
            link = image.attrs['src']
            if link == "": return False
        except IndexError:
            return False
        #2 - Create a pattern for the name 
        ref = self.ref if self.ref != False else "00000"
        product_name = self.name if self.name != False else link.replace('https://www.vinatis.com/', '').replace('.png', '')     
        image_name = f'{ref} - {product_name}' 
        
        #3 - Check if this pattern exists in this the image folder 
        if path.exists(f'./wine_images/{image_name}.png'):
            return image_name
        
        #4 - Download the image
        response = requests.get(link, stream=True)

        if response.ok:

            file = open("./wine_images/{}.png".format(image_name), 'wb')
    
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, file)
            del response
        
            return image_name
        else:
            return False 
    def download_and_save_rewards_images(self):
        rewards = {}
        section = self.find_rewards_section()
        if section == False: return False
        
        #1. Search for images in the rewards_section
        rewards_images = section.find_all('img')
        if rewards_images == []:
            return False
        
        for image in rewards_images:    
            #2. Create reward image name and link
            try:
                reward_image_name = f"{image.attrs['alt']}".strip().replace('/', '_')
                reward_image_link = f"{image.attrs['src']}".strip()
            except IndexError:
                return False
            
            #3. Check if image already exists
            if path.exists(f'./wine_awards_images/{reward_image_name}.png'):
                rewards[reward_image_name] = reward_image_link
                continue
             
            #4. Try to download the image
            link = f"https://www.vinatis.com{reward_image_link}"
            response = requests.get(link, stream=True)
            
            if response.ok:                
                file = open("./wine_awards_images/{}.png".format(reward_image_name), 'wb')
               
               #5. Save the file
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, file)
                rewards[reward_image_name] = reward_image_link
            else:
                return False
            
            del response
        return rewards

    
    
    
    def find_prices_in_section(self, prices_section: object) -> Union[dict, bool]:
        prices = {}
        # 1. FIND UNIT PRICE 
        # Find the div containing the unit price and extract the price
        # Sometimes this section can contain multiple prices because of a discount (<del>) -> Try heep the first one (without discount)
        unit_price_text = prices_section.find('div', class_="our_price_display").text
        try:
            unit_price = re.compile(r"\d?\d?\d,\d?\d?\s€").search(unit_price_text).group(0)
            prices['unit'] = float(unit_price.strip(' €').replace(',', '.')) #just formating to a float
        except AttributeError:
            self.set_scrap_alert("prices['unit_price']", 'not found')

        # 2. FIND GROUP_PRICES (ex: multiple group prices :https://www.vinatis.com/36829-aroma-syrah-2016-cellier-des-princes)
        multiple_prices = prices_section.find_all('div', attrs={"class": "quantity-discount"})
        
        for group_price_section in multiple_prices:
            try: #find price with regex ('6,90 €')
                group_price = re.compile(r"\d?\d?\d,\d?\d?\s€").search(group_price_section.text).group(0)
            except AttributeError: 
                continue
            try: #find quantity with regex ('par 6')
                quantity = int(re.compile(r"par\s\d?\d").search(group_price_section.text).group(0).replace('par ', ''))
            except AttributeError: 
                continue
            
            prices[quantity] = float(group_price.strip(' €').replace(',', '.')) #just formating to a float
            
        if prices == {}:
            return False
        else:
            return prices
    #ex: multiple group prices :https://www.vinatis.com/36829-aroma-syrah-2016-cellier-des-princes
    def find_group_prices_in_price_section(self, prices_section: object) ->Union[dict,bool]:
        multiple_prices = prices_section.find_all('div', attrs={"class": "quantity-discount"})
        if multiple_prices != []:
            return
            
    ###### ERRORS & ALERTS  ######
    ##############################
    def set_error(self, error_description):
        self.errors.append(error_description)
        self.error_number +=1
    def set_scrap_alert(self, attribute, used_selector ):
        self.scrap_alerts[attribute] = used_selector
        self.scrap_alert_number +1
    def set_optional_info_alert(self, info_description):
        self.optional_info_alerts.append(info_description)
        self.optional_info_alert_number +=1
    
    
    ######## ERRORS INFOS ########
    ##############################
    # Each getter will set an error when the attributes is mandatory. It will return False if the Data has not been found.
    # Each setter will set False to the corresponding attribute -> each False attribute means that the script tried to set the attribute unsuccessfully
class selectors:
    ##### DIRECT #####
    name = "h1#produit-titre"
    name_2 = "#features > div:nth-child(1) > section > div > div > div > div.table-caption-css.taille-xl.padding-bottom-30.padding-left-10"
    vintage = "#features > div:nth-child(1) > section > div > div > div > div.table-row-css > div:nth-child(1) > div > div:nth-child(1) > div.table-cell-css.vertical-align-top.padding-vertical-5.taille-xs.color-gray-darker.text-bold"
    titles = "#center_column > div:nth-child(6) > div > div.pb-center-column.col-xs-12.color-gray-darker.no-margin-bottom > div > div > div.table-cell-css.largeur-xs-12.largeur-md-10 > div > div:nth-child(3) > div > div > div > div.largeur-xs-12.largeur-md-8.table-cell-css.vertical-align-top.padding-right-20.padding-top-30.no-padding-vertical-xs.no-padding-vertical-sm.no-padding-right-sm.no-padding-right-xs > div > div.col-xs-12.col-sm-8.col-md-8.col-lg-8.no-padding-left.padding-right-30 > div.title > div:nth-child(2) > div > h2 > span.ss-titre.color-gray-darker.taille-xs.line-height-15-xs.no-padding-horizontal"
    titles_2 = "#center_column > div:nth-child(6) > div > div.pb-center-column.col-xs-12.color-gray-darker.no-margin-bottom > div > div > div.table-cell-css.largeur-xs-12.largeur-md-10 > div > div:nth-child(1) > div > div"
    titles_3 = "#center_column > div:nth-child(6) > div > div.pb-center-column.col-xs-12.color-gray-darker.no-margin-bottom > div > div > div > div > div:nth-child(2) > div > div > div > div.largeur-xs-12.largeur-md-8.table-cell-css.vertical-align-top.padding-right-20.padding-top-30.no-padding-vertical-xs.no-padding-vertical-sm.no-padding-right-sm.no-padding-right-xs > div > div.col-xs-12.col-sm-8.col-md-8.col-lg-8.no-padding-left.padding-right-30 > div.title > div:nth-child(2) > div > h2 > span.ss-titre.color-gray-darker.taille-xs.line-height-15-xs.no-padding-horizontal"
    titles_section = "#center_column > div:nth-child(6) > div > div.pb-center-column.col-xs-12.color-gray-darker.no-margin-bottom > div > div > div > div > div:nth-child(3) > div > div > div > div.largeur-xs-12.largeur-md-8.table-cell-css.vertical-align-top.padding-right-20.padding-top-30.no-padding-vertical-xs.no-padding-vertical-sm.no-padding-right-sm.no-padding-right-xs > div > div.col-xs-12.col-sm-8.col-md-8.col-lg-8.no-padding-left.padding-right-30 > div.title"
    grape_variety = "#features > div:nth-child(1) > section > div > div > div > div.table-row-css > div:nth-child(1) > div > div:nth-child(2) > div.table-cell-css.vertical-align-top.padding-vertical-5.taille-xs.color-gray-darker.text-bold"
    grape_variety_2 = "#features > div:nth-child(1) > section > div > div > div > div.table-row-css > div:nth-child(1) > div > div > div.table-cell-css.vertical-align-top.padding-vertical-5.taille-xs.color-gray-darker.text-bold"
    tastes = "#features > div:nth-child(1) > section > div > div > div > div.table-row-css > div:nth-child(2) > div > div:nth-child(1) > div.table-cell-css.vertical-align-top.padding-vertical-5.taille-xs.color-gray-darker.text-bold"
    #par gout
    by_tastes = "#features > div:nth-child(1) > section > div > div > div > div.table-row-css > div:nth-child(2) > div > div:nth-child(2) > div.table-cell-css.vertical-align-top.padding-vertical-5.taille-xs.color-gray-darker.text-bold"
    #a l'oeil
    visual = "#features > div:nth-child(1) > section > div > div > div > div.table-row-css > div:nth-child(2) > div > div:nth-child(3) > div.table-cell-css.vertical-align-top.padding-vertical-5.taille-xs.color-gray-darker.text-bold"
    #au nez
    smell = "#features > div:nth-child(1) > section > div > div > div > div.table-row-css > div:nth-child(2) > div > div:nth-child(4) > div.table-cell-css.vertical-align-top.padding-vertical-5.taille-xs.color-gray-darker.text-bold"
    #en bouche
    mouthfeel = "#features > div:nth-child(1) > section > div > div > div > div.table-row-css > div:nth-child(2) > div > div:nth-child(5) > div.table-cell-css.vertical-align-top.padding-vertical-5.taille-xs.color-gray-darker.text-bold"
    mouthfeel_2 = "#features > div:nth-child(1) > section > div > div > div > div.table-row-css > div:nth-child(2) > div > div:nth-child(4) > div.table-cell-css.vertical-align-top.padding-vertical-5.taille-xs.color-gray-darker.text-bold"
    service_temperature = "#features > div:nth-child(1) > section > div > div > div > div.table-row-css > div:nth-child(3) > div > div:nth-child(1) > div.table-cell-css.vertical-align-top.padding-vertical-5.taille-xs.color-gray-darker.text-bold"
    # service // en bouteille, cubis etc
    service = "#features > div:nth-child(1) > section > div > div > div > div.table-row-css > div:nth-child(3) > div > div:nth-child(2) > div.table-cell-css.vertical-align-top.padding-vertical-5.taille-xs.color-gray-darker.text-bold"
    conservation = "#features > div:nth-child(1) > section > div > div > div > div.table-row-css > div:nth-child(3) > div > div:nth-child(3) > div.table-cell-css.vertical-align-top.padding-vertical-5.taille-xs.color-gray-darker.text-bold"
    to_drink_as_from = "#features > div:nth-child(1) > section > div > div > div > div.table-row-css > div:nth-child(3) > div > div:nth-child(4) > div.table-cell-css.vertical-align-top.padding-vertical-5.taille-xs.color-gray-darker.text-bold"
    # A boire jusqu'à
    to_drink_until = "#features > div:nth-child(1) > section > div > div > div > div.table-row-css > div:nth-child(3) > div > div:nth-child(4) > div.table-cell-css.vertical-align-top.padding-vertical-5.taille-xs.color-gray-darker.text-bold"
    to_drink_until_2 = "#features > div:nth-child(1) > section > div > div > div > div.table-row-css > div:nth-child(3) > div > div:nth-child(5) > div.table-cell-css.vertical-align-top.padding-vertical-5.taille-xs.color-gray-darker.text-bold"
    #Accords Mets Vins
    food_and_wine_matches = "#features > div:nth-child(1) > section > div > div > div > div.table-row-css > div:nth-child(4) > div > div > div.table-cell-css.vertical-align-top.padding-vertical-5.taille-xs.color-gray-darker.text-bold"
    accords_recommandés = ""
    teaser = "#description_courte > strong"
    resume = "#description_courte_content > div"
    image = "#view_full_size > img"
    prices = "#buy_block > div.price > div"
    unit_price = "#our_price_display > span > span"
    group_price = "#buy_block > div.price.full-width.full-height.table-css > div > div.quantity-discount.color-gray.margin-bottom-10"
    
    capacity = "#center_column > div:nth-child(6) > div > div.pb-center-column.col-xs-12.color-gray-darker.no-margin-bottom > div > div > div.table-cell-css.largeur-xs-12.largeur-md-10 > div > div:nth-child(3) > div > div > div > div.largeur-xs-12.largeur-md-8.table-cell-css.vertical-align-top.padding-right-20.padding-top-30.no-padding-vertical-xs.no-padding-vertical-sm.no-padding-right-sm.no-padding-right-xs > div > div.col-xs-12.col-sm-8.col-md-8.col-lg-8.no-padding-left.padding-right-30 > div.title > div:nth-child(2) > div > h2 > span:nth-child(1) > span"
    capacity_2 = "#center_column > div:nth-child(6) > div > div.pb-center-column.col-xs-12.color-gray-darker.no-margin-bottom > div > div > div.table-cell-css.largeur-xs-12.largeur-md-10 > div > div:nth-child(3) > div > div > div > div.largeur-xs-12.largeur-md-8.table-cell-css.vertical-align-top.padding-right-20.padding-top-30.no-padding-vertical-xs.no-padding-vertical-sm.no-padding-right-sm.no-padding-right-xs > div > div.col-xs-12.col-sm-8.col-md-8.col-lg-8.no-padding-left.padding-right-30 > div.title > div:nth-child(2) > div > h2 > span:nth-child(1) > div > div > button"
    capacity_3 = "#center_column > div:nth-child(6) > div > div.pb-center-column.col-xs-12.color-gray-darker.no-margin-bottom > div > div > div.table-cell-css.largeur-xs-12.largeur-md-10 > div > div:nth-child(4) > div > div > div > div.largeur-xs-12.largeur-md-8.table-cell-css.vertical-align-top.padding-right-20.padding-top-30.no-padding-vertical-xs.no-padding-vertical-sm.no-padding-right-sm.no-padding-right-xs > div > div.col-xs-12.col-sm-8.col-md-8.col-lg-8.no-padding-left.padding-right-30 > div.title > div:nth-child(2) > div > h2 > span:nth-child(1) > span"
    capacity_section = "#center_column > div:nth-child(6) > div > div.pb-center-column.col-xs-12.color-gray-darker.no-margin-bottom > div > div > div.table-cell-css.largeur-xs-12.largeur-md-10 > div > div:nth-child(4) > div > div > div > div.largeur-xs-12.largeur-md-8.table-cell-css.vertical-align-top.padding-right-20.padding-top-30.no-padding-vertical-xs.no-padding-vertical-sm.no-padding-right-sm.no-padding-right-xs > div > div.col-xs-12.col-sm-8.col-md-8.col-lg-8.no-padding-left.padding-right-30 > div.title > div:nth-child(2) > div > h2"
    capacity_section_2 = "#center_column > div:nth-child(6) > div > div.pb-center-column.col-xs-12.color-gray-darker.no-margin-bottom > div > div > div.table-cell-css.largeur-xs-12.largeur-md-10 > div > div:nth-child(4) > div > div > div > div.largeur-xs-12.largeur-md-8.table-cell-css.vertical-align-top.padding-right-20.padding-top-30.no-padding-vertical-xs.no-padding-vertical-sm.no-padding-right-sm.no-padding-right-xs > div > div.col-xs-12.col-sm-8.col-md-8.col-lg-8.no-padding-left.padding-right-30 > div.title > div:nth-child(2)"
    capacity_section_3 = "#center_column > div:nth-child(6) > div > div.pb-center-column.col-xs-12.color-gray-darker.no-margin-bottom > div > div > div > div > div:nth-child(4) > div > div > div > div.largeur-xs-12.largeur-md-8.table-cell-css.vertical-align-top.padding-right-20.padding-top-30.no-padding-vertical-xs.no-padding-vertical-sm.no-padding-right-sm.no-padding-right-xs > div > div.col-xs-12.col-sm-8.col-md-8.col-lg-8.no-padding-left.padding-right-30 > div.title > div:nth-child(2) > div > h2 > span:nth-child(1) > span"
    
    rewards_section = "#center_column > div:nth-child(6) > div > div.pb-center-column.col-xs-12.color-gray-darker.no-margin-bottom > div > div > div.table-cell-css.largeur-xs-12.largeur-md-10 > div > div:nth-child(3) > div > div > div > div.pb-left-column.largeur-xs-12.largeur-md-4.table-cell-css.vertical-align-top.padding-top-30.padding-bottom-10-xs.padding-bottom-10-sm.position-relative > div.recompenses-conteneur-product.recompenses-left.text-align-left"
    rewards_2 = "#center_column > div:nth-child(6) > div > div.pb-center-column.col-xs-12.color-gray-darker.no-margin-bottom > div > div > div.table-cell-css.largeur-xs-12.largeur-md-10 > div > div:nth-child(3) > div > div > div > div.pb-left-column.largeur-xs-12.largeur-md-4.table-cell-css.vertical-align-top.padding-top-30.padding-bottom-10-xs.padding-bottom-10-sm.position-relative > div.recompenses-conteneur-product.recompenses-left.text-align-left"
    product_list = "div#center_column > div.row.product_list.product_list_v2.list.no-padding-lg.no-padding-md"
    first_features_section = "#features > div:nth-child(1) > section > div > div > div > div.table-row-css > div:nth-child(1)"
    first_features_section_2 = "#features > div:nth-child(1) > section"
    features_section = "#features > div:nth-child(1) > section"
    second_features_section = "#features > div:nth-child(1) > section > div > div > div > div.table-row-css > div:nth-child(2)"
    
    test = "table-row-css"
    header = "#center_column > div:nth-child(6) > div > div.pb-center-column.col-xs-12.color-gray-darker.no-margin-bottom > div > div > div.table-cell-css.largeur-xs-12.largeur-md-10 > div > div:nth-child(3) > div > div > div > div.largeur-xs-12.largeur-md-8.table-cell-css.vertical-align-top.padding-right-20.padding-top-30.no-padding-vertical-xs.no-padding-vertical-sm.no-padding-right-sm.no-padding-right-xs > div > div.col-xs-12.col-sm-8.col-md-8.col-lg-8.no-padding-left.padding-right-30 > div.title > div:nth-child(2) > div > h2 > span.ss-titre.color-gray-darker.taille-xs.line-height-15-xs.no-padding-horizontal"
    body = "body#product"
    erreur = "#KAKAKAKAKAKAK"
class data:

    def __init__(self):
        self.designation_abbr = ['DOCG', 'DO','AOP', 'AOC', 'IGT', 'IGP', 'DOC', 'DOP', 'VDP', 'DAC']
        self.fr_regions = ['Normandie', 'Collines Rhodaniennes', 'Savoie-Bugey', 'Jura', 'Corse', 'Savoie', 'Loire', 'Alsace', 'Beaujolais', 'Provence', 'Languedoc-Roussillon', 'Bordeaux', 'Rhône', 'Vin de France', 'Sud-Ouest', 'Bourgogne']
        self.foreign_regions = ['Bairrada', 'Normandie', 'Mount Barker', 'Emilie - Romagne', 'Rheingau', 'Cafayate', 'Lombardie', 'Mosel Saar', 'Vallée du Limari', 'Medimurskog vinogorja', 'Toscane', 'Alto Adige', 'Pfalz', 'Coastal Region', 'Bierzo', 'West Sussex', 'Swartland','Tokaj', 'Vallée de Curico', 'Campanie', 'Nahe', 'Vallée de Aconcagua', 'Pays Vasco', 'Collines Rhodaniennes', 'Vinho Verde', 'Carinena' ,'Rhône', 'Weinviertel', 'Wachau', 'Canton de Genève', 'Alsace', 'Sud-Ouest', 'Péloponnèses', 'Napa Valley', 'Marches', 'Rueda', 'Canton du Valais', 'Mallorca','Vénétie', 'Mosel', 'Eden Valley' 'Canton du Valais', 'Plateau du Golan', 'Galilée', 'Toscana', 'Kakheti', 'South Australia', 'Russian River Valley', "Vallée de l'Aconcagua", 'Vallée de Itata', 'Barossa Valley', "Vallée de l'Oronte", 'Douro', 'Vallée de Colchagua', 'Castilla la Mancha', 'Bierzo', 'Stellenbosch', 'Kamptal', 'Îles Canaries', 'Vénétie', 'Murfatlar', 'Punta del Este, Garzon', 'Abruzzes', 'Piémont', 'Sicile', 'Galicia', 'Vallée de Uco Mendoza', 'Catalogne', 'Mc Laren Vale', 'Marlborough', "Désert d'Atacama", 'Alicante', 'Rioja', 'Colchagua Valley', 'South Eastern Australia', 'Tulum Valley', 'Cuenca', 'Western Cape', 'Mancha','Murcie','Central Coast', 'Pouilles', 'Valle de Guadalupe', 'Navarre', 'Sonoma County', 'Castilla y Leon', 'Valencia', 'Savoie-Bugey', 'Jura', 'Corse', 'Savoie', 'Loire', 'Alsace', 'Beaujolais', 'Provence', 'Languedoc-Roussillon', 'Bordeaux', 'Rhône', 'Vin de France', 'Sud-Ouest', 'Bourgogne']
        self.states = ['Galicia', 'Cap occidental', 'Barossa Valley', 'Californie', 'Baja California', 'Washington']
        self.country = ['Angleterre', 'Hongrie', 'Croatie', 'Autriche', 'Grèce', 'France', 'Allemagne', 'Israël', 'Syrie', 'Maroc', 'Bulgarie', 'Géorgie', 'Portugal' ,'Roumanie', 'Suisse', 'Uruguay', 'Nouvelle-Zélande', 'Argentine', 'Chili', 'Afrique du Sud','Australie', 'Etats-Unis', 'Espagne', 'Mexique', 'Italie']
        self.designation_of_origin = ['Mount Barrow', 'Rheingau', 'Vino de la terra de Castilla y Leon', 'Beaune 1er cru', 'Vin Mousseux de Qualité', "Tokay, tokaj", "Cava","Petit Chablis", "Vin de pays de l'Hérault", 'Savoie-Bugey', 'Kistauri', 'Chorey-Lès-Beaune', 'Fleurie', 'Terra Alta', 'Castillon - Côtes de Bordeaux', 'Lolol', 'Vino de España', 'Chianti Classico Riserva', 'Chianti', 'Jumilla', 'Rueda', 'Priorat','Saint-Chinian', 'Côtes du Rhône Villages', 'Saumur Champigny AOC', 'Hermitage AOC' ,'Crozes-Hermitage AOC', 'Rasteau AOC', 'Castillon - Côtes de Bordeaux AOC', 'Médoc AOC', 'Lalande de Pomerol AOC', 'Marcillac AOP', 'Aude Hauterive IGP', 'Régnié AOC', 'Brouilly AOC', 'Mercurey 1er cru AOC', 'Saint-Amour AOC', 'Saint-Emilion AOC', 'Côtes du Rhône Villages AOP', 'Médoc AOC', 'Saint-Joseph AOP' 'Côtes du Rhône Villages AOC', 'Côte-Rôtie AOC', 'Gigondas', 'Montepulciano DOC', 'Saint-Joseph AOP', 'Pic-Saint-Loup AOC', 'Côte de Brouilly AOC' 'Hérault VDP', 'Graves AOC', 'Monthelie AOC','Beaujolais AOC', 'Rasteau AOC','Médoc AOP', 'Hautes Côtes de Beaune AOC', 'Vaucluse IGP', 'Ardèche IGP', 'Côtes du Roussillon Villages AOC', 'San Severo DOC', 'Gigondas AOC', 'Gigondas AOP', 'Corbieres AOP', 'Châteauneuf-du-Pape AOP', 'Côtes du Roussillon Villages AOC', 'Toro DO', 'Médoc AOP', 'Beaumes de Venise AOC', 'Cairanne AOC', 'La Clape AOP','Atacama DO','La Clape AOC', 'Coteaux Bourguignons AOC', 'Morgon AOC', 'Cabardès AOC', 'Montsant', 'Terrasses du Larzac AOC', 'Saint-Joseph AOC', 'Côtes de Duras AOC', 'Puglia DOC', 'Blaye - Côtes de bordeaux AOC', 'Carcassonne IGP', 'Morgon AOC', 'Alicante DO', 'Rioja DO', 'Costières de Nîmes AOC', 'Var IGP', 'Mercurey AOC', 'Minervois AOP', 'Ventoux AOC', 'Terres du Midi IGP', 'Ribera del Jucar DO', 'Bordeaux Supérieur AOC', 'Coteaux de Peyriac IGP', 'Haut-Médoc AOC', 'Côtes de Bordeaux AOC','Valencia DO', 'Lussac Saint-Emilion AOC', 'La Mancha DO','Côtes Catalanes IGP', 'Bullas DO', 'Saint-Julien AOC','Moulis AOC', 'Pomerol AOC', 'Saint-Emilion 1er Grand Cru Classé AOC', 'Côte de Brouilly', 'Manchuela DO', 'Côtes de Bourg AOC', 'Languedoc AOC', 'Côtes du Rhône AOC', 'Bordeaux AOC', "Pays d'Oc IGP", 'Faugères AOC', 'Bourgogne AOC', 'Châteauneuf-du-Pape AOC', 'Puglia IGP', 'Côtes de Gascogne IGP', 'Ribera del Duero DO', 'Margaux AOC', 'Saint-Emilion Grand Cru AOC', 'Pessac-Léognan AOC', 'Navarra DO', 'Bergerac AOC', 'Saint-Estèphe AOC', 'Lirac AOC', 'Vacqueyras AOC', 'Pauillac AOC', 'Blaye - Côtes de bordeaux']
        self.color = ['Vin Rouge', 'Vin Rose', 'Vin Rosé', 'Vin Blanc', 'Cubi Rouge', 'Cubi Blanc','Cubi Rosé', 'Cubi Rose', 'Vin Orange', 'Vin Ambré', 'Vin Ambre', 'Effervescent Rosé', 'Effervescent Blanc', 'Champagne Blanc', 'Champagne Rose']