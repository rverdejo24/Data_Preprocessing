#!/usr/bin/env python
# coding: utf-8

# # MotorPH 3rd Quarter Sales Data for 2025

# ## Loading Data Set

# In[1]:


import pandas as pd
import re

sales_data = pd.read_csv("raw_data/MotorPH_Sales Data-3rd Quarter-Year 2025.csv")

print(sales_data.head().to_string())


# ## Data Set Information

# ### Data Summary

# In[2]:


print("Sales Data Information")
print(sales_data.info())
print()
print("Sales Data Summary")
print(sales_data.describe())
print()
print("Missing Values per column")
print(pd.isnull(sales_data).sum())


# ## Data Preprocessing

# Rename the columns

# In[3]:


old_date = "date"
old_product_name = "product"
old_unit_price = "unitprice"
old_product_quantity = "quantity"
old_total_price = "total"
old_payment = "payment"
old_client_type = "client_type"

new_date = "Date"
new_product_name = "Product Name"
new_unit_price = "Unit Price"
new_product_quantity = "Product Quantity"
new_total_price = "Total Price"
new_payment = "Payment Type"
new_client_type = "Client Type"

sales_data.rename(columns={
    old_date : new_date,
    old_product_name : new_product_name,
    old_unit_price : new_unit_price,
    old_product_quantity : new_product_quantity,
    old_total_price : new_total_price,
    old_payment : new_payment,
    old_client_type : new_client_type
}, inplace=True)

print(sales_data.head().to_string())


# ### Check for malformed data

# In[4]:


print("Checking malformed data in date column")
print(sales_data[new_date].unique())
patterns = {
    "YYYY-MM-DD": r"^\d{4}-\d{2}-\d{2}$",
    "M/D/YYYY":   r"^\d{1,2}/\d{1,2}/\d{4}$",
    "MM-DD-YYYY": r"^\d{2}-\d{2}-\d{4}$",
    "Mon-DD-YYYY": r"^[A-Za-z]{3}-\d{1,2}-\d{4}$",
}

for name, pattern in patterns.items():
    count = sales_data[new_date].str.match(pattern).sum()
    print(f"{name}: {count} rows")

invalid_day_00 = sales_data[new_date].str.contains(r"-00", regex=True, na=False)
print(f"Rows with day 00: {invalid_day_00.sum()}")
print(sales_data.loc[invalid_day_00, new_date])

print()
print("Checking malformed data in client type column")
print(sorted(sales_data[new_client_type].dropna().unique()))
print()
print("Checking malformed data in product name column")
for product in sorted(sales_data[new_product_name].unique()):
    print(product)


# ### Find and Clean the malformed dates

# In[5]:


def clean_date(value):
    if pd.isna(value):
        return pd.NaT

    value = value.strip()

    if re.match(r"^\d{1,2}/\d{1,2}/\d{4}$", value):
        first, second, year = value.split("/")
        if int(first) > 12:
            return pd.to_datetime(f"{second}/{first}/{year}", format="%m/%d/%Y")
        else:
            return pd.to_datetime(value, format="%m/%d/%Y")

    if re.match(r"^\d{2}-\d{2}-\d{4}$", value):
        if value == "08-40-2025":
            value = "08-04-2025"
        return pd.to_datetime(value, format="%m-%d-%Y")

    if re.match(r"^[A-Za-z]{3}-\d{1,2}-\d{4}$", value):
        return pd.to_datetime(value, format="%b-%d-%Y")

    if re.match(r"^\d{2}-\d{2}-\d{2}$", value):
        return pd.to_datetime(value, format="%m-%d-%y")

    if re.match(r"^\d{4}/\d{2}/\d{2}$", value):
        year, month, day = value.split("/")
        if day == "32":
            day = "31"
        return pd.to_datetime(f"{year}-{month}-{day}", format="%Y-%m-%d")

    if re.match(r"^\d{4}-\d{2}-00$", value):
        return pd.NaT

    return pd.NaT

sales_data[new_date] = sales_data[new_date].apply(clean_date)

still_missing = sales_data[sales_data[new_date].isnull()]
print(still_missing[[new_date]])
print(sales_data[new_date].unique())


# I planned to keep the rows with NaT dates for non-time-based analysis

# In[6]:


print(sales_data[sales_data["Date"].isna()].to_string())


# ### Find the malformed product name
# Find and clean the malformed data based on close match. Based on the previous code most malformed data ends with **x** replacing the last digit of the product name.

# In[7]:


products = sales_data[new_product_name].unique()

malformed = [p for p in products if p.endswith("x")]
clean = [p for p in products if not p.endswith("x")]

product_fixes = {}

for m in malformed:
    prefix = m[:-1]  # everything except the last character
    matches = [c for c in clean if c.startswith(prefix)]
    print(f"{m!r:30} -> possible match: {matches}")
    print("fixing...")
    if len(matches) == 1:
        product_fixes[m] = matches[0]
    else:
        print(f"Ambiguous or no match for {m!r}: {matches}")

print(product_fixes)


# ### Replaced the malformed data using the potential match

# In[8]:


sales_data[new_product_name] = sales_data[new_product_name].replace(product_fixes)
remaining = [p for p in sales_data[new_product_name].unique() if p.endswith("x")]
print("Remaining malformed products:")
print(remaining)


# ### Check if the total values are correct

# In[9]:


expected_total = sales_data[new_product_quantity] * sales_data[new_unit_price]

is_wrong = sales_data[new_total_price] != expected_total

wrong_values = is_wrong.sum()

print(f"Checked {len(sales_data)} rows.")
print(f"Incorrect 'total' values found: {wrong_values}")

if wrong_values > 0:
    print("\nRows with incorrect totals:")
    print(sales_data.loc[is_wrong, [new_date, new_product_name, new_unit_price, new_product_quantity, new_total_price]].to_string())


# ## Replace incorrect total values

# In[10]:


sales_data.loc[is_wrong, new_total_price] = expected_total[is_wrong]

is_wrong_after = sales_data[new_total_price] != expected_total

print(f"Checked {len(sales_data)} rows.")
print(f"Incorrect 'total' values found: {is_wrong_after.sum()}")


# #### Null value handling
# To handle the missing values in client_type, instead of dropping the affected rows, I will assign a new category "Unknown".

# In[11]:


print(sales_data[new_client_type].isnull().sum())


# In[12]:


sales_data[new_client_type] = sales_data[new_client_type].fillna("Unknown")

print(sales_data[new_client_type].isnull().sum())
print(sales_data[new_client_type].value_counts())


# Same logic applies for Payment Type

# In[13]:


sales_data[new_payment] = sales_data[new_payment].fillna("Unknown")

print(sales_data[new_payment].isnull().sum())
print(sales_data[new_payment].value_counts())


# In[14]:


print(sales_data.isnull().sum())


# In[15]:


print(sales_data.to_string())


# ## Export the cleaned sales data

# In[16]:


sales_data.to_csv("cleaned_data/MotorPH_Sales Data-3rd Quarter-Year 2025_cleaned.csv", index=False)

