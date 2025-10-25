# ------------------- Ultimate E-Commerce Dashboard with Map & Heatmap -------------------
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

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
st.sidebar.header("Filter Data")
years = st.sidebar.multiselect("Select Year(s):", options=df['year'].unique(), default=df['year'].unique())
months = st.sidebar.multiselect("Select Month(s):", options=df['Month'].unique(), default=df['Month'].unique())
quarters = st.sidebar.multiselect("Select Quarter(s):", options=df['Quarter'].unique(), default=df['Quarter'].unique())
regions = st.sidebar.multiselect("Select Region(s):", options=df['Region'].unique(), default=df['Region'].unique())
categories = st.sidebar.multiselect("Select Category(s):", options=df['Category'].unique(), default=df['Category'].unique())
sub_categories = st.sidebar.multiselect("Select Sub-Category(s):", options=df['Sub-Category'].unique(), default=df['Sub-Category'].unique())

# Top N sliders
top_products_n = st.sidebar.slider("Top N Products", min_value=5, max_value=20, value=10)
top_customers_n = st.sidebar.slider("Top N Customers", min_value=5, max_value=20, value=10)
top_cities_n = st.sidebar.slider("Top N Cities", min_value=5, max_value=20, value=15)

# Apply filters
filtered_df = df[
    (df['year'].isin(years)) &
    (df['Month'].isin(months)) &
    (df['Quarter'].isin(quarters)) &
    (df['Region'].isin(regions)) &
    (df['Category'].isin(categories)) &
    (df['Sub-Category'].isin(sub_categories))
]

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

# ------------------- Tabs for Organized Layout -------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Trends", "Products & Categories", "Regions & Cities", "Top Customers", "Seasonality & Map"])

# ------------------- Tab 1: Trends -------------------
with tab1:
    st.subheader("Monthly Sales Trend")
    monthly_sales = filtered_df.groupby(['year', 'Month'])['Sales'].sum().reset_index()
    monthly_sales['Month_Year'] = monthly_sales['Month'].astype(str) + '-' + monthly_sales['year'].astype(str)
    fig1 = px.line(monthly_sales, x='Month_Year', y='Sales', markers=True, template="plotly_dark", title="Monthly Sales Trend")
    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Quarterly Sales Trend")
    quarterly_sales = filtered_df.groupby(['year', 'Quarter'])['Sales'].sum().reset_index()
    quarterly_sales['Quarter_Year'] = 'Q' + quarterly_sales['Quarter'].astype(str) + '-' + quarterly_sales['year'].astype(str)
    fig2 = px.line(quarterly_sales, x='Quarter_Year', y='Sales', markers=True, template="plotly_dark", title="Quarterly Sales Trend")
    fig2.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig2, use_container_width=True)

# ------------------- Tab 2: Products & Categories -------------------
with tab2:
    st.subheader(f"Top {top_products_n} Products by Sales")
    top_products = filtered_df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(top_products_n).reset_index()
    fig3 = px.bar(top_products, x='Sales', y='Product Name', orientation='h', color='Sales', text='Sales', color_continuous_scale='Viridis', template='plotly_dark')
    fig3.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Sales by Category")
    category_sales = filtered_df.groupby('Category')['Sales'].sum().sort_values(ascending=False).reset_index()
    fig4 = px.bar(category_sales, x='Sales', y='Category', color='Sales', text='Sales', color_continuous_scale='Cividis', template='plotly_dark')
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Sales by Sub-Category")
    sub_category_sales = filtered_df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).reset_index()
    fig5 = px.bar(sub_category_sales, x='Sales', y='Sub-Category', color='Sales', text='Sales', color_continuous_scale='Plasma', template='plotly_dark')
    st.plotly_chart(fig5, use_container_width=True)

# ------------------- Tab 3: Regions & Cities -------------------
with tab3:
    st.subheader("Sales by Region")
    region_sales = filtered_df.groupby('Region')['Sales'].sum().sort_values(ascending=False).reset_index()
    fig6 = px.bar(region_sales, x='Sales', y='Region', color='Sales', text='Sales', color_continuous_scale='Teal', template='plotly_dark')
    st.plotly_chart(fig6, use_container_width=True)

    st.subheader(f"Top {top_cities_n} Cities by Sales")
    city_sales = filtered_df.groupby('City')['Sales'].sum().sort_values(ascending=False).head(top_cities_n).reset_index()
    fig7 = px.bar(city_sales, x='Sales', y='City', color='Sales', text='Sales', color_continuous_scale='Inferno', template='plotly_dark')
    st.plotly_chart(fig7, use_container_width=True)

    # Interactive Map
    st.subheader("City-Level Sales Map")
    city_map = filtered_df.groupby(['City', 'State', 'Country'])['Sales'].sum().reset_index()
    fig_map = px.scatter_geo(city_map, locations="Country", locationmode='country names',
                             color="Sales", size="Sales",
                             hover_name="City", projection="natural earth",
                             template="plotly_dark", title="Sales by City (Map)")
    st.plotly_chart(fig_map, use_container_width=True)

# ------------------- Tab 4: Top Customers -------------------
with tab4:
    st.subheader(f"Top {top_customers_n} Customers by Sales")
    top_customers = filtered_df.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False).head(top_customers_n).reset_index()
    fig8 = px.bar(top_customers, x='Sales', y='Customer Name', color='Sales', text='Sales', color_continuous_scale='Cividis', template='plotly_dark')
    st.plotly_chart(fig8, use_container_width=True)

# ------------------- Tab 5: Seasonality Heatmap -------------------
with tab5:
    st.subheader("Monthly-Yearly Sales Heatmap")
    heatmap = filtered_df.groupby(['year', 'Month'])['Sales'].sum().reset_index()
    heatmap_pivot = heatmap.pivot(index='Month', columns='year', values='Sales')
    fig9 = px.imshow(heatmap_pivot, text_auto=True, color_continuous_scale='Viridis', title="Sales Heatmap: Month vs Year", template='plotly_dark')
    st.plotly_chart(fig9, use_container_width=True)

# ------------------- Download Filtered Data -------------------
with st.expander("📥 Download Filtered Data"):
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download CSV", data=csv, file_name='filtered_sales_data.csv', mime='text/csv')

# ------------------- Footer -------------------
st.markdown("---")
st.markdown("Made with ❤️ by Mrunal Asutkar | Ultimate Expert-Level Streamlit Dashboard")
