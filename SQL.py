import mysql.connector
import pandas as pd
import numpy as np

# -----------------------------
# LOAD CSV
# -----------------------------
file = "C:/Users/Neil/Documents/Suresh/Luxury_Housing/cleaned_data_final.csv"
df = pd.read_csv(file)

# -----------------------------
# CONNECT TO MYSQL
# -----------------------------
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Beast@9202",
    database="luxury_housing"
)

cursor = mydb.cursor()

#cursor.execute("DROP TABLE IF EXISTS Housing_Analysis;")

# -----------------------------
# CREATE TABLE
# -----------------------------
create_table_query = """
CREATE TABLE IF NOT EXISTS Housing_Analysis (
    property_id VARCHAR(20),
    micro_market VARCHAR(100),
    project_name VARCHAR(150),
    developer_name VARCHAR(100),
    unit_size_sqft INT,
    configuration VARCHAR(20),
    ticket_price_cr FLOAT,
    transaction_type VARCHAR(50),
    buyer_type VARCHAR(50),
    purchase_quarter DATE,
    amenity_score FLOAT,
    possession_status VARCHAR(50),
    sales_channel VARCHAR(50),
    buyer_comments TEXT,
    price_per_sqft FLOAT,
    year INT,
    quarter_number INT,
    quarter_name VARCHAR(20),
    quarter_sort INT,
    booking_flag INT,
    booking_status VARCHAR(20)
);
"""
cursor.execute(create_table_query)

# -----------------------------
# SELECT REQUIRED COLUMNS
# -----------------------------
df = df[
    [
        'property_id',
        'micro_market',
        'project_name',
        'developer_name',
        'unit_size_sqft',
        'configuration',
        'ticket_price_cr',
        'transaction_type',
        'buyer_type',
        'purchase_quarter',
        'amenity_score',
        'possession_status',
        'sales_channel',
        'buyer_comments',
        'price_per_sqft',
        'year',
        'quarter_number',
        'quarter_name',
        'quarter_sort',
        'booking_flag',
        'booking_status'
    ]
]

# -----------------------------
# FIX NaN + DATATYPES
# -----------------------------
df = df.replace({np.nan: None})

df['year'] = df['year'].astype('Int64')
df['quarter_number'] = df['quarter_number'].astype('Int64')
df['booking_flag'] = df['booking_flag'].astype('Int64')

# DO NOTHING to property_id
df['property_id'] = df['property_id'].astype(str)

# Convert nullable ints → Python objects (VERY IMPORTANT)
for col in ['year', 'quarter_number', 'booking_flag']:
    df[col] = df[col].astype(object)

# Convert date column properly
df['purchase_quarter'] = pd.to_datetime(df['purchase_quarter'], errors='coerce').dt.date

# -----------------------------
# INSERT QUERY
# -----------------------------
insert_query = """
INSERT INTO Housing_Analysis (
    property_id,
    micro_market,
    project_name,
    developer_name,
    unit_size_sqft,
    configuration,
    ticket_price_cr,
    transaction_type,
    buyer_type,
    purchase_quarter,
    amenity_score,
    possession_status,
    sales_channel,
    buyer_comments,
    price_per_sqft,
    year,
    quarter_number,
    quarter_name,
    quarter_sort,
    booking_flag,
    booking_status
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# -----------------------------
# CONVERT ROWS (FIXED PART)
# -----------------------------
rows = [
    tuple(None if pd.isna(x) else x for x in row)
    for row in df.to_numpy()
]

print(f"{len(rows)} rows ready to insert.")

# -----------------------------
# INSERT DATA
# -----------------------------
cursor.executemany(insert_query, rows)
mydb.commit()

print(f"{cursor.rowcount} rows inserted successfully.")

# -----------------------------
# CLOSE CONNECTION
# -----------------------------
cursor.close()
mydb.close()

