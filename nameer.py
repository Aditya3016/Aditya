import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# Initialize the browser (make sure chromedriver is set up correctly)
driver = webdriver.Chrome()

brands = []
product_names = []
prices = []

for page in range(1, 6):
    url = f"https://www.myntra.com/t-shirt-under-5000?rawQuery=t-shirt%20under%205000&page={page}"
    driver.get(url)

    # Wait until products are loaded
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product-base"))
        )
    except:
        print(f"[!] Timeout on page {page}")
        continue

    products = driver.find_elements(By.CLASS_NAME, "product-base")

    for product in products:
        try:
            brand = product.find_element(By.CLASS_NAME, "product-brand").text
            name = product.find_element(By.CLASS_NAME, "product-product").text

            try:
                price_text = product.find_element(By.CLASS_NAME, "product-discountedPrice").text
            except NoSuchElementException:
                price_text = product.find_element(By.CLASS_NAME, "product-price").text

            price = ''.join([char for char in price_text if char.isdigit()])

            brands.append(brand)
            product_names.append(name)
            prices.append(price)

        except Exception as e:
            print(f"Skipping product due to error: {e}")
            continue

driver.quit()

# Create DataFrame
df = pd.DataFrame({
    "Brand": brands,
    "Product Name": product_names,
    "Price (INR)": prices
})

# Convert prices to numeric
df["Price (INR)"] = pd.to_numeric(df["Price (INR)"], errors="coerce")

# Save to CSV
df.to_csv("Myntra_TShirts_Under_5000.csv", index=False)

# Output summary
print("✅ Scraping complete. CSV saved successfully.")
print(f"\n📦 Total Products Scraped: {len(df)}")
print(df.head())
