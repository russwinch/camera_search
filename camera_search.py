"""
Searches for used Canon 5D Mk III on wexphotovideo.com.
"""
from bs4 import BeautifulSoup
import requests

import instance.config as config


def find_cameras(target_condition=None):
    """
    Find cameras in a webpage and determine if they match the condition.

    :target_condition: a list of the desired conditions the camera can be in
    """
    url = 'https://www.wexphotovideo.com/used-dslrs/?esp_category_filter_Manufacturer=Canon&esp_category_filter_Model=EOS%205D%20Mk%20III&esp_category_filter_StockStatus=1&esp_category_filter_StockStatus=2&esp_category_filter_StockStatus=11&facetMode=data'
    response = requests.get(url, timeout=5)
    response_dict = response.json()
    html = response_dict['zones'][0]['html']

    page_content = BeautifulSoup(html, "html.parser")
    cameras = page_content.find_all(class_='listing-product clearfix')

    found_cameras = []
    for camera in cameras:
        condition = camera.find(class_='condition').span.string
        price = camera.find(class_='price').string
        href = camera.a['href']
        if (condition in target_condition
            and not _check_found_cameras(cid=href,
                                         filepath=config.file_location)):
            found_cameras.append({'condition': condition,
                                  'price': price,
                                  'href': href})
    return found_cameras


def _check_found_cameras(cid=None, filepath=None):
    """
    Compare identified cameras with the list of those found previously.

    :cid: the url of the camera, used as it's unique id
    :filepath: the local file where previously identified cameras are recorded
    """
    with open(filepath, mode='r') as f:
        found = False
        for line in f:
            if line.strip() == cid:
                found = True
        return found


def write_found_cameras(cid=None, filepath=None):
    """"
    Write to the local file of previously identified cameras.

    :cid: the url of the camera, used as it's unique id
    :filepath: the local file where previously identified cameras are recorded
    """
    with open(filepath, mode='a') as f:
        f.write(str(cid) + '\n')


if __name__ == '__main__':
    found = find_cameras(target_condition=['9+', '9'])
    if found:
        print(found)
