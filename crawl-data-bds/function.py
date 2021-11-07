from bs4 import BeautifulSoup
import math


def crawl_apartment_links_of_a_page(url, scraper, headers):
    html = scraper.get(url, headers=headers).content
    soup = BeautifulSoup(html, 'html.parser')
    apartments = soup.find_all('a', class_="js__product-link-for-product-id")
    for i in range(len(apartments)):
        apartments[i] = 'https://batdongsan.com.vn' + apartments[i].get('href')
    return apartments


def crawl_apartment_info(url, scraper, headers):
    html = scraper.get(url, headers=headers).content
    soup = BeautifulSoup(html, 'html.parser')
    info_dict = {'url': url, 'title': None, 'address': None, 'bedroom': None, 'toilet': None, 'investor': None, 'acreage': None,
                 'price': None, 'lat': None, 'long': None, 'distance': None, 'images': [], 'description': None}

    # crawl address, bedroom, toilet, investor
    list_standards = soup.find_all('div', class_="re__list-standard-1line--md")
    for list_standard in list_standards:
        if list_standard.find('span', class_="title").text == 'Địa chỉ:':
            info_dict['address'] = list_standard.find('span', class_="value").text.lower()
        elif list_standard.find('span', class_="title").text == 'Số phòng ngủ:':
            info_dict['bedroom'] = list_standard.find('span', class_="value").text.lower()
        elif list_standard.find('span', class_="title").text == 'Số toilet:':
            info_dict['toilet'] = list_standard.find('span', class_="value").text.lower()
        elif list_standard.find('span', class_="title").text == 'Chủ đầu tư:':
            info_dict['investor'] = list_standard.find('span', class_="value").text.lower()

    # price, acreage, bedroom
    info_items = soup.find_all('div', class_="re__pr-short-info-item js__pr-short-info-item")
    for info_item in info_items:
        if info_item.find('span', class_="title").text == 'Mức giá':
            if info_item.find('span', class_="ext") is not None:
                info_dict['price'] = info_item.find('span', class_="ext").text.lower()
            else:
                info_dict['price'] = info_item.find('span', class_="value").text.lower()
        elif info_item.find('span', class_="title").text == 'Diện tích':
            info_dict['acreage'] = info_item.find('span', class_="value").text.lower()
        elif info_item.find('span', class_="title").text == 'Phòng ngủ':
            info_dict['bedroom'] = info_item.find('span', class_="value").text.lower()

    # lat, long
    location = soup.find('div', class_="re__section re__pr-map js__section").find('iframe').get('data-src')
    location = location[location.index('q=') + 2:location.index('&')].split(',')
    location = list(map(lambda x: float(x), location))
    info_dict['lat'] = location[0]
    info_dict['long'] = location[1]
    info_dict['distance'] = distance_to_center(location)

    # description
    info_dict['description'] = soup.find('div', class_="re__section-body re__detail-content js__section-body "
                                                       "js__pr-description js__tracking").text.strip().lower()

    # images
    images = soup.find_all('div', class_="re__media-thumb-item")
    for image in images:
        info_dict['images'].append(image.find('img').get('data-src'))

    # title
    info_dict['title'] = soup.find('h1', class_="re__pr-title pr-title").text.lower()

    return info_dict


def distance_to_center(location):
    center = list(map(lambda x: math.radians(x), [21.028889, 105.8525]))
    location = list(map(lambda x: math.radians(x), location))
    return 6378 * math.acos((math.sin(location[0]) * math.sin(center[0]))
                            + (math.cos(location[0]) * math.cos(center[0]) * math.cos(center[1] - location[1])))
