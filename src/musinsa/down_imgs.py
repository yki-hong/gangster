from selenium import webdriver
from selenium.webdriver.common.by import By
import hashlib
import requests
import shutil
import json
import os
import random
import time

with open("./cloth_urls.json", "r") as f:
  pages = json.load(f)

DATA_PATH = "../../data/musinsa"
browser = webdriver.Safari()
for page in pages:
  url = page["url"]
  img_folder_name = hashlib.md5(url.encode()).hexdigest()
  if not os.path.exists(os.path.join(DATA_PATH, img_folder_name)):
    os.makedirs(os.path.join(DATA_PATH, img_folder_name))
  else:
    continue

  # save page_url info
  with open(os.path.join(DATA_PATH, img_folder_name, "page_info.json"), "w") as _f:
    json.dump(page, _f)
  time.sleep(random.randint(3,10) ** 2)

  print(f"Open {url} ...")
  browser.get(url)
  browser.implicitly_wait(0.5)

  product_thumbs = browser.find_elements(By.CLASS_NAME, "product_thumb")
  for _product_thumb in product_thumbs:
    for _img_tag in _product_thumb.find_elements(By.TAG_NAME, "img"):
      img_url = _img_tag.get_attribute("src").replace("60.jpg", "500.jpg")
      img_alt = _img_tag.get_attribute("alt")
      hashed_img_url =  hashlib.md5(img_url.encode()).hexdigest()
      with open(os.path.join(DATA_PATH, img_folder_name, f"{hashed_img_url}.json"), "w") as f:
        json.dump({"url": img_url, "alt": img_alt}, f)
      if not os.path.exists(os.path.join(DATA_PATH, img_folder_name, f"{hashed_img_url}.jpg")):
        time.sleep(random.randint(2,6))
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
          response.raw.decode_content = True
          with open(os.path.join(DATA_PATH, img_folder_name, f"{hashed_img_url}.jpg"), "wb") as img_file:
            shutil.copyfileobj(response.raw, img_file)
          print(f"\t Save "+ os.path.join(DATA_PATH, img_folder_name, f"{hashed_img_url}.jpg"))
          del response
        
    
