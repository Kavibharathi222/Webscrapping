import time
import csv
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# Set up Chrome options and driver
options = Options()
options.add_argument("--headless")  
driver_path = "C:\webdriver\chromedriver"  
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

def scrape_amazon_best_sellers(url):
    driver.get(url)
    time.sleep(3)  
    
    products_data = []

    try:
        # Locate the product containers
        product_elements = driver.find_elements(By.CSS_SELECTOR, ".zg-item-immersion")
        
        for product in product_elements:
            product_data = {}
            
            # Extract product details
            try:
                product_data["Product Name"] = product.find_element(By.CSS_SELECTOR, ".p13n-sc-truncated").text
            except:
                product_data["Product Name"] = None
            
            try:
                product_data["Product Price"] = product.find_element(By.CSS_SELECTOR, ".p-price .p-whole").text
            except:
                product_data["Product Price"] = None

            try:
                product_data["Sale Discount"] = product.find_element(By.CSS_SELECTOR, ".p-badge").text
            except:
                product_data["Sale Discount"] = None

            try:
                product_data["Best Seller Rating"] = product.find_element(By.CSS_SELECTOR, ".a-icon.a-icon-star").text
            except:
                product_data["Best Seller Rating"] = None
            
            try:
                product_data["Ship From"] = product.find_element(By.CSS_SELECTOR, ".a-size-small.a-color-secondary").text
            except:
                product_data["Ship From"] = None
            
            try:
                product_data["Sold By"] = product.find_element(By.CSS_SELECTOR, ".a-size-small.a-color-secondary.a-text-bold").text
            except:
                product_data["Sold By"] = None

            try:
                product_data["Rating"] = product.find_element(By.CSS_SELECTOR, ".a-icon-star").text
            except:
                product_data["Rating"] = None

            try:
                product_data["Product Description"] = product.find_element(By.CSS_SELECTOR, ".a-size-base.a-color-secondary").text
            except:
                product_data["Product Description"] = None

            try:
                product_data["Number Bought in the Past Month"] = product.find_element(By.CSS_SELECTOR, ".a-size-small.a-color-secondary").text
            except:
                product_data["Number Bought in the Past Month"] = None

            # Store the category name (can be extracted from the URL or manually specified)
            product_data["Category Name"] = url.split('/')[-2]
            
            # Get all available images
            images = product.find_elements(By.CSS_SELECTOR, ".a-dynamic-image")
            image_urls = [img.get_attribute("src") for img in images]
            product_data["All Available Images"] = image_urls

            products_data.append(product_data)

    except Exception as e:
        print(f"Error while scraping data: {e}")
    
    return products_data

def save_to_file(data, filename="products_data.json"):
    # Save data in JSON format
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def save_to_csv(data, filename="products_data.csv"):
    # Save data in CSV format
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

def main():
    category_urls = [
        "https://www.amazon.in/gp/bestsellers/kitchen/ref=zg_bs_nav_kitchen_0",
        "https://www.amazon.in/gp/bestsellers/shoes/ref=zg_bs_nav_shoes_0",
        "https://www.amazon.in/gp/bestsellers/computers/ref=zg_bs_nav_computers_0",
        "https://www.amazon.in/gp/bestsellers/electronics/ref=zg_bs_nav_electronics_0"
    ]
    
    all_products = []

    for url in category_urls:
        print(f"Scraping data from {url}...")
        products = scrape_amazon_best_sellers(url)
        all_products.extend(products)

    # Save the scraped data
    save_to_json = input("Would you like to save data in JSON format? (yes/no): ").strip().lower()
    if save_to_json == 'yes':
        save_to_file(all_products, "amazon_best_sellers.json")
    
    save_to_csv = input("Would you like to save data in CSV format? (yes/no): ").strip().lower()
    if save_to_csv == 'yes':
        save_to_csv(all_products, "amazon_best_sellers.csv")

    driver.quit()

if __name__ == "__main__":
    main()
