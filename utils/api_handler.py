# utils/api_handler.py

# Task 3.1: Fetch Product Details

# a) Fetch All Products
import requests

def fetch_all_products():
    """
    Fetches all products from DummyJSON API

    Returns:
        list of product dictionaries
    """

    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        print(f"Successfully fetched {len(products)} products from API")

        return products

    except requests.exceptions.RequestException as e:
        print("Failed to fetch products from API")
        print(f"Error: {e}")
        return []

# b) Create Product Mapping
   
def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info

    Parameters:
        api_products (list): products returned from fetch_all_products()

    Returns:
        dict: mapping of product ID to product details
    """

    product_map = {}

    for product in api_products:
        product_id = product.get("id")

        product_map[product_id] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating")
        }

    return product_map

# Task 3.2: Enrich Sales Data

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    """

    enriched_transactions = []

    for tx in transactions:
        enriched_tx = tx.copy()

        try:
            # Extract numeric product ID (P101 -> 101)
            product_id_str = tx.get("ProductID", "")
            numeric_id = int(product_id_str.replace("P", ""))

            if numeric_id in product_mapping:
                product_info = product_mapping[numeric_id]

                enriched_tx["API_Category"] = product_info.get("category")
                enriched_tx["API_Brand"] = product_info.get("brand")
                enriched_tx["API_Rating"] = product_info.get("rating")
                enriched_tx["API_Match"] = True
            else:
                enriched_tx["API_Category"] = None
                enriched_tx["API_Brand"] = None
                enriched_tx["API_Rating"] = None
                enriched_tx["API_Match"] = False

        except Exception:
            enriched_tx["API_Category"] = None
            enriched_tx["API_Brand"] = None
            enriched_tx["API_Rating"] = None
            enriched_tx["API_Match"] = False

        enriched_transactions.append(enriched_tx)

    # -------- Save to file --------
    output_file = "data/enriched_sales_data.txt"

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            header = [
                "TransactionID", "Date", "ProductID", "ProductName",
                "Quantity", "UnitPrice", "CustomerID", "Region",
                "API_Category", "API_Brand", "API_Rating", "API_Match"
            ]
            f.write("|".join(header) + "\n")

            for tx in enriched_transactions:
                row = [
                    str(tx.get("TransactionID")),
                    str(tx.get("Date")),
                    str(tx.get("ProductID")),
                    str(tx.get("ProductName")),
                    str(tx.get("Quantity")),
                    str(tx.get("UnitPrice")),
                    str(tx.get("CustomerID")),
                    str(tx.get("Region")),
                    str(tx.get("API_Category")),
                    str(tx.get("API_Brand")),
                    str(tx.get("API_Rating")),
                    str(tx.get("API_Match"))
                ]
                f.write("|".join(row) + "\n")

        print(f"Enriched data saved to: {output_file}")

    except Exception as e:
        print("Failed to save enriched data")
        print(e)

    return enriched_transactions

#============================================
def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions back to file using pipe-delimited format
    """

    header = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    try:
        with open(filename, "w", encoding="utf-8") as file:
            # Write header
            file.write("|".join(header) + "\n")

            # Write each enriched transaction
            for tx in enriched_transactions:
                row = [
                    str(tx.get("TransactionID", "")),
                    str(tx.get("Date", "")),
                    str(tx.get("ProductID", "")),
                    str(tx.get("ProductName", "")),
                    str(tx.get("Quantity", "")),
                    str(tx.get("UnitPrice", "")),
                    str(tx.get("CustomerID", "")),
                    str(tx.get("Region", "")),
                    str(tx.get("API_Category", "")) if tx.get("API_Category") is not None else "",
                    str(tx.get("API_Brand", "")) if tx.get("API_Brand") is not None else "",
                    str(tx.get("API_Rating", "")) if tx.get("API_Rating") is not None else "",
                    str(tx.get("API_Match", ""))
                ]

                file.write("|".join(row) + "\n")

        print(f"Enriched sales data saved successfully to: {filename}")

    except Exception as e:
        print("Error while saving enriched sales data")
        print(e)


