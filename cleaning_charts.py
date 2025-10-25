import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# load dataset
df=pd.read_csv("data/train.csv")
print(df.head(10))

# date format to make readable
df["Order Date"]=pd.to_datetime(df["Order Date"],dayfirst=True, errors='coerce')

# drop 'Postal Code' Column
df.drop(columns=['Postal Code'],inplace=True)

# creating year,month,quarter column
df["year"]=df["Order Date"].dt.year
df['Month']=df['Order Date'].dt.month
df['Quarter']=df['Order Date'].dt.quarter

# total sales
total_Sales=df['Sales'].sum()

# Total Orders
total_orders=df['Order ID'].nunique()

# total customes
total_customers=df['Customer ID'].nunique()

#  average order value
aov=total_Sales/total_orders


# -------------monthly sales trend Graph-------------
monthly_sales = df.groupby(['year', 'Month'])['Sales'].sum().reset_index()

# Create a month-year label for X-axis
monthly_sales['Month_Year'] = monthly_sales['Month'].astype(str) + '-' + monthly_sales['year'].astype(str)
                                                                                                      
# Plot line chart
plt.figure(figsize=(12,6))
sns.lineplot(data=monthly_sales, x='Month_Year', y='Sales', marker='o')
plt.xticks(rotation=45)
plt.title("Monthly Sales Trend")
plt.xlabel("Month-Year")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.show()

# -------------top-product by sales graph------------

# Group by Product Name and sum sales
top_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()

# Plot bar chart
plt.figure(figsize=(12,6))
sns.barplot(data=top_products, x='Sales', y='Product Name', palette='viridis')
plt.title("Top 10 Products by Sales")
plt.xlabel("Total Sales")
plt.ylabel("Product Name")
plt.tight_layout()
plt.show()

# ---------sales by category/sub-category graph------------

category_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False).reset_index()

# Plot chart for Category
plt.figure(figsize=(8,5))
sns.barplot(data=category_sales, x='Sales', y='Category', palette='coolwarm')
plt.title("Sales by Category")
plt.xlabel("Total Sales")
plt.ylabel("Category")
plt.tight_layout()
plt.show()

sub_category_sales = df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).reset_index()

# Plot chart for sub-category
plt.figure(figsize=(10,6))
sns.barplot(data=sub_category_sales, x='Sales', y='Sub-Category', palette='magma')
plt.title("Sales by Sub-Category")
plt.xlabel("Total Sales")
plt.ylabel("Sub-Category")
plt.tight_layout()
plt.show()

# ---------sales by region/city-----------

# Group by Region and sum sales
region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False).reset_index()

# Plot bar chart for Region
plt.figure(figsize=(8,5))
sns.barplot(data=region_sales, x='Sales', y='Region', palette='cool')
plt.title("Sales by Region")
plt.xlabel("Total Sales")
plt.ylabel("Region")
plt.tight_layout()
plt.show()

#-----------quaterly sales trend------------

# Group by Year and Quarter, sum sales
quarterly_sales = df.groupby(['year', 'Quarter'])['Sales'].sum().reset_index()

# Create a label for X-axis 
quarterly_sales['Quarter_Year'] = 'Q' + quarterly_sales['Quarter'].astype(str) + '-' + quarterly_sales['year'].astype(str)

# Plot line chart
plt.figure(figsize=(12,6))
sns.lineplot(data=quarterly_sales, x='Quarter_Year', y='Sales', marker='o')
plt.xticks(rotation=45)
plt.title("Quarterly Sales Trend")
plt.xlabel("Quarter-Year")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.show()
