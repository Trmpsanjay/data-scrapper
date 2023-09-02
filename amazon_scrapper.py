
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from models.mobile_phone import MobilePhone

s = HTMLSession()

def get_data(url):
    """
       Fetch HTML data from a given URL using an HTMLSession object.

       Args:
           url (str): The URL to fetch data from.

       Returns:
           BeautifulSoup: The BeautifulSoup object representing the parsed HTML content.
               None if an error occurs during the request.
       """
    try:
        r = s.get(url)
        r.html.render(sleep=1)  # Render  content
        soup = BeautifulSoup(r.html.html, 'lxml')  # Parse HTML with BeautifulSoup with the help of lxml
        return soup
    except Exception as e:
        print(f"An error occurred while fetching data from {url}: {e}")
        return None


def scrape_amazon_mobiles(base_url, num_pages=15):
    """
       Scrape smartphone data from Amazon based on a base URL.

       Args:
           base_url (str): The base URL for the Amazon search query.
           num_pages (int, optional): The number of pages to scrape (default is 15).

       Returns:
           list: A list of MobilePhone objects representing scraped mobile data.
       """
    phone_details_list = []
    # looping to get all the 15 pages
    for i in range(1, num_pages+1):
        print(f"Scraping page {i}...")
        url = f"{base_url}&page={i}"
        soup = get_data(url)
        if soup:
            mobile_link_list = soup.find_all('a',
                                         class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
            for link in mobile_link_list:
                link = 'https://www.amazon.in' + link['href']
                print(f'scrapping page ... : {link}')
                mobile_page = get_data(link)
                # Extract mobile details
                if mobile_page:
                    try:
                        name = mobile_page.find('span', class_="a-size-large product-title-word-break").text
                        price = mobile_page.find('span', class_='a-price-whole').text.replace(',', '')
                        image_url = mobile_page.find('div', class_='imgTagWrapper').find('img')['src']
                        prod_desc_details = mobile_page.find('table', class_='a-normal in-comparison-table').find_all('td',
                                                                                          class_='base-item-column')
                        ram = prod_desc_details[4].text
                        battery = prod_desc_details[13].text + 'mAh Battery'
                        camera = prod_desc_details[10].text
                        warranty = prod_desc_details[9].text
                        processor = prod_desc_details[6].text
                        display = prod_desc_details[1].text
                        # Create a MobilePhone object and add it to the list
                        mobile_phone = MobilePhone(name=name, ram=ram, display=display, camera=camera, battery=battery,
                                                   processor=processor, warranty=warranty, image_url=image_url, price=price)
                        phone_details_list.append(mobile_phone)
                    except Exception as e:
                        print(f'An error occurred while processing {link} \n : {e}')
                        continue
                else:
                    print(f'Unable to scrap page: {link}')
        else:
            print(f'Unable to scrap page: {i}')
    return  phone_details_list

if __name__ == "__main__":
    base_url = "https://www.amazon.in/s?k=smart+phone&rh=n%3A1389432031&ref=nb_sb_noss"
    num_pages = 1  # Adjust this number based on how many pages you want to scrape
    phone_details_list = scrape_amazon_mobiles(base_url, num_pages)

    for item in phone_details_list:
        print(item._name)
        print(item._price)