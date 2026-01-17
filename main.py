# main.py
#=============================================
# Task 4.1: Generate Comprehensive Text Report
#==============================================

from datetime import datetime
from collections import defaultdict

def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    """
    Generates a comprehensive formatted text report
    """

    # ---------- 2. BASIC METRICS ----------
    total_transactions = len(transactions)
    total_revenue = sum(tx["Quantity"] * tx["UnitPrice"] for tx in transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = [tx["Date"] for tx in transactions]
    start_date = min(dates)
    end_date = max(dates)

    # ---------- 3. REGION-WISE ----------
    region_summary = defaultdict(lambda: {"revenue": 0, "count": 0})

    for tx in transactions:
        region = tx["Region"]
        amount = tx["Quantity"] * tx["UnitPrice"]
        region_summary[region]["revenue"] += amount
        region_summary[region]["count"] += 1

    region_sorted = sorted(
        region_summary.items(),
        key=lambda x: x[1]["revenue"],
        reverse=True
    )

    # ---------- 4. TOP PRODUCTS ----------
    product_summary = defaultdict(lambda: {"qty": 0, "revenue": 0})

    for tx in transactions:
        name = tx["ProductName"]
        product_summary[name]["qty"] += tx["Quantity"]
        product_summary[name]["revenue"] += tx["Quantity"] * tx["UnitPrice"]

    top_products = sorted(
        product_summary.items(),
        key=lambda x: x[1]["qty"],
        reverse=True
    )[:5]

    # ---------- 5. TOP CUSTOMERS ----------
    customer_summary = defaultdict(lambda: {"spent": 0, "count": 0})

    for tx in transactions:
        cid = tx["CustomerID"]
        customer_summary[cid]["spent"] += tx["Quantity"] * tx["UnitPrice"]
        customer_summary[cid]["count"] += 1

    top_customers = sorted(
        customer_summary.items(),
        key=lambda x: x[1]["spent"],
        reverse=True
    )[:5]

    # ---------- 6. DAILY SALES ----------
    daily_summary = defaultdict(lambda: {"revenue": 0, "count": 0, "customers": set()})

    for tx in transactions:
        date = tx["Date"]
        daily_summary[date]["revenue"] += tx["Quantity"] * tx["UnitPrice"]
        daily_summary[date]["count"] += 1
        daily_summary[date]["customers"].add(tx["CustomerID"])

    daily_sorted = sorted(daily_summary.items())

    # ---------- 7. PRODUCT PERFORMANCE ANALYSIS ----------
    # Best selling day
    best_day, best_day_stats = max(
    daily_summary.items(),
    key=lambda x: x[1]["revenue"]
    )

    # Low performing products (quantity < 10)
    low_products = [
    (product, stats["qty"], stats["revenue"])
    for product, stats in product_summary.items()
    if stats["qty"] < 10
    ]
    
    # Average transaction value per region
    avg_tx_value_region = {}
    for region, stats in region_summary.items():
        avg_tx_value_region[region] = (
            stats["revenue"] / stats["count"]
            if stats["count"] else 0
    )

    # ---------- 8. API ENRICHMENT ----------
    enriched_success = [tx for tx in enriched_transactions if tx.get("API_Match")]
    failed_enrichment = [
        tx["ProductName"] for tx in enriched_transactions if not tx.get("API_Match")
    ]

    success_rate = (len(enriched_success) / len(enriched_transactions)) * 100 if enriched_transactions else 0

    # ---------- WRITE REPORT ----------
    with open(output_file, "w", encoding="utf-8") as file:

        # HEADER
        file.write("=" * 44 + "\n")
        file.write("           SALES ANALYTICS REPORT\n")
        file.write(f"     Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"     Records Processed: {total_transactions}\n")
        file.write("=" * 44 + "\n\n")

        # OVERALL SUMMARY
        file.write("OVERALL SUMMARY\n")
        file.write("-" * 44 + "\n")
        file.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        file.write(f"Total Transactions:   {total_transactions}\n")
        file.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
        file.write(f"Date Range:           {start_date} to {end_date}\n\n")

        # REGION PERFORMANCE
        file.write("REGION-WISE PERFORMANCE\n")
        file.write("-" * 44 + "\n")
        file.write(f"{'Region':10}{'Sales':15}{'% of Total':12}{'Transactions'}\n")

        for region, stats in region_sorted:
            pct = (stats["revenue"] / total_revenue) * 100
            file.write(
                f"{region:10}₹{stats['revenue']:,.2f}   {pct:6.2f}%      {stats['count']}\n"
            )
        file.write("\n")

        # TOP PRODUCTS
        file.write("TOP 5 PRODUCTS\n")
        file.write("-" * 44 + "\n")
        file.write(f"{'Rank':5}{'Product':20}{'Qty':8}{'Revenue'}\n")

        for idx, (prod, stats) in enumerate(top_products, 1):
            file.write(
                f"{idx:<5}{prod:20}{stats['qty']:<8}₹{stats['revenue']:,.2f}\n"
            )
        file.write("\n")

        # TOP CUSTOMERS
        file.write("TOP 5 CUSTOMERS\n")
        file.write("-" * 44 + "\n")
        file.write(f"{'Rank':5}{'Customer':12}{'Spent':15}{'Orders'}\n")

        for idx, (cid, stats) in enumerate(top_customers, 1):
            file.write(
                f"{idx:<5}{cid:12}₹{stats['spent']:,.2f}   {stats['count']}\n"
            )
        file.write("\n")

        # DAILY SALES
        file.write("DAILY SALES TREND\n")
        file.write("-" * 44 + "\n")
        file.write(f"{'Date':12}{'Revenue':15}{'Txns':8}{'Customers'}\n")

        for date, stats in daily_sorted:
            file.write(
                f"{date:12}₹{stats['revenue']:,.2f}   {stats['count']:<8}{len(stats['customers'])}\n"
            )
        file.write("\n")
        
        # PRODUCT PERFORMANCE

        file.write("PRODUCT PERFORMANCE ANALYSIS\n")
        file.write("-" * 44 + "\n")

        file.write(f"Best Selling Day:\n")
        file.write(
            f"{best_day} | Revenue: ₹{best_day_stats['revenue']:,.2f} "
            f"| Transactions: {best_day_stats['count']}\n\n"
        )

        file.write("Low Performing Products (Quantity < 10):\n")

        if low_products:
           for prod, qty, rev in sorted(low_products, key=lambda x: x[1]):
               file.write(
                   f"- {prod} | Qty: {qty} | Revenue: ₹{rev:,.2f}\n"
        )
        else:
            file.write("None\n")

        file.write("\nAverage Transaction Value per Region:\n")
        for region, avg_val in avg_tx_value_region.items():
            file.write(
                f"- {region}: ₹{avg_val:,.2f}\n"
        )

        file.write("\n")

        # API SUMMARY
        file.write("API ENRICHMENT SUMMARY\n")
        file.write("-" * 44 + "\n")
        file.write(f"Enriched Records: {len(enriched_success)}\n")
        file.write(f"Success Rate:    {success_rate:.2f}%\n")
        file.write("Unmatched Products:\n")

        for prod in sorted(set(failed_enrichment)):
            file.write(f"- {prod}\n")

    print(f"Sales report generated successfully at: {output_file}")



# -------- Part 1 imports --------
from utils.file_handler import (
    read_sales_data,
    parse_transactions,
    validate_and_filter
)

# -------- Part 2 imports --------
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)

# -------- Part 3 imports --------
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)

# -------- Part 4 import --------
from utils.api_handler import generate_sales_report


def main():
    try:
        # ==========================================================
        # HEADER
        # ==========================================================
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # ==========================================================
        # [1/10] READ SALES DATA
        # ==========================================================
        print("\n[1/10] Reading sales data...")
        file_path = "data/sales_data.txt"
        raw_lines = read_sales_data(file_path)
        print(f"Successfully read {len(raw_lines)} transactions")

        # ==========================================================
        # [2/10] PARSE & CLEAN
        # ==========================================================
        print("\n[2/10] Parsing and cleaning data...")
        parsed_transactions = parse_transactions(raw_lines)
        print(f"Parsed {len(parsed_transactions)} records")

        # ==========================================================
        # [3/10] VALIDATE DATA (internal)
        # ==========================================================
        valid_transactions, invalid_count, summary = validate_and_filter(parsed_transactions)

        # ==========================================================
        # [4/10] SHOW FILTER OPTIONS (based on VALID data)
        # ==========================================================
        print("\n[3/10] Filter Options Available:")
        regions = sorted({tx["Region"] for tx in valid_transactions})
        amounts = [tx["Quantity"] * tx["UnitPrice"] for tx in valid_transactions]

        print("Regions:", ", ".join(regions))
        print(f"Amount Range: {int(min(amounts))} - {int(max(amounts))}")

        choice = "n"
        print("\nDo you want to filter data? (y/n): n")
       
        # ==========================================================
        # [5/10] VALIDATION SUMMARY
        # ==========================================================
        print("\n[4/10] Validating transactions...")
        print(f"Valid: {summary['final_count']} | Invalid: {summary['invalid']}")

        # ==========================================================
        # [6/10] DATA ANALYSIS (PART 2)
        # ==========================================================
        print("\n[5/10] Analyzing sales data...")

        total_revenue = calculate_total_revenue(valid_transactions)
        region_sales = region_wise_sales(valid_transactions)
        top_products = top_selling_products(valid_transactions, n=5)
        customer_stats = customer_analysis(valid_transactions)
        daily_trend = daily_sales_trend(valid_transactions)
        peak_day = find_peak_sales_day(valid_transactions)
        low_products = low_performing_products(valid_transactions, threshold=10)

        print("Analysis complete")

        # ==========================================================
        # [7/10] FETCH API PRODUCTS
        # ==========================================================
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"Fetched {len(api_products)} products")

        # ==========================================================
        # [8/10] ENRICH SALES DATA
        # ==========================================================
        print("\n[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)

        success_count = sum(1 for tx in enriched_transactions if tx["API_Match"])
        success_rate = (success_count / len(enriched_transactions)) * 100

        print(
            f"Enriched {success_count}/{len(enriched_transactions)} "
            f"transactions ({success_rate:.1f}%)"
        )

        # ==========================================================
        # [9/10] SAVE ENRICHED DATA
        # ==========================================================
        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched_transactions)
        print("Saved to: data/enriched_sales_data.txt")

        # ==========================================================
        # [10/10] GENERATE REPORT
        # ==========================================================
        print("\n[9/10] Generating report...")
        generate_sales_report(
            valid_transactions,
            enriched_transactions,
            output_file="output/sales_report.txt"
        )
        print("Report saved to: output/sales_report.txt")

        # ==========================================================
        # COMPLETION
        # ==========================================================
        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\nERROR OCCURRED")
        print(str(e))


if __name__ == "__main__":
    main()
