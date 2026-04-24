import pandas as pd
import numpy as np

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv('Luxury_Housing_Bangalore.csv')

# -----------------------------
# CLEAN COLUMN NAMES FIRST
# -----------------------------
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_')
)

# -----------------------------
# UNIT SIZE CLEANING
# -----------------------------
df['unit_size_sqft'] = pd.to_numeric(df['unit_size_sqft'], errors='coerce')
df.loc[df['unit_size_sqft'] <= 0, 'unit_size_sqft'] = np.nan

df['unit_size_sqft'] = df.groupby('configuration')['unit_size_sqft']\
    .transform(lambda x: x.fillna(x.median()))

df['unit_size_sqft'].fillna(df['unit_size_sqft'].median(), inplace=True)
df['unit_size_sqft'] = df['unit_size_sqft'].round().astype('Int64')

# -----------------------------
# TICKET PRICE CLEANING
# -----------------------------
df['ticket_price_cr'] = (
    df['ticket_price_cr']
    .astype(str)
    .str.replace('[^0-9.]', '', regex=True)
)

df['ticket_price_cr'] = pd.to_numeric(df['ticket_price_cr'], errors='coerce')
df.loc[df['ticket_price_cr'] <= 0, 'ticket_price_cr'] = np.nan

df['ticket_price_cr'] = df.groupby('micro_market')['ticket_price_cr']\
    .transform(lambda x: x.fillna(x.median()))

# -----------------------------
# AMENITY SCORE CLEANING
# -----------------------------
df['amenity_score'] = pd.to_numeric(df['amenity_score'], errors='coerce')

df['amenity_score'] = df.groupby('micro_market')['amenity_score']\
    .transform(lambda x: x.fillna(x.median()))

df['amenity_score'].fillna(df['amenity_score'].median(), inplace=True)

# -----------------------------
# NORMALIZE TEXT FIELDS
# -----------------------------
df['micro_market'] = df['micro_market'].astype(str).str.strip().str.lower()
df['developer_name'] = df['developer_name'].astype(str).str.strip().str.lower()

# -----------------------------
# CONFIGURATION → BHK
# -----------------------------
df['configuration'] = (
    df['configuration']
    .astype(str)
    .str.upper()
    .str.strip()
    .str.replace('+', '', regex=False)
    .str.replace(' ', '')
)

df['bhk'] = df['configuration'].str.extract('(\d+)').astype(float)

# -----------------------------
# FEATURE ENGINEERING
# -----------------------------
df['price_per_sqft'] = (df['ticket_price_cr'] * 1e7) / df['unit_size_sqft']

# -----------------------------
# OUTLIER DETECTION
# -----------------------------
lower_limit = 2000
upper_limit = 25000

outliers = df[
    (df['price_per_sqft'] < lower_limit) |
    (df['price_per_sqft'] > upper_limit)
]

print("\n Outliers Detected:")
print(outliers[['micro_market', 'bhk', 'unit_size_sqft',
                'ticket_price_cr', 'price_per_sqft']].head())

# -----------------------------
# OUTLIER FIX
# -----------------------------
df['ticket_price_cr'] = df.groupby('micro_market')['ticket_price_cr']\
    .transform(lambda x: x.mask(
        (x < x.quantile(0.05)) | (x > x.quantile(0.95)),
        x.median()
    ))

# Business Rules
df.loc[(df['bhk'] == 1) & (df['ticket_price_cr'] > 2), 'ticket_price_cr'] = np.nan

df.loc[(df['unit_size_sqft'] > 5000) & (df['ticket_price_cr'] < 1), 'ticket_price_cr'] = np.nan

# Refill after rules
df['ticket_price_cr'] = df.groupby('micro_market')['ticket_price_cr']\
    .transform(lambda x: x.fillna(x.median()))

# Recalculate
df['price_per_sqft'] = (df['ticket_price_cr'] * 1e7) / df['unit_size_sqft']

# -----------------------------
# DATE FEATURE ENGINEERING
# -----------------------------
df['purchase_quarter'] = pd.to_datetime(df['purchase_quarter'], errors='coerce')

df['year'] = df['purchase_quarter'].dt.year
df['quarter_number'] = df['purchase_quarter'].dt.quarter
df['quarter_name'] = 'Q' + df['quarter_number'].astype(str) + '_' + df['year'].astype(str)
df['quarter_sort'] = df['year'] * 10 + df['quarter_number']

# -----------------------------
# BOOKING FLAG & STATUS
# -----------------------------
df['transaction_type'] = df['transaction_type'].astype(str).str.strip().str.lower()

df['booking_flag'] = df['transaction_type'].map({
    'primary': 1,
    'secondary': 0
})

# Mentor logic
df['booking_status'] = df['booking_flag'].map({
    1: 'booked',
    0: 'pending'
})

# -----------------------------
# FINAL VALIDATION
# -----------------------------
print("\n Final Price per Sqft Summary:")
print(df['price_per_sqft'].describe())

print("\n Remaining Outliers:")
print(df[
    (df['price_per_sqft'] < lower_limit) |
    (df['price_per_sqft'] > upper_limit)
].shape[0])

print("\n Missing Values:")
print(df.isnull().sum())

# -----------------------------
# SAVE FINAL DATA
# -----------------------------
df.to_csv("cleaned_data_final.csv", index=False)

print("\n Cleaning completed successfully!")
print(df.columns.tolist())