import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ------------------- Page Configuration -------------------
st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

# ------------------- Load Dataset -------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/train.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors='coerce')
    df.drop(columns=['Postal Code'], inplace=True)
    df["year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Quarter"] = df["Order Date"].dt.quarter
    return df

df = load_data()

# ------------------- Sidebar Filters -------------------
st.sidebar.header("🔍 Filter Data")
years = st.sidebar.multiselect("Select Year(s):", options=df['year'].unique(), default=df['year'].unique())
months = st.sidebar.multiselect("Select Month(s):", options=df['Month'].unique(), default=df['Month'].unique())
quarters = st.sidebar.multiselect("Select Quarter(s):", options=df['Quarter'].unique(), default=df['Quarter'].unique())
regions = st.sidebar.multiselect("Select Region(s):", options=df['Region'].unique(), default=df['Region'].unique())
categories = st.sidebar.multiselect("Select Category(s):", options=df['Category'].unique(), default=df['Category'].unique())
sub_categories = st.sidebar.multiselect("Select Sub-Category(s):", options=df['Sub-Category'].unique(), default=df['Sub-Category'].unique())

# Filter dataframe
filtered_df = df[(df['year'].isin(years)) & (df['Month'].isin(months)) & (df['Quarter'].isin(quarters)) & (df['Region'].isin(regions)) & (df['Category'].isin(categories)) & (df['Sub-Category'].isin(sub_categories))]

# ------------------- KPI Metrics -------------------
total_sales = filtered_df['Sales'].sum()
total_orders = filtered_df['Order ID'].nunique()
total_customers = filtered_df['Customer ID'].nunique()
aov = total_sales / total_orders if total_orders else 0

st.markdown("<h2 style='text-align: center;'>📊 E-Commerce Dashboard</h2>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Sales", f"${total_sales:,.2f}", delta=f"${total_sales/1000:,.2f}K")
col2.metric("🛒 Total Orders", f"{total_orders:,}", delta=f"{total_orders//10:,}")
col3.metric("👥 Total Customers", f"{total_customers:,}", delta=f"{total_customers//10:,}")
col4.metric("📈 Avg Order Value", f"${aov:,.2f}", delta=f"${aov*0.1:,.2f}")
st.markdown("---")

# ------------------- Tabs -------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Trends", "Products & Categories", "Regions & Cities", "Top Customers", "Interactive Map"])

# ------------------- Tab 1: Trends -------------------
with tab1:
    st.subheader("📅 Monthly Sales Trend")
    monthly_sales = filtered_df.groupby(['year', 'Month'])['Sales'].sum().reset_index()
    monthly_sales['Month_Year'] = monthly_sales['Month'].astype(str) + '-' + monthly_sales['year'].astype(str)
    fig1 = px.line(monthly_sales, x='Month_Year', y='Sales', title="Monthly Sales Trend", markers=True, template="plotly_dark")
    fig1.update_layout(xaxis_tickangle=-45, yaxis_title="Total Sales", xaxis_title="Month-Year")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("📊 Quarterly Sales Trend")
    quarterly_sales = filtered_df.groupby(['year', 'Quarter'])['Sales'].sum().reset_index()
    quarterly_sales['Quarter_Year'] = 'Q' + quarterly_sales['Quarter'].astype(str) + '-' + quarterly_sales['year'].astype(str)
    fig2 = px.line(quarterly_sales, x='Quarter_Year', y='Sales', title="Quarterly Sales Trend", markers=True, template="plotly_dark")
    fig2.update_layout(xaxis_tickangle=-45, yaxis_title="Total Sales", xaxis_title="Quarter-Year")
    st.plotly_chart(fig2, use_container_width=True)

# ------------------- Tab 2: Products & Categories -------------------
with tab2:
    st.subheader("🛍 Top 10 Products by Sales")
    top_products = filtered_df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()
    fig3 = px.bar(top_products, x='Sales', y='Product Name', orientation='h', text='Sales', color='Sales', color_continuous_scale='Viridis', title="Top 10 Products by Sales", template="plotly_dark")
    fig3.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("📦 Sales by Category")
    category_sales = filtered_df.groupby('Category')['Sales'].sum().sort_values(ascending=False).reset_index()
    fig4 = px.bar(category_sales, x='Sales', y='Category', text='Sales', color='Sales', color_continuous_scale='Cividis', title="Sales by Category", template="plotly_dark")
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("📦 Sales by Sub-Category")
    sub_category_sales = filtered_df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).reset_index()
    fig5 = px.bar(sub_category_sales, x='Sales', y='Sub-Category', text='Sales', color='Sales', color_continuous_scale='Plasma', title="Sales by Sub-Category", template="plotly_dark")
    st.plotly_chart(fig5, use_container_width=True)

# ------------------- Tab 3: Regions & Cities -------------------
with tab3:
    st.subheader("🌍 Sales by Region")
    region_sales = filtered_df.groupby('Region')['Sales'].sum().sort_values(ascending=False).reset_index()
    fig6 = px.bar(region_sales, x='Sales', y='Region', text='Sales', color='Sales', color_continuous_scale='Teal', title="Sales by Region", template="plotly_dark")
    st.plotly_chart(fig6, use_container_width=True)

    st.subheader("🏙 Top 15 Cities by Sales")
    city_sales = filtered_df.groupby('City')['Sales'].sum().sort_values(ascending=False).head(15).reset_index()
    fig7 = px.bar(city_sales, x='Sales', y='City', text='Sales', color='Sales', color_continuous_scale='Inferno', title="Top 15 Cities by Sales", template="plotly_dark")
    st.plotly_chart(fig7, use_container_width=True)

# ------------------- Tab 4: Top Customers -------------------
with tab4:
    st.subheader("👑 Top 10 Customers by Sales")
    top_customers = filtered_df.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()
    fig8 = px.bar(top_customers, x='Sales', y='Customer Name', text='Sales', color='Sales', color_continuous_scale='Cividis', title="Top 10 Customers", template="plotly_dark")
    st.plotly_chart(fig8, use_container_width=True)

# ------------------- Tab 5: Interactive Map -------------------
with tab5:
    st.subheader("🗺 City-Level Sales Map")
    city_geo = filtered_df.groupby('City').agg({'Sales':'sum', 'Customer ID':'nunique'}).reset_index()
    import random
    random.seed(42)
    city_geo['lat'] = np.random.uniform(25, 50, size=len(city_geo))
    city_geo['lon'] = np.random.uniform(-125, -65, size=len(city_geo))
    fig_map = px.scatter_mapbox(city_geo, lat='lat', lon='lon', size='Sales', color='Sales', hover_name='City', hover_data=['Sales', 'Customer ID'], color_continuous_scale='Viridis', size_max=40, zoom=3, mapbox_style='carto-darkmatter', title="City-Level Sales Map")
    st.plotly_chart(fig_map, use_container_width=True)

# ------------------- Download Filtered Data -------------------
st.markdown("---")
st.subheader("💾 Download Filtered Data")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(label="Download CSV", data=csv, file_name='filtered_data.csv', mime='text/csv')

st.markdown("---")
st.markdown("Dashboard developed by Mrunal Asutkar | 🌐 Professional Portfolio Project")
