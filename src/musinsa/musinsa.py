from selenium import webdriver
from selenium.webdriver.common.by import By
import json

CLOTH_IDS = {
  "001006": "니트/스웨터",
  "001005": "맨투맨/스췌트셔츠",
}

first_url = "https://www.musinsa.com/categories/item/{0}"
url_format = "https://www.musinsa.com/categories/item/{0}?d_cat_cd={0}&brand=&list_kind=small&sort=pop_category&sub_sort=&page={1}&display_cnt=90&group_sale=&exclusive_yn=&sale_goods=&timesale_yn=&ex_soldout=&kids=&color=&price1=&price2=&shoeSizeOption=&tags=&campaign_id=&includeKeywords=&measure="

pages = []
browser = webdriver.Safari()
for _cloth_id in CLOTH_IDS:
  total_paging_num = None
  browser.get(first_url.format(_cloth_id))
  browser.implicitly_wait(0.5)
  _total_paging_nums = browser.find_elements(By.CLASS_NAME, "totalPagingNum")
  for _total_paging_num in _total_paging_nums:
    # total_paging_num = _total_paging_num
    if total_paging_num is None:
      total_paging_num = int(_total_paging_num.text)
    else:
      assert total_paging_num == int(_total_paging_num.text)
  print(f"{CLOTH_IDS[_cloth_id]} total pages: {total_paging_num}")
  
  for page_id in range(1, total_paging_num+1):
    browser.get(url_format.format(_cloth_id, page_id))
    browser.implicitly_wait(1.0)    
    cloth_pages = browser.find_elements(By.CLASS_NAME, "img-block")
    for cloth_page in cloth_pages:
      pages.append({
        "url": cloth_page.get_attribute("href"),
        "title": cloth_page.get_attribute("title"),
        "name": cloth_page.get_attribute("name")
      })
      
with open("cloth_urls.json", "w") as f:
  json.dump(pages, f)
  