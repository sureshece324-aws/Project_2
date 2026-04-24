# Project_2
**Luxury_Housing_Analysis_Bangalore**

This project focuses on analyzing the premium real estate market in Bangalore. It involves a full data lifecycle: cleaning raw data with Python, migrating it to a MySQL database for structured storage, and building an interactive Power BI dashboard to uncover market trends and developer performance.

**Tech Stack**

Data Cleaning: Python (Pandas, NumPy)

Database: MySQL

Business Intelligence: Power BI

Version Control: GitHub

**Data Cleaning & Transformation (Cleaning_Data.py)**

The raw dataset contained inconsistencies typical of real estate records. The cleaning script performed the following critical tasks:

Column Normalization: Converted all column names to lowercase and replaced spaces with underscores for better compatibility with SQL.

Missing Value Imputation: * unit_size_sqft was filled using the median value specific to each unit configuration (e.g., all 3BHKs filled with 3BHK median).

ticket_price_cr and amenity_score were imputed based on the micro_market median to ensure regional pricing accuracy.

Outlier Management: * Identified properties with unrealistic price-per-sqft (below 2,000 or above 25,000).

Applied business rules: for example, 1BHKs priced over 2 Cr were flagged and reset to the market median.

**Feature Engineering:**

Calculated price_per_sqft by converting ticket prices into absolute INR values.

Created a time-dimension for quarters (quarter_name, quarter_sort) to enable trend analysis over time.

Derived booking_status (Booked vs. Pending) based on transaction types.

**Database Migration (SQL.py)**

To ensure a "Single Source of Truth," the cleaned data was migrated to a relational database:

Schema Definition: Created the Housing_Analysis table with optimized data types (e.g., FLOAT for pricing and DATE for time-series data).

Data Integrity: The script handles NaN values by converting them to SQL-friendly None (NULL) objects during the insertion process.

Batch Insertion: Used executemany to efficiently push the entire dataset from a Pandas DataFrame into the MySQL instance.

**Power BI Analysis (Housing_Analysis.pbix)**

The final interactive dashboard translates the structured data into three core areas of insight:

1. Executive KPIs
   
Total Market Revenue: Summary cards highlighting the scale of the luxury segment (e.g., 558.24K Cr).

Top 5 Builders: A real-time leaderboard showing the dominant developers by total revenue and booking success.

2. Market Dynamics
   
Configuration Demand: A donut chart showing the split between 3BHK, 4BHK, and 5BHK units, revealing the shift toward ultra-spacious living.

Amenity Value: A scatter plot analysis proving that projects with an amenity_score above 8.5 command a significant price premium.

3. Spatial Analysis & Drill-Through
   
Regional Concentration: Visualizes high-value project density in Bangalore's key growth corridors.

Drill-Through Detail: Allows users to right-click a specific builder or micro-market to view a granular, project-by-project breakdown of inventory and pricing.

**Key Business Findings**

Pricing Drivers: Premium facilities are the primary drivers of value; once a project hits an 8.5 amenity score, price-per-sqft increases exponentially.

Developer Trust: A small group of Tier-1 developers accounts for the majority of luxury revenue, indicating high brand loyalty in the premium segment.

Strategic Corridors: Hebbal and Whitefield remain the primary hubs for luxury launches due to infrastructure and proximity to tech hubs.

**Steps followed to clean the data:**

**Input file: Luxury_Housing_Bangalore - Input**

The data cleaning process addressed both structural and data-level inconsistencies across the dataset. Using the **Cleaning_data.py** script, tasks such as column header standardization, handling missing or empty rows, removal of unwanted symbols and extra spaces, regional data imputation, and outlier treatment based on business rules were performed. This process generated a refined dataset **(Cleaned_data - output.csv)** ready for analysis.

Subsequently, a SQL database was created using **SQL.py**, and the cleaned data was loaded into MySQL. Finally, the database was integrated with **Power BI Desktop** to develop interactive dashboards and data visualizations.
