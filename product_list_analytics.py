#!/usr/bin/env python
# coding: utf-8

# # Descriptive Analytics #

# Load Data Set

# In[30]:


import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt

product_list = pd.read_csv("cleaned_data/MotorPH_Products_List_2025_cleaned.csv")

product_list.head(10)


# ## Counts By Product Type ##

# In[31]:


product_type_counts = product_list.groupby("Product Type")["Product Name"].count().sort_values(ascending=False)

plt.bar(product_type_counts.index, product_type_counts.values)

plt.xlabel("Product Type")
plt.xticks(rotation=45)
plt.ylabel("Number of Units")
plt.title("MotorPH Product Inventory - Count by Product Type (Q3 2025)")
plt.tight_layout()
plt.show()


# ## Price per Product ##

# In[46]:


print(product_list[["Product Name", "Unit Price"]].sort_values(by="Unit Price", ascending=False))


# ## Mean, Median, and Mode comparison of Unit Price ##

# In[32]:


prices = product_list["Unit Price"]

# stats
mean = prices.mean()
median = prices.median()
mode = prices.mode().iloc[0]

# KDE curve
kde = gaussian_kde(prices)

x = np.linspace(prices.min(), prices.max(), 500)
y = kde(x)

plt.plot(x, y)

# Height of the curve per stats
mode_y = kde(mode)[0]
median_y = kde(median)[0]
mean_y = kde(mean)[0]

# vertical lines
plt.vlines(mode, 0, mode_y, label="Mode")
plt.vlines(median, 0, median_y, label="Median")
plt.vlines(mean, 0, mean_y, label="Mean")

# Labels
plt.text(mode, mode_y, "Mode", ha="center", va="bottom")
plt.text(median, median_y, "Median", ha="center", va="bottom")
plt.text(mean, mean_y, "Mean", ha="center", va="bottom")

plt.xlabel("Unit Price")
plt.ylabel("Density")
plt.title("MotorPH Price Distribution of Products")

# Formats
# plt.ticklabel_format(style="plain", axis="y")
plt.gca().xaxis.set_major_formatter(
    FuncFormatter(lambda x, pos: f"₱{x:,.0f}")
)

plt.tight_layout()
plt.show()


# ## Product Price Distribution ##

# In[33]:


plt.hist(prices, bins=10, edgecolor="black")

plt.xlabel("Unit Price")
plt.ylabel("Number of Products")
plt.title("MotorPH Product Price Distribution")

plt.gca().xaxis.set_major_formatter(
    FuncFormatter(lambda x, pos: f"₱{x:,.0f}")
)

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ## Units Acquired per year ##

# In[38]:


product_list["Date of Acquisition"] = product_list["Date of Acquisition"]

acquisition_counts = product_list.groupby("Date of Acquisition")["Product Name"].count().sort_index()

plt.bar(acquisition_counts.index.astype(str), acquisition_counts.values)

plt.xlabel("Acquisition Year")
plt.ylabel("Units Acquired")
plt.title("Units Acquired per Year")

plt.tight_layout()
plt.show()

