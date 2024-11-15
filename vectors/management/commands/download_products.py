import requests
import csv

url = "https://skygarden.search.windows.net/indexes/productsv3-prod/docs/search"

querystring = {"api-version":"2017-11-11"}

def remove_duplicates(data):
    unique_data = []
    seen_titles = set()
    for item in data:
        title = item.get('title')
        if title not in seen_titles:
            unique_data.append(item)
            seen_titles.add(title)
    return unique_data

def get_products(start=0, stop=1000):
    payload = {
        "search": "*",
        "filter": "category_id eq '284' and (structure eq 'standalone' or structure eq 'parent')",
        "count": True,
        "top": stop,
        "skip": start,
        "orderby": "date_created desc",
        "select": "short_url_code, title, original_image, slug, stock_record_price_retail, description, date_created"
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "insomnia/9.3.3",
        "Api-Key": "11AE9D65AB2130E912F883DBD27324D7"
    }

    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data.get('value', [])
    else:
        raise Exception(f"API request failed with status code {response.status_code}")

products = []
# Check if the response is successful
start = 0
skip = 1000
while skip <= 5000:
    data = get_products(start, skip)
    products.extend(data)  # Use extend instead of append to add individual products
    start = skip
    skip += 1000

print(f"Total products fetched: {len(products)}")
# Remove duplicates based on title
products = remove_duplicates(products)

print(f"Number of unique products after removing duplicates: {len(products)}")

# Open a CSV file for writing
with open('products.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # Create a CSV writer object
    writer = csv.DictWriter(csvfile, fieldnames=['code', 'title', 'image', 'slug', 'price', 'description', 'date_created'])
    
    # Write the header row
    writer.writeheader()
    
    # Write each product to the CSV file
    for product in products:
        # Clean description
        description = product.get('description', '')
        # Remove large spaces
        description = ' '.join(description.split())
        # Remove special characters, keeping basic punctuation
        description = ''.join(char for char in description if char.isalnum() or char in [' ', '.', ',', '!', '?', '-'])
        
        writer.writerow({
            'code': product.get('short_url_code', ''),
            'title': product.get('title', ''),
            'image': product.get('original_image', ''),
            'slug': product.get('slug', ''),
            'price': product.get('stock_record_price_retail', ''),
            'description': description,
            'date_created': product.get('date_created', '')
        })

print("CSV file 'products.csv' has been created successfully.")
