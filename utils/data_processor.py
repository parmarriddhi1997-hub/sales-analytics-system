# Task 2.1: Sales Summary Calculator

# a) Calculate Total Revenue

def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions.

    Args:
        transactions (list): list of validated transaction dictionaries

    Returns:
        float: total revenue
    """

    total_revenue = 0.0

    for tx in transactions:
        total_revenue += tx["Quantity"] * tx["UnitPrice"]

    return round(total_revenue, 2)

# b) Region wise Sales Analysis

def region_wise_sales(transactions):
    """
    Analyzes sales by region.

    Args:
        transactions (list): list of validated transaction dictionaries

    Returns:
        dict: region-wise sales statistics
    """

    region_data = {}
    total_revenue = calculate_total_revenue(transactions)

    # Aggregate sales and counts per region
    for tx in transactions:
        region = tx["Region"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0.0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += revenue
        region_data[region]["transaction_count"] += 1

    # Calculate percentage and round values
    for region in region_data:
        percentage = (region_data[region]["total_sales"] / total_revenue) * 100
        region_data[region]["percentage"] = round(percentage, 2)
        region_data[region]["total_sales"] = round(region_data[region]["total_sales"], 2)

    # Sort by total_sales descending
    sorted_region_data = dict(
        sorted(
            region_data.items(),
            key=lambda item: item[1]["total_sales"],
            reverse=True
        )
    )

    return sorted_region_data

# c) Top Selling Products

def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold.

    Args:
        transactions (list): list of validated transaction dictionaries
        n (int): number of top products to return

    Returns:
        list: list of tuples (ProductName, TotalQuantity, TotalRevenue)
    """

    product_summary = {}

    # Aggregate quantity and revenue per product
    for tx in transactions:
        product = tx["ProductName"]
        quantity = tx["Quantity"]
        revenue = quantity * tx["UnitPrice"]

        if product not in product_summary:
            product_summary[product] = {
                "total_quantity": 0,
                "total_revenue": 0.0
            }

        product_summary[product]["total_quantity"] += quantity
        product_summary[product]["total_revenue"] += revenue

    # Sort by total_quantity descending
    sorted_products = sorted(
        product_summary.items(),
        key=lambda item: item[1]["total_quantity"],
        reverse=True
    )

    # Prepare output format
    top_products = []
    for product, stats in sorted_products[:n]:
        top_products.append(
            (product, stats["total_quantity"], round(stats["total_revenue"], 2))
        )

    return top_products

# d) Customer Purchase Analysis

def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns

    Returns:
        dict: customer-wise statistics sorted by total_spent descending
    """

    customer_data = {}

    # Step 1: Aggregate data per customer
    for tx in transactions:
        customer_id = tx["CustomerID"]
        amount = tx["Quantity"] * tx["UnitPrice"]
        product = tx["ProductName"]

        if customer_id not in customer_data:
            customer_data[customer_id] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products_bought": set()   # use set for uniqueness
            }

        customer_data[customer_id]["total_spent"] += amount
        customer_data[customer_id]["purchase_count"] += 1
        customer_data[customer_id]["products_bought"].add(product)

    # Step 2: Calculate average order value & convert set → list
    for customer_id, stats in customer_data.items():
        stats["avg_order_value"] = round(
            stats["total_spent"] / stats["purchase_count"], 2
        )
        stats["products_bought"] = list(stats["products_bought"])

    # Step 3: Sort by total_spent descending
    sorted_customers = dict(
        sorted(
            customer_data.items(),
            key=lambda item: item[1]["total_spent"],
            reverse=True
        )
    )

    return sorted_customers

# Task 2.2: Date-based Analysis

# a) Daily Sales Trend

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date

    Returns:
        dict: date-wise sales statistics sorted chronologically
    """

    daily_data = {}

    # Step 1: Aggregate data by date
    for tx in transactions:
        date = tx["Date"]
        amount = tx["Quantity"] * tx["UnitPrice"]
        customer_id = tx["CustomerID"]

        if date not in daily_data:
            daily_data[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "unique_customers": set()
            }

        daily_data[date]["revenue"] += amount
        daily_data[date]["transaction_count"] += 1
        daily_data[date]["unique_customers"].add(customer_id)

    # Step 2: Convert set → count & clean structure
    for date, stats in daily_data.items():
        stats["unique_customers"] = len(stats["unique_customers"])
        stats["revenue"] = round(stats["revenue"], 2)

    # Step 3: Sort chronologically by date
    sorted_daily_data = dict(sorted(daily_data.items()))

    return sorted_daily_data

# b) Find Peak Sales Day

def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue

    Returns:
        tuple: (date, revenue, transaction_count)
    """

    daily_summary = {}

    # Step 1: Aggregate revenue & transaction count per date
    for tx in transactions:
        date = tx["Date"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        if date not in daily_summary:
            daily_summary[date] = {
                "revenue": 0.0,
                "transaction_count": 0
            }

        daily_summary[date]["revenue"] += amount
        daily_summary[date]["transaction_count"] += 1

    # Step 2: Find peak revenue day
    peak_date = None
    peak_revenue = 0.0
    peak_count = 0

    for date, stats in daily_summary.items():
        if stats["revenue"] > peak_revenue:
            peak_date = date
            peak_revenue = stats["revenue"]
            peak_count = stats["transaction_count"]

    return (peak_date, round(peak_revenue, 2), peak_count)

# Task 2.3: Product Performance

# a) Low Performing Products

def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales

    Returns:
        list of tuples: (ProductName, TotalQuantity, TotalRevenue)
    """

    product_summary = {}

    # Step 1: Aggregate quantity and revenue per product
    for tx in transactions:
        product = tx["ProductName"]
        quantity = tx["Quantity"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        if product not in product_summary:
            product_summary[product] = {
                "total_quantity": 0,
                "total_revenue": 0.0
            }

        product_summary[product]["total_quantity"] += quantity
        product_summary[product]["total_revenue"] += revenue

    # Step 2: Filter low performing products
    low_products = []
    for product, stats in product_summary.items():
        if stats["total_quantity"] < threshold:
            low_products.append(
                (product, stats["total_quantity"], round(stats["total_revenue"], 2))
            )

    # Step 3: Sort by total quantity ascending
    low_products.sort(key=lambda x: x[1])

    return low_products
