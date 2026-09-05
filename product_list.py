#!/usr/bin/env python
# coding: utf-8

# # MotorPH Product List
# ## Loading Data Set

# In[1]:


import pandas as pd

product_list = pd.read_csv("raw_data/MotorPH_Products_List_2025.csv")

print(product_list.head().to_string())


# ## Data Preprocessing

# Check the dataset information

# In[2]:


print(product_list.info())
print()
print(product_list.describe())


# Check for missing values

# In[3]:


pd.isnull(product_list).count()


# 
# The **EntrDetails** column contains different data categories that can be split into different columns. I will place each details into the following categories.
# * Type
# * Engine Configuration
# * Cooling System
# * Displacement (cc)
# * Transmission.

# In[4]:


entr_no = "Product ID Number"
prod_name = "Product Name"
entr_details = "EntrDetails"
prod_type = "Product Type"
engine_conf = "Engine Configuration"
cooling_system = "Cooling System"
displacement = "Displacement (cc)"
transmission = "Transmission"
mfg_year = "Date of Manufacturing"
acquisition_date = "Date of Acquisition"
unit_price = "Unit Price"

new_columns = [entr_no, prod_name, prod_type, engine_conf, cooling_system, displacement, transmission, mfg_year, acquisition_date, unit_price]

split1 = product_list[entr_details].str.split("/", n=1, expand=True)
product_list[prod_type] = split1[0].str.strip()

split2 = split1[1].str.split(",", expand=True)
product_list[engine_conf] = split2[0].str.strip()
product_list[cooling_system] = split2[1].str.strip()
product_list[displacement] = split2[2].str.replace("cc", "", regex=False).astype(int)
product_list[transmission] = split2[3].str.strip()

product_list.drop(columns=[entr_details], inplace=True)


def rename_columns(old_column, new_column):
    product_list.rename(columns={old_column : new_column}, inplace=True)

rename_columns("Acquisiton", acquisition_date)
rename_columns("EntrName", prod_name)
rename_columns("EntrNo", entr_no)
rename_columns("Manufacturing Date", mfg_year)
rename_columns("UnitPrice", unit_price)

product_list = product_list[new_columns]


print(product_list.head().to_string())


# ## Export the cleaned data

# In[5]:


product_list.to_csv("cleaned_data/MotorPH_Products_List_2025_cleaned.csv", index=False)
print(product_list.head().to_string())

