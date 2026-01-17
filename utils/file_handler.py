# utils/file_handler.py

def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues.

    Args:
        filename (str): Path to sales_data.txt file

    Returns:
        list: List of raw transaction lines (strings)
    """

    encodings = ['utf-8', 'latin-1', 'cp1252']
    lines = []

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()
            # If reading is successful, break the loop
            break
        except UnicodeDecodeError:
            # Try next encoding
            continue
        except FileNotFoundError:
            print(f"Error: File not found -> {filename}")
            return []

    if not lines:
        print("Error: Unable to read file with supported encodings.")
        return []

    # Remove header and empty lines
    cleaned_lines = []
    for line in lines[1:]:  # Skip header
        line = line.strip()
        if line:
            cleaned_lines.append(line)

    return cleaned_lines



def parse_transactions(raw_lines):
    """
    Parses raw sales lines into a cleaned list of dictionaries.

    Args:
        raw_lines (list): List of raw transaction strings

    Returns:
        list: List of parsed transaction dictionaries
    """

    transactions = []

    for line in raw_lines:
        parts = line.split('|')

        # Skip rows with incorrect number of fields
        if len(parts) != 8:
            continue

        (
            transaction_id,
            date,
            product_id,
            product_name,
            quantity,
            unit_price,
            customer_id,
            region
        ) = parts

        # Clean ProductName (remove commas / take base name)
        product_name = product_name.split(',')[0].strip()

        # Clean numeric fields (remove commas)
        quantity = quantity.replace(',', '').strip()
        unit_price = unit_price.replace(',', '').strip()

        try:
            quantity = int(quantity)
            unit_price = float(unit_price)
        except ValueError:
            # Skip records with invalid numeric conversion
            continue

        transaction = {
            "TransactionID": transaction_id.strip(),
            "Date": date.strip(),
            "ProductID": product_id.strip(),
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id.strip(),
            "Region": region.strip()
        }

        transactions.append(transaction)

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters.

    Args:
        transactions (list): list of transaction dictionaries
        region (str): region filter (optional)
        min_amount (float): minimum transaction amount (optional)
        max_amount (float): maximum transaction amount (optional)

    Returns:
        tuple: (valid_transactions, invalid_count, summary_dict)
    """

    total_input = len(transactions)
    valid_transactions = []
    invalid_count = 0

    # ---------- VALIDATION ----------
    for tx in transactions:
        try:
            if (
                tx.get("Quantity") <= 0 or
                tx.get("UnitPrice") <= 0 or
                not tx.get("TransactionID", "").startswith("T") or
                not tx.get("ProductID", "").startswith("P") or
                not tx.get("CustomerID", "").startswith("C") or
                not tx.get("Region")
            ):
                invalid_count += 1
                continue

            valid_transactions.append(tx)

        except Exception:
            invalid_count += 1

    # ---------- FILTERING ----------
    filtered_by_region = 0
    filtered_by_amount = 0

    filtered_transactions = []

    for tx in valid_transactions:
        amount = tx["Quantity"] * tx["UnitPrice"]

        # Region filter
        if region and tx["Region"] != region:
            filtered_by_region += 1
            continue

        # Amount filter
        if min_amount is not None and amount < min_amount:
            filtered_by_amount += 1
            continue

        if max_amount is not None and amount > max_amount:
            filtered_by_amount += 1
            continue

        filtered_transactions.append(tx)

    summary = {
        "total_input": total_input,
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(filtered_transactions)
    }

    # ---------- DISPLAY (Required) ----------
    print("Available regions:", sorted(set(tx["Region"] for tx in valid_transactions)))
    print("Transaction amount range:",
          min(tx["Quantity"] * tx["UnitPrice"] for tx in valid_transactions),
          "-",
          max(tx["Quantity"] * tx["UnitPrice"] for tx in valid_transactions))
    print("Records after filtering:", summary["final_count"])

    return filtered_transactions, invalid_count, summary
