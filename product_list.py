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


pd.isnull(product_list).sum()


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


# # Product Analysis #

# ## Load and read the cleaned dataset ##

# In[6]:


product_list = pd.read_csv("cleaned_data/MotorPH_Products_List_2025_cleaned.csv")


# ## Inspect the dataset ##

# In[11]:


print(product_list.columns)
print()
print(product_list.shape)
print()
print(product_list.dtypes)
print()
print(product_list.nunique())
print()
print(product_list.info())
print()
print(product_list["Unit Price"].describe())


# ## View the total number of products ##

# In[12]:


total_products = product_list["Product Name"].count()
print(total_products)


# ## Counts by product type ##

# In[15]:


product_type_counts = product_list.groupby("Product Type")["Product Name"].count().sort_values(ascending=False)
print(product_type_counts)

total_product_types = product_list["Product Type"].nunique()
print(total_product_types)


# ## Unit Price Statistics ##

# In[19]:


average_price = product_list["Unit Price"].mean()
minimum_price = product_list["Unit Price"].min()
maximum_price = product_list["Unit Price"].max()
median_price = product_list["Unit Price"].median()

print(f"Average Price: {average_price:,.2f}")
print(f"Minimum Price: {minimum_price:,.2f}")
print(f"Maximum Price: {maximum_price:,.2f}")
print(f"Median Price: {median_price:,.2f}")


# ## Cheapest Product ##

# In[23]:


cheapest_product = product_list.loc[product_list["Unit Price"].idxmin(),["Product Name", "Product Type", "Unit Price"]]
print(f"Cheapest Product:\n{cheapest_product}")


# ## Most Expensive Product ##

# In[24]:


most_expensive_product = product_list.loc[product_list["Unit Price"].idxmax(),["Product Name", "Product Type", "Unit Price"]]
print(f"Most Expensive Product:\n{most_expensive_product}")


# ## Total Inventory Cost ##

# In[25]:


total_inventory_cost = product_list["Unit Price"].sum()
print(f"Total Inventory Cost: {total_inventory_cost:,.2f}")


# ## Number of Products Acquired Each year ##

# In[26]:


acquisition_counts = product_list.groupby("Date of Acquisition")["Product Name"].count().sort_index()
print(acquisition_counts)


# ## Highest Acquisition Year and Count ##

# In[27]:


highest_acquisition_year = acquisition_counts.idxmax()
highest_acquisition_count = acquisition_counts.max()

print(f"Highest Acquisition Year: {highest_acquisition_year}"
      f"\nHighest Acquisition Count: {highest_acquisition_count}")


# ## Lowest Acquisition Year and Count ##

# In[28]:


lowest_acquisition_year = acquisition_counts.idxmin()
lowest_acquisition_count = acquisition_counts.min()

print(f"Lowest Acquisition Year: {lowest_acquisition_year}"
      f"\nLowest Acquisition Count: {lowest_acquisition_count}")

