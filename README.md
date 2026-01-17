# Sales Analytics System

A Python-based sales analytics application that processes sales transaction data, performs statistical analysis, integrates external product data via API, enriches transactions, and generates a comprehensive sales report.

## Project Structure

sales-analytics-system/
│
├── main.py
├── README.md
├── requirements.txt   
│
├── data/
│   ├── sales_data.txt
│   └── enriched_sales_data.txt
│
├── output/
│   └── sales_report.txt
│
└── utils/
    ├── file_handler.py
    ├── data_processor.py
    └── api_handler.py

## Prerequisites

- Python 3.9 or higher

- Internet connection (required for API integration)

## Required Python Libraries

This project uses standard Python libraries plus one external package:

- requests

## Setup Instructions

 1. Clone or download the repository

    git clone <repository-url>
    cd sales-analytics-system


 2. Ensure input data file exists

    - data/sales_data.txt


 3. Verify folder structure

    - data/ folder must exist

    - utils/ folder must contain all helper modules

    - output/ folder will be created automatically when running the program

## How to Run the Project

From the project root directory, run:

__python main.py__   

## What Happens When You Run main.py

The program executes the following steps automatically:

1. Reads sales data from file

2. Parses and cleans transaction records

3. Displays available regions and transaction ranges

4. Validates transactions

5. Performs sales analytics:

  - Total revenue
  - Region-wise sales
  - Top products
  - Customer analysis
  - Daily sales trend
  - Peak sales day
  - Low-performing products

6. Fetches product data from DummyJSON API

7. Enriches sales transactions with API data

8. Saves enriched data to:

__data/enriched_sales_data.txt__


9. Generates a detailed sales report:

__output/sales_report.txt__

## Output Files
1. Enriched Sales Data

Location: __data/enriched_sales_data.txt__
Contains original transaction data plus:

  - API category
  - API brand
  - API rating
  - API match status

2. Sales Report

Location: __output/sales_report.txt__
Includes:

  - Overall sales summary
  - Region-wise performance
  - Top products & customers
  - Daily trends
  - Product performance analysis
  - API enrichment summary

## API Used

__DummyJSON Products API__

 - Base URL:

     https://dummyjson.com/products


 Used to enrich sales data with:

  - Product category
  - Brand
  - Rating  

 ## Error Handling

  - All major steps are wrapped in try-except

  - User-friendly messages shown on failure

  - Program exits gracefully without crashing 