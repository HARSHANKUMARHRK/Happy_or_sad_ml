from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
import requests
import hashlib

driver = webdriver.Chrome(ChromeDriverManager().install())

def download_image(url, folder_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Generate a unique filename for the image using its URL hash
            image_hash = hashlib.sha1(url.encode()).hexdigest()
            filename = f"{image_hash}.jpg"
            image_path = os.path.join(folder_path, filename)
            
            with open(image_path, "wb") as f:
                f.write(response.content)
            
            return image_path
        else:
            return None
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None
    
url = "https://www.google.com/search?sxsrf=AB5stBiVS4Xfdnr8jDXh998CkVYXtCeLEw:1689608615925&q=sad+images&tbm=isch&sa=X&ved=2ahUKEwjf6vHKipaAAxV-amwGHR9RBB4Q0pQJegQIFBAB&biw=1848&bih=984&dpr=1"


sad_folder = "./sad_images"
# good_folder = "./good_images"


os.makedirs(sad_folder, exist_ok=True)
# os.makedirs(good_folder, exist_ok=True)


driver.get(url)


image_elements = driver.find_elements_by_tag_name("img")


for img_element in image_elements:
    image_url = img_element.get_attribute("src")
    alt_text = img_element.get_attribute("alt").lower()
    
    if "sad" in alt_text:
        folder_path = sad_folder
    # elif "good" in alt_text:
    #     # folder_path = good_folder
    else:
        continue
    
    downloaded_image_path = download_image(image_url, folder_path)
    if downloaded_image_path:
        print(f"Image downloaded and saved: {downloaded_image_path}")

driver.quit()