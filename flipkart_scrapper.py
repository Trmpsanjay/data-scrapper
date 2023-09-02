import traceback
# import pandas as pd
from bs4 import BeautifulSoup
import requests

from models.mobile_phone import MobilePhone



# base_url = "https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&otracker=categorytree"


def scrape_flipkart_mobiles(base_url, num_pages=15):
    """
       Scrape smartphone data from Flipkart based on a base URL.

       Args:
           base_url (str): The base URL for the flipkart search query.
           num_pages (int, optional): The number of pages to scrape (default is 15).

       Returns:
           list: A list of MobilePhone objects representing scraped mobile data.
       """
    # looping to get all the 15 pages
    phone_details_list = []
    try:
        for i in range(1,num_pages+1):
            print(f"Scraping page {i}...")
            url = f"{base_url}&page={i}"
            http_resp = requests.get(url)
            soup_obj = BeautifulSoup(http_resp.text, 'lxml')
            data_class = soup_obj.find('div', class_='_1YokD2 _3Mn1Gg')
            phone_details_data = data_class.find_all('div', class_='_13oc-S')
            # Extract mobile details
            for ind_phone in phone_details_data:
                try:
                    phone_name = ind_phone.find('div', class_='_4rR01T').text
                    image_url = ind_phone.find('img', class_='_396cs4')['src']
                    phone_desc_list = ind_phone.find_all('li', class_='rgWa7D')
                    ram = phone_desc_list[0].text
                    display = phone_desc_list[1].text
                    camera = phone_desc_list[2].text
                    price = int(ind_phone.find('div', class_='_30jeq3 _1_WHN1').text[1:].replace(',', ''))
                    try:
                        battery = phone_desc_list[3].text
                    except IndexError:
                        battery = "Info Not Available"
                    try:
                        processor = phone_desc_list[4].text
                    except IndexError:
                        processor = "Info Not Available"
                    try:
                        warranty = phone_desc_list[5].text
                    except IndexError:
                        warranty = "Info Not Available"
                    # phone_details = {
                    #     "Name": phone_name,
                    #     "Ram": ram,
                    #     "Display": display,
                    #     "Camera": camera,
                    #     "Battery": battery,
                    #     "Processor": processor,
                    #     "Warranty": warranty
                    # } will save time if we need to convert into csv or excel
                    # Create a MobilePhone object and add it to the list
                    mobile_phone = MobilePhone(name=phone_name, ram=ram, display=display, camera=camera,
                                               battery=battery, processor=processor, warranty=warranty,
                                               image_url=image_url, price=price)
                    # print(type(phone_details))
                    phone_details_list.append(mobile_phone)
                except IndexError:
                    traceback.print_exc()

                except Exception as e:
                    print("An error occurred:", e)

    except Exception as e:
        print("An error occurred:", e)
    return phone_details_list


if __name__ == "__main__":
    base_url = "https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&otracker=categorytree"
    num_pages = 15  # Adjust this number based on how many pages you want to scrape
    phone_details_list = scrape_flipkart_mobiles(base_url, num_pages)

    for item in phone_details_list:
        print(item._name)
        print(item._price)
