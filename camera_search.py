from bs4 import BeautifulSoup
import re
import requests

page_link = 'https://www.wexphotovideo.com/used-dslrs/#esp_category_sort=FSM_Rational_Price&esp_category_order=desc&esp_category_hitsperpage=&esp_category_cf=Model&esp_category_filter_Manufacturer=Canon&esp_category_filter_Model=EOS%205D%20Mk%20III'
# fetch the content from url
try:
    page_response = requests.get(page_link, timeout=5)
except requests.ConnectionError:
    pass
# parse html
page_content = BeautifulSoup(page_response.content, "html.parser")
cameras = page_content.find_all(class_='listing-product clearfix')
# print(cameras)
for camera in cameras:
    model = camera.find(string=re.compile("5D Mark III"))
    if model:
        print(model)
        print(camera.find(class_="condition"))
    # condition = camera.find(class_='condition')
    # print(condition)

