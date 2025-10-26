
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ----------------------------
# 1️⃣ PAGE SETUP
# ----------------------------
st.set_page_config(page_title="InsightTrack Dashboard", layout="wide")
st.title("📊 InsightTrack — Sales Dashboard")


# ----------------------------
# 2️⃣ GENERATE DYNAMIC DATA
# ----------------------------
# Use a personalized seed to make the data unique
np.random.seed(hash("Mayuri2025") % 10000)

# Define regions and categories (you can modify these for originality)
regions = ["North", "South", "East", "West"]
categories = ["Electronics", "Furniture", "Clothing", "Sports"]

# Generate 120 random orders
num_orders = 120
dates = pd.date_range(start="2024-01-01", periods=num_orders, freq="7D")
data = {
    "OrderID": range(3001, 3001 + num_orders),
    "Date": dates,
    "Region": np.random.choice(regions, num_orders),
    "Category": np.random.choice(categories, num_orders),
    "Quantity": np.random.randint(1, 6, num_orders),
    "UnitPrice": np.round(np.random.uniform(50, 1000, num_orders), 2),
}

# Create DataFrame
df = pd.DataFrame(data)

# Calculate Sales and Profit dynamically
df["Sales"] = (df["Quantity"] * df["UnitPrice"]).round(2)
# Add a small unique profit margin per category
profit_map = {"Electronics": 0.12, "Furniture": 0.20, "Clothing": 0.35, "Sports": 0.25}
df["Profit"] = (df["Sales"] * df["Category"].map(profit_map) * np.random.uniform(0.9, 1.1, num_orders)).round(2)
# New feature: Profit Margin %
df["ProfitMargin"] = ((df["Profit"] / df["Sales"]) * 100).round(2)

# ----------------------------
# 3️⃣ SIDEBAR FILTERS
# ----------------------------
st.sidebar.header("Filter Orders")
selected_regions = st.sidebar.multiselect("Choose Regions", df["Region"].unique(), default=df["Region"].unique())
selected_categories = st.sidebar.multiselect("Choose Categories", df["Category"].unique(), default=df["Category"].unique())
date_range = st.sidebar.date_input(
    "Select Date Range", 
    [df["Date"].min().date(), df["Date"].max().date()]
)

# Apply filters
filtered_df = df[
    (df["Region"].isin(selected_regions)) &
    (df["Category"].isin(selected_categories)) &
    (df["Date"].dt.date.between(date_range[0], date_range[1]))
]

# ----------------------------
# 4️⃣ KEY METRICS
# ----------------------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df.shape[0]
avg_order_value = filtered_df["Sales"].mean() if total_orders else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Total Sales", f"${total_sales:,.2f}")
c2.metric("📈 Total Profit", f"${total_profit:,.2f}")
c3.metric("🧾 Total Orders", total_orders)
c4.metric("📊 Avg Order Value", f"${avg_order_value:,.2f}")

st.markdown("---")

# ----------------------------
# 5️⃣ VISUALIZATIONS
# ----------------------------
# Sales by Region (Bar Chart)
region_sales = filtered_df.groupby("Region")["Sales"].sum().reset_index()
fig_region = px.bar(region_sales, x="Region", y="Sales", color="Region", title="Sales by Region")
st.plotly_chart(fig_region, use_container_width=True)

# Sales by Category (Pie Chart)
category_sales = filtered_df.groupby("Category")["Sales"].sum().reset_index()
fig_category = px.pie(category_sales, names="Category", values="Sales", title="Sales by Category")
st.plotly_chart(fig_category, use_container_width=True)

# Monthly Trend (Line Chart)
filtered_df["Month"] = filtered_df["Date"].dt.to_period("M").dt.to_timestamp()
monthly_sales = filtered_df.groupby("Month")["Sales"].sum().reset_index()
fig_trend = px.line(monthly_sales, x="Month", y="Sales", markers=True, title="Monthly Sales Trend",line_shape="linear",color_discrete_sequence=["teal"])
st.plotly_chart(fig_trend, use_container_width=True)

# Profit Margin Scatter Plot (unique feature)
fig_profit = px.scatter(
    filtered_df, x="Sales", y="ProfitMargin", color="Category",
    hover_data=["OrderID", "Region"], title="Sales vs Profit Margin"
)
st.plotly_chart(fig_profit, use_container_width=True)

# ----------------------------
# 6️⃣ DATA TABLE + DOWNLOAD
# ----------------------------
st.subheader("Filtered Orders Table")
st.dataframe(filtered_df.sort_values("Date", ascending=False))

csv_data = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download Filtered Data", csv_data, "filtered_orders.csv", "text/csv")

# ----------------------------
# 7️⃣ INSIGHTS (unique personal touch)
# ----------------------------
st.markdown("---")
st.subheader("Quick Insights")
if total_orders > 0:
    top_region = filtered_df.groupby("Region")["Sales"].sum().idxmax()
    top_category = filtered_df.groupby("Category")["Sales"].sum().idxmax()
    st.write(f"- 🏆 Top Region: {top_region}")
    st.write(f"- 🥇 Top Category: {top_category}")
    st.write(f"- Average Quantity per Order: {filtered_df['Quantity'].mean():.2f}")
else:
    st.write("No orders match the selected filters.")

